"""Bedrock Converse -> OpenAI-compatible shim.

Mimics only the `.chat.completions.create(model=, messages=, temperature=,
max_tokens=)` interface that the LLM class calls, and returns an OpenAI-shaped
response (`choices[0].message.content`, `usage.prompt_tokens/completion_tokens`).
This lets run.py use Bedrock with zero changes to the runner/LLM/grader/router.

The key is read only from the BEDROCK_KEY environment variable (Bearer token);
it is never stored in a file or in code.
"""
import json
import os
import time
import urllib.request
import urllib.error

REGION = os.getenv("BEDROCK_REGION", "us-east-1")
_ENDPOINT = "https://bedrock-runtime.{region}.amazonaws.com/model/{mid}/converse"


class _Msg:
    def __init__(self, content): self.content = content


class _Choice:
    def __init__(self, content): self.message = _Msg(content)


class _Usage:
    def __init__(self, pin, pout):
        self.prompt_tokens = pin
        self.completion_tokens = pout


class _Resp:
    def __init__(self, content, pin, pout):
        self.choices = [_Choice(content)]
        self.usage = _Usage(pin, pout)


class _Completions:
    def __init__(self, key, region):
        self.key = key
        self.region = region

    def create(self, model, messages, temperature=0.0, max_tokens=256, **_):
        # Converse takes `system` as a top-level field, not inside messages (OpenAI puts it in messages[0]).
        system = [{"text": m["content"]} for m in messages if m["role"] == "system"]
        convo = [{"role": m["role"], "content": [{"text": m["content"]}]}
                 for m in messages if m["role"] != "system"]
        mid = model if model.startswith("us.") else "us." + model
        url = _ENDPOINT.format(region=self.region, mid=mid)
        body = {"messages": convo,
                "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperature}}
        if system:
            body["system"] = system
        data = json.dumps(body).encode("utf-8")

        last_err = None
        for attempt in range(5):
            req = urllib.request.Request(
                url, data=data, method="POST",
                headers={"Authorization": "Bearer " + self.key,
                         "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    out = json.loads(r.read())
                text = out["output"]["message"]["content"][0]["text"]
                u = out.get("usage", {})
                return _Resp(text, u.get("inputTokens", 0), u.get("outputTokens", 0))
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(2 ** attempt)  # 1,2,4,8,16s backoff
                    continue
                raise
            except urllib.error.URLError as e:
                last_err = e
                time.sleep(2 ** attempt)
                continue
        raise RuntimeError("Bedrock call failed after retries: %r" % last_err)


class _Chat:
    def __init__(self, key, region):
        self.completions = _Completions(key, region)


class BedrockClient:
    """Drop-in replacement that slots into the OpenAI() position."""
    def __init__(self, api_key=None, region=REGION):
        key = api_key or os.getenv("BEDROCK_KEY")
        if not key:
            raise RuntimeError("BEDROCK_KEY environment variable is not set (export BEDROCK_KEY=...)")
        self.chat = _Chat(key, region)
