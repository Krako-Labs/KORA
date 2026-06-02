#!/usr/bin/env python3
"""Optional browser-level keyboard smoke check for the local KORA Studio preview."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_BASE_URL = "http://127.0.0.1:8765"
DEFAULT_BROWSER = "chromium"


class BrowserKeyboardSmokeError(RuntimeError):
    """Raised when the browser keyboard smoke check cannot run or fails."""


def _normalise_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def _require_local_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise BrowserKeyboardSmokeError(
            "KORA Studio browser keyboard smoke only accepts http://127.0.0.1 or http://localhost URLs."
        )


def _build_playwright_spec() -> str:
    return textwrap.dedent(
        r"""
        const { test, expect } = require("playwright/test");

        const baseUrl = process.env.KORA_STUDIO_BROWSER_BASE_URL;

        test("KORA Studio local preview primary keyboard path works", async ({ page }) => {
          const cspViolations = [];
          const pageErrors = [];
          const failedRequests = [];

          page.on("console", (message) => {
            const text = message.text();
            if (message.type() === "error" && /Content Security Policy|Refused to|violates/.test(text)) {
              cspViolations.push(text);
            }
          });
          page.on("pageerror", (error) => {
            pageErrors.push(error.message);
          });
          page.on("requestfailed", (request) => {
            const url = request.url();
            if (url.startsWith(baseUrl)) {
              failedRequests.push(`${url}: ${request.failure()?.errorText || "request failed"}`);
            }
          });

          const response = await page.goto(`${baseUrl}/`, { waitUntil: "domcontentloaded" });
          expect(response, "root response").not.toBeNull();
          expect(response.status(), "root HTTP status").toBe(200);
          await page.waitForFunction(() => window.koraStudioScriptStatus?.status === "ready");

          const selectorContract = page.locator('[data-kora-keyboard-selector-contract="v4.2"]');
          const modelSelector = page.locator('[data-kora-keyboard-contract="model-selector"]');
          const requestOption = page.locator('[data-kora-keyboard-contract="approved-request-option"]').first();
          const runButton = page.locator('[data-kora-keyboard-contract="primary-run-local-harness"]');
          const retryButton = page.locator('[data-kora-keyboard-contract="shell-retry-last-approved-request"]');
          const runProgress = page.locator('[data-kora-keyboard-contract="run-progress-summary"]');
          const resultSummary = page.locator('[data-kora-keyboard-contract="primary-result-summary"]');
          const detailsToggle = page.locator('[data-kora-keyboard-contract="details-drawer-toggle"]');
          const detailsDrawer = page.locator('[data-kora-keyboard-contract="details-drawer"]');
          const detailsClose = page.locator('[data-kora-keyboard-contract="details-drawer-close"]');

          await expect(selectorContract).toBeAttached();
          await expect(modelSelector).toBeAttached();
          await expect(requestOption).toBeAttached();
          await expect(runButton).toBeVisible();
          await expect(runProgress).toBeVisible();
          await expect(resultSummary).toBeVisible();
          await expect(detailsToggle).toBeVisible();
          await expect(detailsToggle).toHaveAttribute("aria-expanded", "false");
          await expect(retryButton).toBeDisabled();

          await expect(requestOption).toHaveAttribute("aria-pressed", "true");
          await expect(requestOption).toHaveAttribute("aria-current", "true");
          await expect(page.locator("#kora-selected-request-id")).toHaveText(/local-harness-/);

          await runButton.focus();
          await expect(runButton).toBeFocused();
          await page.keyboard.press("Enter");
          await page.waitForFunction(() => window.koraStudioSelectedRunState?.selected_run_id);
          await page.waitForFunction(() => document.querySelector("#kora-primary-result-status")?.textContent === "completed");
          await expect(runProgress).toBeVisible();
          await expect(page.locator("#kora-primary-result-status")).toHaveText("completed");
          await expect(retryButton).toBeAttached();

          await detailsToggle.focus();
          await expect(detailsToggle).toBeFocused();
          await page.keyboard.press("Enter");
          await expect(detailsToggle).toHaveAttribute("aria-expanded", "true");
          await expect(detailsDrawer).toHaveAttribute("data-kora-drawer-state", "open");
          await expect(detailsClose).toBeFocused();
          await page.keyboard.press("Escape");
          await expect(detailsToggle).toHaveAttribute("aria-expanded", "false");
          await expect(detailsDrawer).toHaveAttribute("data-kora-drawer-state", "closed");
          await expect(detailsToggle).toBeFocused();

          expect(cspViolations, "browser CSP violations").toEqual([]);
          expect(pageErrors, "page errors").toEqual([]);
          expect(failedRequests, "failed same-origin requests").toEqual([]);
        });

        test("KORA Studio local preview mobile rail keyboard path works", async ({ page }) => {
          const cspViolations = [];
          const pageErrors = [];
          const failedRequests = [];

          page.on("console", (message) => {
            const text = message.text();
            if (message.type() === "error" && /Content Security Policy|Refused to|violates/.test(text)) {
              cspViolations.push(text);
            }
          });
          page.on("pageerror", (error) => {
            pageErrors.push(error.message);
          });
          page.on("requestfailed", (request) => {
            const url = request.url();
            if (url.startsWith(baseUrl)) {
              failedRequests.push(`${url}: ${request.failure()?.errorText || "request failed"}`);
            }
          });

          await page.setViewportSize({ width: 390, height: 844 });
          const response = await page.goto(`${baseUrl}/`, { waitUntil: "domcontentloaded" });
          expect(response, "root response").not.toBeNull();
          expect(response.status(), "root HTTP status").toBe(200);
          await page.waitForFunction(() => window.koraStudioScriptStatus?.status === "ready");

          const railToggle = page.locator('[data-kora-keyboard-contract="mobile-rail-toggle"]');
          const leftRail = page.locator('[data-kora-keyboard-contract="mobile-left-rail"]');
          const railClose = page.locator('[data-kora-keyboard-contract="mobile-rail-close"]');

          await expect(railToggle).toBeVisible();
          await expect(railToggle).toHaveAttribute("aria-expanded", "false");
          await expect(leftRail).toHaveAttribute("data-kora-rail-state", "closed");
          await expect(leftRail).toHaveAttribute("aria-hidden", "true");

          await railToggle.focus();
          await expect(railToggle).toBeFocused();
          await page.keyboard.press("Enter");
          await expect(railToggle).toHaveAttribute("aria-expanded", "true");
          await expect(leftRail).toHaveAttribute("data-kora-rail-state", "open");
          await expect(leftRail).toHaveAttribute("aria-hidden", "false");
          await expect(railClose).toBeFocused();

          await page.keyboard.press("Escape");
          await expect(railToggle).toHaveAttribute("aria-expanded", "false");
          await expect(leftRail).toHaveAttribute("data-kora-rail-state", "closed");
          await expect(leftRail).toHaveAttribute("aria-hidden", "true");
          await expect(railToggle).toBeFocused();

          expect(cspViolations, "browser CSP violations").toEqual([]);
          expect(pageErrors, "page errors").toEqual([]);
          expect(failedRequests, "failed same-origin requests").toEqual([]);
        });
        """
    ).strip()


def run_browser_keyboard_smoke(
    base_url: str = DEFAULT_BASE_URL,
    *,
    browser: str = DEFAULT_BROWSER,
    timeout: int = 15000,
) -> list[str]:
    """Run the optional Playwright browser keyboard smoke check."""

    base_url = _normalise_base_url(base_url)
    _require_local_url(base_url)
    if shutil.which("npx") is None:
        raise BrowserKeyboardSmokeError("npx is required for the optional browser keyboard smoke check.")

    repo_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="_kora_studio_browser_keyboard_", dir=repo_root / "tests") as tmp_dir:
        spec_path = Path(tmp_dir) / "kora_studio_browser_keyboard.spec.js"
        spec_path.write_text(_build_playwright_spec(), encoding="utf-8")
        env = {"KORA_STUDIO_BROWSER_BASE_URL": base_url, **dict(os.environ)}
        node_path_command = [
            "npx",
            "--yes",
            "--package",
            "@playwright/test",
            "node",
            "-e",
            (
                "const bin = process.env.PATH.split(':')"
                ".find((entry) => entry.includes('/_npx/') && entry.endsWith('/node_modules/.bin'));"
                "if (!bin) process.exit(1);"
                "console.log(bin.replace(/\\/\\.bin$/, ''));"
            ),
        ]
        node_path_result = subprocess.run(
            node_path_command,
            cwd=repo_root,
            env=env,
            text=True,
            capture_output=True,
        )
        if node_path_result.returncode != 0:
            output = "\n".join(part for part in [node_path_result.stdout.strip(), node_path_result.stderr.strip()] if part)
            raise BrowserKeyboardSmokeError(output or "Unable to locate the temporary Playwright package path.")
        env["NODE_PATH"] = node_path_result.stdout.strip()
        command = [
            "npx",
            "--yes",
            "--package",
            "@playwright/test",
            "playwright",
            "test",
            str(spec_path),
            "--browser",
            browser,
            "--reporter",
            "line",
            "--timeout",
            str(timeout),
        ]
        completed = subprocess.run(command, cwd=repo_root, env=env, text=True, capture_output=True)
        if completed.returncode != 0:
            output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
            raise BrowserKeyboardSmokeError(output or f"Playwright exited with status {completed.returncode}")
    return [
        "/ browser keyboard root ok",
        "/ browser keyboard selector contract ok",
        "/ browser keyboard approved request state ok",
        "/ browser keyboard Run Local Harness ok",
        "/ browser keyboard progress and result summaries ok",
        "/ browser keyboard bounded retry state ok",
        "/ browser keyboard details drawer focus return ok",
        "/ browser keyboard mobile rail focus return ok",
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Browser-check an already-running local KORA Studio preview keyboard path.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--browser", default=DEFAULT_BROWSER)
    parser.add_argument("--timeout", type=int, default=15000)
    args = parser.parse_args(argv)
    try:
        results = run_browser_keyboard_smoke(args.base_url, browser=args.browser, timeout=args.timeout)
    except BrowserKeyboardSmokeError as exc:
        print(f"KORA Studio browser keyboard smoke check failed: {exc}", file=sys.stderr)
        return 1
    print("KORA Studio browser keyboard smoke check passed.")
    for result in results:
        print(f"- {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
