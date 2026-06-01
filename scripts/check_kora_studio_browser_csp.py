#!/usr/bin/env python3
"""Optional browser-level CSP smoke check for the local KORA Studio preview."""

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


class BrowserCspSmokeError(RuntimeError):
    """Raised when the browser CSP smoke check cannot run or fails."""


def _normalise_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def _require_local_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise BrowserCspSmokeError("KORA Studio browser CSP smoke only accepts http://127.0.0.1 or http://localhost URLs.")


def _build_playwright_spec() -> str:
    return textwrap.dedent(
        r"""
        const { test, expect } = require("playwright/test");

        const baseUrl = process.env.KORA_STUDIO_BROWSER_BASE_URL;
        const expectedCsp = "default-src 'none'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; form-action 'none'; style-src 'self'; script-src 'self'; connect-src 'self'";

        test("KORA Studio local preview works under CSP", async ({ page }) => {
          const cspViolations = [];
          const pageErrors = [];
          const failedRequests = [];
          const assetResponses = new Map();

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
          page.on("response", (response) => {
            const url = response.url();
            if (url === `${baseUrl}/studio-assets/studio.css` || url === `${baseUrl}/studio-assets/studio.js`) {
              assetResponses.set(url, {
                status: response.status(),
                headers: response.headers(),
              });
            }
          });

          const response = await page.goto(`${baseUrl}/`, { waitUntil: "domcontentloaded" });
          expect(response, "root response").not.toBeNull();
          expect(response.status(), "root HTTP status").toBe(200);
          expect(response.headers()["content-security-policy"], "root CSP header").toBe(expectedCsp);

          await expect(page.locator(".studio-shell")).toBeVisible();
          await expect(page.locator("#kora-composer-run-local-harness-button")).toBeVisible();
          await expect(page.locator("[data-kora-request-id]").first()).toBeAttached();
          await page.waitForFunction(() => window.koraStudioScriptStatus?.status === "ready");

          const cssResponse = assetResponses.get(`${baseUrl}/studio-assets/studio.css`);
          const jsResponse = assetResponses.get(`${baseUrl}/studio-assets/studio.js`);
          expect(cssResponse?.status, "CSS asset status").toBe(200);
          expect(jsResponse?.status, "JavaScript asset status").toBe(200);
          expect(cssResponse?.headers["content-type"], "CSS content type").toContain("text/css");
          expect(jsResponse?.headers["content-type"], "JavaScript content type").toContain("application/javascript");

          await page.locator("#kora-composer-run-local-harness-button").click();
          await page.waitForFunction(() => window.koraStudioSelectedRunState?.selected_run_id);
          await expect(page.locator("#kora-selected-run-state")).toContainText("completed");
          await expect(page.locator("#kora-sse-status")).not.toHaveText("idle");

          expect(cspViolations, "browser CSP violations").toEqual([]);
          expect(pageErrors, "page errors").toEqual([]);
          expect(failedRequests, "failed same-origin requests").toEqual([]);
        });
        """
    ).strip()


def run_browser_csp_smoke(
    base_url: str = DEFAULT_BASE_URL,
    *,
    browser: str = DEFAULT_BROWSER,
    timeout: int = 15000,
) -> list[str]:
    """Run the optional Playwright browser CSP smoke check."""

    base_url = _normalise_base_url(base_url)
    _require_local_url(base_url)
    if shutil.which("npx") is None:
        raise BrowserCspSmokeError("npx is required for the optional browser CSP smoke check.")

    repo_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="_kora_studio_browser_csp_", dir=repo_root / "tests") as tmp_dir:
        spec_path = Path(tmp_dir) / "kora_studio_browser_csp.spec.js"
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
            raise BrowserCspSmokeError(output or "Unable to locate the temporary Playwright package path.")
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
            raise BrowserCspSmokeError(output or f"Playwright exited with status {completed.returncode}")
    return [
        "/ browser root ok",
        "/ browser CSP header ok",
        "/ browser local CSS asset ok",
        "/ browser local JavaScript asset ok",
        "/ browser Run Local Harness interaction ok",
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Browser-check an already-running local KORA Studio preview under CSP.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--browser", default=DEFAULT_BROWSER)
    parser.add_argument("--timeout", type=int, default=15000)
    args = parser.parse_args(argv)
    try:
        results = run_browser_csp_smoke(args.base_url, browser=args.browser, timeout=args.timeout)
    except BrowserCspSmokeError as exc:
        print(f"KORA Studio browser CSP smoke check failed: {exc}", file=sys.stderr)
        return 1
    print("KORA Studio browser CSP smoke check passed.")
    for result in results:
        print(f"- {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
