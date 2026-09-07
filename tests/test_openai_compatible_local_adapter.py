import json
from urllib import request

import pytest

from kora.adapters.openai_compatible_local import (
    LocalOpenAICompatibleError,
    OpenAICompatibleLocalAdapter,
)


def test_rejects_non_loopback_endpoint():
    with pytest.raises(LocalOpenAICompatibleError, match="loopback"):
        OpenAICompatibleLocalAdapter(environ={"KORA_LOCAL_OPENAI_ENDPOINT":"https://example.com","KORA_LOCAL_OPENAI_MODEL":"x"})


def test_parses_local_openai_response(monkeypatch):
    class Response:
        def __enter__(self): return self
        def __exit__(self,*args): return False
        def read(self): return b''
    payload={"choices":[{"message":{"content":json.dumps({"answer":"ok"})}}],"usage":{"prompt_tokens":7,"completion_tokens":3}}
    class FakeResponse(Response):
        def __iter__(self): return iter([])
    def fake_urlopen(req, timeout):
        class F:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return json.dumps(payload).encode()
        return F()
    monkeypatch.setattr(request,"urlopen",fake_urlopen)
    adapter=OpenAICompatibleLocalAdapter(environ={"KORA_LOCAL_OPENAI_ENDPOINT":"http://127.0.0.1:9999","KORA_LOCAL_OPENAI_MODEL":"qwen"})
    result=adapter.run(task_id="n",input={"x":1},budget={"max_tokens":8},output_schema={})
    assert result["output"]=={"answer":"ok"}
    assert result["usage"]["tokens_in"]==7
    assert result["meta"]["remote_provider_calls"]==0


def test_local_prompt_uses_required_key_hint_not_full_schema(monkeypatch):
    captured = {}
    payload={"choices":[{"message":{"content":json.dumps({"answer":"ok"})},"finish_reason":"stop"}],"usage":{"prompt_tokens":7,"completion_tokens":3}}
    def fake_urlopen(req, timeout):
        captured.update(json.loads(req.data.decode()))
        class F:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return json.dumps(payload).encode()
        return F()
    monkeypatch.setattr(request,"urlopen",fake_urlopen)
    adapter=OpenAICompatibleLocalAdapter(environ={"KORA_LOCAL_OPENAI_ENDPOINT":"http://127.0.0.1:9999","KORA_LOCAL_OPENAI_MODEL":"qwen"})
    schema={"type":"object","properties":{"answer":{"type":"string"}},"required":["answer"],"additionalProperties":False}
    adapter.run(task_id="n",input={"x":1},budget={"max_tokens":8},output_schema=schema)
    user=json.loads(captured["messages"][1]["content"])
    assert user["required_output_keys"]==["answer"]
    assert user["output_shape"]=={"answer":{"type":"string"}}
    assert "output_schema" not in user


def test_local_api_key_file_is_supported_without_exposing_value(tmp_path, monkeypatch):
    key_file=tmp_path/"local.key"
    key_file.write_text("secret-local-token")
    payload={"choices":[{"message":{"content":json.dumps({"answer":"ok"})},"finish_reason":"stop"}],"usage":{}}
    captured={}
    def fake_urlopen(req, timeout):
        captured.update(dict(req.header_items()))
        class F:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return json.dumps(payload).encode()
        return F()
    monkeypatch.setattr(request,"urlopen",fake_urlopen)
    adapter=OpenAICompatibleLocalAdapter(environ={"KORA_LOCAL_OPENAI_ENDPOINT":"http://127.0.0.1:9999","KORA_LOCAL_OPENAI_MODEL":"qwen","KORA_LOCAL_OPENAI_API_KEY_FILE":str(key_file),"KORA_LOCAL_OPENAI_RUNTIME_ID":"runtime-test"})
    adapter.run(task_id="n",input={"x":1},budget={},output_schema={"type":"object","required":["answer"]})
    assert captured["Authorization"]=="Bearer secret-local-token"
    assert "secret-local-token" not in repr(adapter.cache_identity())


def test_schema_hint_preserves_array_item_shape_only():
    from kora.adapters.openai_compatible_local import _schema_hint
    schema={
        "type":"object",
        "properties":{
            "evidence":{
                "type":"array",
                "items":{
                    "type":"object",
                    "properties":{"source_id":{"type":"string"},"point":{"type":"string"}},
                    "required":["source_id","point"],
                },
            },
            "source_ids":{"type":"array","items":{"type":"string"}},
        },
        "required":["evidence","source_ids"],
    }
    assert _schema_hint(schema)=={
        "evidence":{"type":"array","items_type":"object","item_required_keys":["source_id","point"]},
        "source_ids":{"type":"array","items_type":"string"},
    }


def test_cache_identity_requires_runtime_id_for_local_reuse():
    adapter=OpenAICompatibleLocalAdapter(environ={"KORA_LOCAL_OPENAI_ENDPOINT":"http://127.0.0.1:9999","KORA_LOCAL_OPENAI_MODEL":"qwen"})
    import pytest
    with pytest.raises(LocalOpenAICompatibleError,match="RUNTIME_ID"):
        adapter.cache_identity()
