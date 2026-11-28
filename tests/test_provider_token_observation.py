"""Offline transport fixtures; no provider calls."""
import json
import sys
from types import SimpleNamespace
from urllib import request

import pytest

from kora.adapters.openai_adapter import OpenAIAdapter
from kora.adapters.openai_compatible_local import OpenAICompatibleLocalAdapter
from kora.solution.economics import EconomicsNode, ExecutionPolicy, WorkloadEconomicsRunner, compare_economics


@pytest.mark.parametrize('provider', ['local', 'remote'])
@pytest.mark.parametrize('counts,expected', [({}, (None, None)), ({'in': 0, 'out': 0}, (100.0, 100.0)), ({'in': 3}, (70.0, None)), ({'in': 1.5, 'out': True}, (None, None)), ({'in': None, 'out': -1}, (None, None))])
def test_provider_token_reductions_require_observed_counts(monkeypatch, provider, counts, expected):
    answer = {'answer': 'ok'}
    if provider == 'local':
        keys = {'in': 'prompt_tokens', 'out': 'completion_tokens'}
        payload = {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {keys[k]: v for k, v in counts.items()}}
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return json.dumps(payload).encode()
        monkeypatch.setattr(request, 'urlopen', lambda *a, **kw: Response())
        adapter = OpenAICompatibleLocalAdapter(environ={'KORA_LOCAL_OPENAI_ENDPOINT': 'http://127.0.0.1:9999', 'KORA_LOCAL_OPENAI_MODEL': 'fixture', 'KORA_LOCAL_OPENAI_RUNTIME_ID': 'fixture'})
    else:
        keys = {'in': 'input_tokens', 'out': 'output_tokens'}
        payload = {'output_text': json.dumps(answer), 'usage': {keys[k]: v for k, v in counts.items()}}
        # Stub the transport and credential lookup before constructing the adapter.
        monkeypatch.setattr('kora.adapters.openai_adapter._openai_api_key_from_environment', lambda: 'offline-fixture')
        monkeypatch.setenv('KORA_OPENAI_CACHE_ID', 'fixture')
        monkeypatch.setitem(sys.modules, 'requests', SimpleNamespace(post=lambda *a, **kw: SimpleNamespace(status_code=200, json=lambda: payload), RequestException=RuntimeError))
        adapter = OpenAIAdapter(model='fixture')
    runner = WorkloadEconomicsRunner(nodes=(EconomicsNode('n', 'fixture', 'routine'),), adapters={'a': adapter})
    policy = ExecutionPolicy('test', {'routine': 'a'}, exact_reuse=True)
    result = runner.run(workload={'brief': {}}, policy=policy)
    baseline = {'tokens_in': 10, 'tokens_out': 10, 'model_calls': 1, 'adapter_attempts': 1}
    comparison = compare_economics(baseline, result)
    assert result['output'] == answer
    assert (comparison['input_token_reduction_percent'], comparison['output_token_reduction_percent']) == expected
    assert comparison['model_call_reduction_percent'] == 0.0
    cached = runner.run(workload={'brief': {}}, policy=policy)
    comparison = compare_economics(baseline, cached)
    assert comparison['input_token_reduction_percent'] == comparison['output_token_reduction_percent'] == 100.0
    assert cached['adapter_attempts'] == 0
