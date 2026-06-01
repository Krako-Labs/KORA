from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_kora_studio_browser_csp.py"
CI_OPTIONAL_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_kora_studio_browser_csp_ci_optional.sh"
SPEC = importlib.util.spec_from_file_location("check_kora_studio_browser_csp", SCRIPT_PATH)
assert SPEC is not None
browser_csp = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(browser_csp)


def test_browser_csp_smoke_rejects_non_local_urls() -> None:
    with pytest.raises(browser_csp.BrowserCspSmokeError):
        browser_csp.run_browser_csp_smoke("https://example.com")


def test_browser_csp_smoke_spec_keeps_local_preview_boundaries() -> None:
    spec = browser_csp._build_playwright_spec()

    assert "default-src 'none'" in spec
    assert "style-src 'self'" in spec
    assert "script-src 'self'" in spec
    assert "connect-src 'self'" in spec
    assert "/studio-assets/studio.css" in spec
    assert "/studio-assets/studio.js" in spec
    assert "koraStudioScriptStatus" in spec
    assert "koraStudioSelectedRunState" in spec
    assert "#kora-composer-run-local-harness-button" in spec
    assert "Content Security Policy" in spec
    assert "unsafe-inline" not in spec
    assert "unsafe-eval" not in spec
    assert "https://" not in spec


def test_browser_csp_smoke_invokes_playwright_without_repo_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append({"command": command, **kwargs})
        if "node" in command:
            return SimpleNamespace(returncode=0, stdout="/tmp/npm-cache/_npx/example/node_modules\n", stderr="")
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(browser_csp.shutil, "which", lambda name: "/usr/bin/npx" if name == "npx" else None)
    monkeypatch.setattr(browser_csp.subprocess, "run", fake_run)

    results = browser_csp.run_browser_csp_smoke("http://127.0.0.1:8765/", browser="chromium", timeout=1234)

    assert "/ browser CSP header ok" in results
    assert len(calls) == 2
    command = calls[1]["command"]
    assert command[:5] == ["npx", "--yes", "--package", "@playwright/test", "playwright"]
    assert "test" in command
    assert "--browser" in command
    assert "chromium" in command
    assert "--timeout" in command
    assert "1234" in command
    env = calls[1]["env"]
    assert env["KORA_STUDIO_BROWSER_BASE_URL"] == "http://127.0.0.1:8765"
    assert env["NODE_PATH"] == "/tmp/npm-cache/_npx/example/node_modules"


def test_browser_csp_smoke_reports_missing_npx(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(browser_csp.shutil, "which", lambda name: None)

    with pytest.raises(browser_csp.BrowserCspSmokeError, match="npx is required"):
        browser_csp.run_browser_csp_smoke("http://127.0.0.1:8765")


def test_ci_optional_browser_csp_wrapper_is_explicit_opt_in() -> None:
    script = CI_OPTIONAL_SCRIPT_PATH.read_text(encoding="utf-8")

    assert "KORA_STUDIO_BROWSER_CSP_SMOKE" in script
    assert 'KORA_STUDIO_BROWSER_CSP_SMOKE:-}" != "1"' in script
    assert "python3 -m kora studio --no-browser" in script
    assert "python3 scripts/check_kora_studio_browser_csp.py" in script
    assert "npm install" not in script
    assert "playwright install" not in script
    assert "package.json" not in script
