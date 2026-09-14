/* Read-only projection of one explicitly configured local evidence record. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const show = (id, value) => { $(id).textContent = String(value); };
  const dl = (id, values) => {
    const nodes = [];
    for (const [key, value] of Object.entries(values)) {
      const dt = document.createElement("dt");
      const dd = document.createElement("dd");
      dt.textContent = key.replaceAll("_", " ");
      dd.textContent = value === null || value === undefined ? "not measured" : String(value);
      nodes.push(dt, dd);
    }
    $(id).replaceChildren(...nodes);
  };
  fetch("/api/hero/live", {cache: "no-store"})
    .then(response => {
      if (!response.ok) throw new Error("Local evidence request failed (" + response.status + ").");
      return response.json();
    })
    .then(data => {
      show("boundary", data.claim_boundary);
      if (!data.available) {
        show("status", "Not configured");
        show("recorded", "Set KORA_HERO_LIVE_EVIDENCE_PATH to one retained record.");
        show("calls", "0");
        show("providers", "0");
        show("cleanup", "Not started");
        show("window", "No live run loaded");
        show("quality", "No evidence configured");
        return;
      }
      const accepted = data.verification.accepted_outcome;
      show("status", accepted ? "Objective pass" : "Failed");
      $("status").dataset.state = accepted ? "passed" : "failed";
      show("recorded", data.recorded_at);
      show("calls", data.actual_execution.model_calls);
      show("providers", data.actual_execution.provider_calls);
      show("cleanup", data.cleanup.cleanup_success ? "Verified" : "Failed");
      show("window", data.actual_execution.live_window_ms + " ms bounded window");
      show("quality", "Semantic non-regression: " + data.verification.semantic_non_regression);
      show("output", JSON.stringify(data.output, null, 2));
      dl("control", data.A_workload_control);
      dl("execution", data.B_local_execution);
      show("runtime", JSON.stringify(data.runtime_identity, null, 2));
      show("usage", JSON.stringify({usage:data.usage,effective_config:data.effective_config}, null, 2));
      show("run", "Run · " + data.run_id);
      show("digest", "Planning SHA-256 · " + data.planning_digest);
      show("events", "Ordered events · " + data.event_count);
      window.koraHeroLiveState = data;
    })
    .catch(error => {
      show("status", "Evidence rejected");
      show("error", error.message || error);
      $("error").hidden = false;
    });
})();
