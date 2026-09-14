/* Browser QC for the opt-in, read-only Hero live evidence surface. */
const {chromium} = require(process.env.KORA_PLAYWRIGHT_MODULE || "playwright");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const base = process.argv[2] || "http://127.0.0.1:8794";
const output = process.argv[3] || "/tmp/kora-hero-live-browser-qc";
const origin = new URL(base);
assert(
  ["127.0.0.1", "localhost"].includes(origin.hostname) && origin.protocol === "http:",
  "localhost only",
);
fs.mkdirSync(output, {recursive: true});

(async () => {
  const browser = await chromium.launch({headless: true});
  const context = await browser.newContext({viewport: {width: 1440, height: 1080}});
  const page = await context.newPage();
  const errors = [];
  const external = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") errors.push(message.text());
  });
  page.on("request", req => {
    if (new URL(req.url()).origin !== origin.origin) external.push(req.url());
  });

  await page.goto(base + "/hero/live");
  await page.waitForFunction(() => window.koraHeroLiveState?.available === true);
  const state = await page.evaluate(() => window.koraHeroLiveState);
  assert.equal(state.actual_execution.provider_calls, 0);
  assert(state.actual_execution.model_calls >= 1 && state.actual_execution.model_calls <= 3);
  assert.equal(state.runtime_identity.network, "loopback");
  assert.equal(state.verification.semantic_non_regression, "not_measured");
  assert.equal(state.cleanup.cleanup_success, true);
  assert.equal(await page.locator("#status").innerText(), "Objective pass");
  assert.equal(await page.locator("#providers").innerText(), "0");
  assert((await page.locator("#output").innerText()).includes("headline"));
  assert((await page.locator("#boundary").innerText()).includes("not measured"));
  assert.equal(external.length, 0);
  assert.equal(errors.length, 0);

  const api = await (await context.request.get(base + "/api/hero/live")).json();
  assert.deepEqual(api, state);
  await page.screenshot({
    path: path.join(output, "hero-live-evidence.png"),
    fullPage: true,
    animations: "disabled",
  });
  fs.writeFileSync(
    path.join(output, "summary.json"),
    JSON.stringify(
      {
        checks: 10,
        run_id: state.run_id,
        model_calls: state.actual_execution.model_calls,
        provider_calls: state.actual_execution.provider_calls,
        cleanup_success: state.cleanup.cleanup_success,
        unexpected_console_errors: errors,
        external_requests: external,
      },
      null,
      2,
    ) + "\n",
  );
  console.log("Hero live browser QC: 10 checks passed");
  await browser.close();
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
