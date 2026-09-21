/* Read-only manual replay of one scrubbed Inference -> Execution evidence record. */
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
  const median = values => {
    if (!Array.isArray(values) || values.length === 0) return "not measured";
    const sorted = values.map(Number).sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
  };

  let evidence = null;
  let visibleStates = 0;
  const controlIds = ["replay-restart", "replay-previous", "replay-next", "replay-final"];

  const renderTimeline = count => {
    if (!evidence || !evidence.available) return;
    const timeline = evidence.event_timeline;
    visibleStates = Math.max(1, Math.min(Number(count), timeline.length));
    const visible = timeline.slice(0, visibleStates);
    const stateNodes = visible.map(item => {
      const li = document.createElement("li");
      li.textContent = item.state;
      li.title = "Actual event " + item.sequence + ": " + item.event;
      return li;
    });
    $("states").replaceChildren(...stateNodes);
    const current = visible[visible.length - 1];
    show(
      "replay-position",
      (visibleStates === timeline.length ? "Final" : "Step " + visibleStates + " of " + timeline.length) +
        " · actual event " + current.sequence + " of " + evidence.event_count
    );
    show("replay-current", current.event + " → " + current.state);
    $("replay-previous").disabled = visibleStates <= 1;
    $("replay-next").disabled = visibleStates >= timeline.length;
    $("replay-final").disabled = visibleStates >= timeline.length;
  };

  const setReplayDisabled = disabled => {
    for (const id of controlIds) $(id).disabled = disabled;
  };

  const render = data => {
    evidence = data;
    show("boundary", data.claim_boundary);
    if (!data.available) {
      show("status", "Not configured");
      show("recorded", "Set KORA_INFERENCE_EXECUTION_EVIDENCE_PATH to one scrubbed observed record.");
      show("model-calls", "0");
      show("compiled", "0");
      show("reuse", "0");
      show("replay-position", "No evidence configured");
      show("replay-current", "Read-only replay is unavailable.");
      setReplayDisabled(true);
      return;
    }

    show("status", "Objective pass");
    show("recorded", data.recorded_at);
    show("model-calls", data.model_accounting.calls);
    show("tokens", data.model_accounting.input_tokens + " in · " + data.model_accounting.output_tokens + " out");
    show("compiled", data.counters.compiled_executions);
    show("reuse", data.counters.exact_reuse_hits);
    show("lane-model", data.model_accounting.calls + " observed model calls");
    show("lane-kora", data.counters.compiled_executions + " compiled executions · exact reuse " + data.counters.exact_reuse_hits);
    show("lane-ood", data.counters.unknown_or_ood_escalations + " escalations · " + data.counters.safe_pauses + " safe pause");
    show("event-count", data.event_count + " ordered events · " + data.event_timeline.length + " projected states");
    dl("candidate", {
      digest: data.candidate.digest,
      automatic_from_live_observations: data.candidate.automatic_from_live_observations,
      deterministic_repeat_equal: data.candidate.deterministic_repeat_equal,
      activation_passed: data.activation.passed,
      raw_overlap_count: data.activation.raw_overlap_count,
      normalized_overlap_count: data.activation.normalized_overlap_count,
    });
    dl("safety", {
      ood_silent_deterministic_success: data.counters.ood_silent_deterministic_success,
      unknown_or_ood_escalations: data.counters.unknown_or_ood_escalations,
      safe_pauses: data.counters.safe_pauses,
      exact_reuse_hits: data.counters.exact_reuse_hits,
    });
    show("timings", JSON.stringify({
      model_intelligence_ms: data.timings_ms.model_intelligence,
      model_intelligence_p50_ms: median(data.timings_ms.model_intelligence),
      candidate_generation_ms: data.timings_ms.candidate_generation,
      candidate_validation_ms: data.timings_ms.candidate_validation,
      compiled_execution_ms: data.timings_ms.compiled_execution,
      compiled_execution_p50_ms: median(data.timings_ms.compiled_execution),
      verification_ms: data.timings_ms.verification,
    }, null, 2));
    show("identity", JSON.stringify(data.model_identity, null, 2));
    show("event-digest", "Event SHA-256 · " + data.event_digest);
    setReplayDisabled(false);
    renderTimeline(data.event_timeline.length);
    window.koraInferenceExecutionState = data;
  };

  const loadEvidence = () => {
    $("evidence-reload").disabled = true;
    $("error").hidden = true;
    return fetch("/api/inference-execution", {cache: "no-store"})
      .then(response => {
        if (!response.ok) throw new Error("Inference → Execution evidence request failed (" + response.status + ").");
        return response.json();
      })
      .then(render)
      .catch(error => {
        show("status", "Evidence rejected");
        show("error", error.message || error);
        $("error").hidden = false;
        setReplayDisabled(true);
      })
      .finally(() => { $("evidence-reload").disabled = false; });
  };

  $("replay-restart").addEventListener("click", () => renderTimeline(1));
  $("replay-previous").addEventListener("click", () => renderTimeline(visibleStates - 1));
  $("replay-next").addEventListener("click", () => renderTimeline(visibleStates + 1));
  $("replay-final").addEventListener("click", () => renderTimeline(evidence.event_timeline.length));
  $("evidence-reload").addEventListener("click", loadEvidence);
  setReplayDisabled(true);
  loadEvidence();
})();
