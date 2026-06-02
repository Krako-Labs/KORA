from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_kora_studio_browser_keyboard.py"
CI_OPTIONAL_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_kora_studio_browser_keyboard_ci_optional.sh"
SPEC = importlib.util.spec_from_file_location("check_kora_studio_browser_keyboard", SCRIPT_PATH)
assert SPEC is not None
browser_keyboard = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(browser_keyboard)


def test_browser_keyboard_smoke_rejects_non_local_urls() -> None:
    with pytest.raises(browser_keyboard.BrowserKeyboardSmokeError):
        browser_keyboard.run_browser_keyboard_smoke("https://example.com")


def test_browser_keyboard_smoke_spec_uses_selector_contract_and_stable_assertions() -> None:
    spec = browser_keyboard._build_playwright_spec()

    assert 'data-kora-keyboard-selector-contract="v4.2"' in spec
    assert 'data-kora-keyboard-contract="model-selector"' in spec
    assert 'data-kora-keyboard-contract="approved-request-option"' in spec
    assert 'data-kora-keyboard-contract="primary-run-local-harness"' in spec
    assert 'data-kora-keyboard-contract="run-progress-summary"' in spec
    assert 'data-kora-keyboard-contract="primary-result-summary"' in spec
    assert 'data-kora-keyboard-contract="shell-retry-last-approved-request"' in spec
    assert 'data-kora-keyboard-contract="mobile-rail-toggle"' in spec
    assert 'data-kora-keyboard-contract="mobile-left-rail"' in spec
    assert 'data-kora-keyboard-contract="mobile-rail-close"' in spec
    assert 'data-kora-keyboard-contract="details-drawer-toggle"' in spec
    assert 'data-kora-keyboard-contract="details-drawer"' in spec
    assert 'data-kora-keyboard-contract="details-drawer-close"' in spec
    assert "koraStudioScriptStatus" in spec
    assert "koraStudioSelectedRunState" in spec
    assert 'page.keyboard.press("Enter")' in spec
    assert 'page.keyboard.press("Escape")' in spec
    assert "setViewportSize" in spec
    assert "390" in spec
    assert "844" in spec
    assert "toBeFocused" in spec
    assert "toHaveAttribute" in spec
    assert "toBeAttached" in spec
    assert "Content Security Policy" in spec
    assert "page.keyboard.press(\"Tab\")" not in spec
    assert "unsafe-inline" not in spec
    assert "unsafe-eval" not in spec
    assert "https://" not in spec


def test_browser_keyboard_smoke_invokes_playwright_without_repo_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append({"command": command, **kwargs})
        if "node" in command:
            return SimpleNamespace(returncode=0, stdout="/tmp/npm-cache/_npx/example/node_modules\n", stderr="")
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(browser_keyboard.shutil, "which", lambda name: "/usr/bin/npx" if name == "npx" else None)
    monkeypatch.setattr(browser_keyboard.subprocess, "run", fake_run)

    results = browser_keyboard.run_browser_keyboard_smoke("http://127.0.0.1:8765/", browser="chromium", timeout=1234)

    assert "/ browser keyboard selector contract ok" in results
    assert "/ browser keyboard approved request state ok" in results
    assert "/ browser keyboard bounded retry state ok" in results
    assert "/ browser keyboard details drawer focus return ok" in results
    assert "/ browser keyboard mobile rail focus return ok" in results
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


def test_browser_keyboard_smoke_reports_missing_npx(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(browser_keyboard.shutil, "which", lambda name: None)

    with pytest.raises(browser_keyboard.BrowserKeyboardSmokeError, match="npx is required"):
        browser_keyboard.run_browser_keyboard_smoke("http://127.0.0.1:8765")


def test_ci_optional_browser_keyboard_wrapper_is_explicit_opt_in() -> None:
    script = CI_OPTIONAL_SCRIPT_PATH.read_text(encoding="utf-8")

    assert "KORA_STUDIO_BROWSER_KEYBOARD_SMOKE" in script
    assert 'KORA_STUDIO_BROWSER_KEYBOARD_SMOKE:-}" != "1"' in script
    assert "python3 -m kora studio --no-browser" in script
    assert "python3 scripts/check_kora_studio_browser_keyboard.py" in script
    assert "npm install" not in script
    assert "playwright install" not in script
    assert "package.json" not in script
