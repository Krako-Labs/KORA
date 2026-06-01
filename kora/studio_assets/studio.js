(function () {
  window.koraStudioScriptStatus = {status: "booting", error: ""};
  window.addEventListener("error", (event) => {
    window.koraStudioScriptStatus = {status: "failed", error: event.message || "Unknown local preview script error."};
  });
  const dataElement = document.getElementById("kora-approved-requests-data");
  const approvedRequests = JSON.parse(dataElement ? dataElement.textContent || "[]" : "[]");
  const requestById = new Map(approvedRequests.map((request) => [request.request_id, request]));
  let selectedRequestId = approvedRequests.length ? approvedRequests[0].request_id : "";
  let selectedRunId = "";
  let selectedRunEvents = [];
  let selectedRunCounters = {};
  let selectedRunComparison = {};
  let selectedRunReportMetadata = {};
  let runLoading = false;
  let runError = "";
  let lastApprovedRequestId = selectedRequestId;
  let retryAvailable = false;
  let runHistory = [];
  const runHistoryLimit = 5;
  let sseAvailable = typeof EventSource !== "undefined";
  let sseStatus = "idle";
  let sseError = "";
  let sseEvents = [];
  let sseFallbackUsed = false;
  let activeEventSource = null;

  const text = (id, value) => {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = String(value);
    }
  };

  const studioShell = document.querySelector(".studio-shell");
  const leftRail = document.getElementById("kora-left-rail");
  const leftRailToggle = document.getElementById("kora-left-rail-toggle");
  const leftRailClose = document.getElementById("kora-left-rail-close");
  const workspace = document.querySelector(".studio-workspace");
  const detailsDrawer = document.getElementById("kora-details-drawer");
  const detailsDrawerToggle = document.getElementById("kora-details-drawer-toggle");
  const detailsDrawerClose = document.getElementById("kora-details-drawer-close");

  const isSmallRailViewport = () => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
      return false;
    }
    return window.matchMedia("(max-width: 760px)").matches;
  };

  const setLeftRailOpen = (open, options) => {
    const shouldOpen = open === true;
    const shouldHideRail = !shouldOpen && isSmallRailViewport();
    if (studioShell) {
      studioShell.setAttribute("data-kora-rail-open", shouldOpen ? "true" : "false");
    }
    if (leftRail) {
      leftRail.setAttribute("data-kora-rail-state", shouldOpen ? "open" : "closed");
      leftRail.setAttribute("aria-hidden", shouldHideRail ? "true" : "false");
      if (shouldHideRail) {
        leftRail.setAttribute("inert", "");
      } else {
        leftRail.removeAttribute("inert");
      }
    }
    if (leftRailToggle) {
      leftRailToggle.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
      leftRailToggle.setAttribute("aria-label", shouldOpen ? "Close left rail" : "Open left rail");
    }
    const shouldManageFocus = !options || options.manageFocus !== false;
    if (shouldManageFocus && shouldOpen && leftRailClose) {
      leftRailClose.focus();
    }
    if (shouldManageFocus && !shouldOpen && leftRailToggle) {
      leftRailToggle.focus();
    }
  };

  if (leftRailToggle) {
    leftRailToggle.addEventListener("click", () => {
      const isOpen = leftRailToggle.getAttribute("aria-expanded") === "true";
      setLeftRailOpen(!isOpen);
    });
  }
  if (leftRailClose) {
    leftRailClose.addEventListener("click", () => {
      setLeftRailOpen(false);
    });
  }
  if (typeof window !== "undefined") {
    window.addEventListener("resize", () => {
      const isOpen = leftRailToggle && leftRailToggle.getAttribute("aria-expanded") === "true";
      setLeftRailOpen(isOpen, {manageFocus: false});
    });
  }

  const setDetailsDrawerOpen = (open, options) => {
    const shouldOpen = open === true;
    if (workspace) {
      workspace.setAttribute("data-kora-drawer-open", shouldOpen ? "true" : "false");
    }
    if (detailsDrawer) {
      detailsDrawer.setAttribute("data-kora-drawer-state", shouldOpen ? "open" : "closed");
      detailsDrawer.setAttribute("aria-hidden", shouldOpen ? "false" : "true");
      if (shouldOpen) {
        detailsDrawer.removeAttribute("inert");
      } else {
        detailsDrawer.setAttribute("inert", "");
      }
    }
    if (detailsDrawerToggle) {
      detailsDrawerToggle.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
      detailsDrawerToggle.setAttribute("aria-label", shouldOpen ? "Close details drawer" : "Open details drawer");
    }
    const shouldManageFocus = !options || options.manageFocus !== false;
    if (shouldManageFocus && shouldOpen && detailsDrawerClose) {
      detailsDrawerClose.focus();
    }
    if (shouldManageFocus && !shouldOpen && detailsDrawerToggle) {
      detailsDrawerToggle.focus();
    }
  };

  if (detailsDrawerToggle) {
    detailsDrawerToggle.addEventListener("click", () => {
      const isOpen = detailsDrawerToggle.getAttribute("aria-expanded") === "true";
      setDetailsDrawerOpen(!isOpen);
    });
  }
  if (detailsDrawerClose) {
    detailsDrawerClose.addEventListener("click", () => {
      setDetailsDrawerOpen(false);
    });
  }
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && leftRail && leftRail.getAttribute("data-kora-rail-state") === "open") {
      setLeftRailOpen(false);
    }
    if (event.key === "Escape" && detailsDrawer && detailsDrawer.getAttribute("data-kora-drawer-state") === "open") {
      setDetailsDrawerOpen(false);
    }
  });
  setLeftRailOpen(false, {manageFocus: false});
  setDetailsDrawerOpen(false, {manageFocus: false});

  const setButtonState = () => {
    document.querySelectorAll("[data-kora-request-id]").forEach((button) => {
      const isSelected = button.getAttribute("data-kora-request-id") === selectedRequestId;
      button.setAttribute("aria-pressed", isSelected ? "true" : "false");
      button.setAttribute("aria-current", isSelected ? "true" : "false");
    });
  };

  const setRetryState = (available, message) => {
    retryAvailable = available === true && requestById.has(lastApprovedRequestId);
    text("kora-run-error-state", message || "No selected-run error.");
    text("kora-shell-retry-guidance", message || "No retry needed. Select an approved request, run Local Harness, or inspect diagnostics if a run fails.");
    text("kora-last-approved-request-id", lastApprovedRequestId || "none");
    text("kora-retry-available", retryAvailable ? "true" : "false");
    document.querySelectorAll("[data-kora-retry-last-approved-request-button]").forEach((retryButton) => {
      retryButton.disabled = !retryAvailable || runLoading;
    });
  };

  const setRunLoading = (loading) => {
    runLoading = loading === true;
    const runButton = document.getElementById("kora-run-local-harness-button");
    const composerRunButton = document.getElementById("kora-composer-run-local-harness-button");
    if (runButton) {
      runButton.disabled = runLoading;
    }
    if (composerRunButton) {
      composerRunButton.disabled = runLoading;
    }
    document.querySelectorAll("[data-kora-retry-last-approved-request-button]").forEach((retryButton) => {
      retryButton.disabled = runLoading || !retryAvailable;
    });
  };

  const setSseState = (status, error, fallbackUsed) => {
    sseStatus = status || "idle";
    sseError = error || "";
    if (fallbackUsed !== undefined) {
      sseFallbackUsed = fallbackUsed === true;
    }
    text("kora-sse-status", sseStatus);
    text("kora-sse-error", sseError || "No generated event stream error.");
    text("kora-sse-fallback-used", sseFallbackUsed ? "true" : "false");
    const streamMessages = {
      idle: "Generated event stream idle",
      connecting: "Connecting to generated event stream",
      streaming: "Receiving generated events",
      completed: "Generated event stream completed",
      fallback: "Using local events endpoint fallback"
    };
    const eventMessages = {
      connecting: "Waiting for generated events",
      streaming: "Generated events received",
      completed: "Generated events complete",
      fallback: "Generated events loaded by fallback"
    };
    setRunProgressSummary({
      event_status: eventMessages[sseStatus],
      stream_status: streamMessages[sseStatus] || sseStatus,
      error: sseError || "No run error. Generated event stream is local harness events only, not model token streaming or provider output."
    });
  };

  const closeActiveEventSource = () => {
    if (activeEventSource) {
      activeEventSource.close();
      activeEventSource = null;
    }
  };

  const setShellSelectedRunSurfaceState = (updates) => {
    const state = updates || {};
    if (state.run_id !== undefined) {
      text("kora-drawer-selected-run-id", state.run_id || "not run yet");
    }
    if (state.timeline !== undefined) {
      text("kora-shell-selected-timeline-status", state.timeline);
      text("kora-drawer-selected-timeline-status", state.timeline);
    }
    if (state.counters !== undefined) {
      text("kora-shell-selected-counters-status", state.counters);
      text("kora-drawer-selected-counters-status", state.counters);
    }
    if (state.comparison !== undefined) {
      text("kora-shell-selected-comparison-status", state.comparison);
      text("kora-drawer-selected-comparison-status", state.comparison);
    }
    if (state.report !== undefined) {
      text("kora-shell-selected-report-status", state.report);
      text("kora-drawer-selected-report-status", state.report);
    }
  };

  const setPrimaryResultSummary = (updates) => {
    const state = updates || {};
    if (state.request_id !== undefined) {
      text("kora-primary-result-request-id", state.request_id || "none");
    }
    if (state.run_id !== undefined) {
      text("kora-primary-result-run-id", state.run_id || "not run yet");
    }
    if (state.status !== undefined) {
      text("kora-primary-result-status", state.status || "not_started");
    }
    if (state.event_count !== undefined) {
      text("kora-primary-result-event-count", state.event_count);
    }
    if (state.avoided_model_calls !== undefined) {
      text("kora-primary-result-avoided-model-calls", state.avoided_model_calls);
    }
    if (state.deterministic_routes !== undefined) {
      text("kora-primary-result-deterministic-routes", state.deterministic_routes);
    }
    if (state.comparison_status !== undefined) {
      text("kora-primary-result-comparison-status", state.comparison_status || "not loaded");
    }
    if (state.report_status !== undefined) {
      text("kora-primary-result-report-status", state.report_status || "not loaded");
    }
    if (state.boundary !== undefined) {
      text("kora-primary-result-boundary", state.boundary || "Generated local harness output only. Not production telemetry, not production cost evidence, no model execution, no provider calls, no report export, and no file writing.");
    }
  };

  const setRunProgressSummary = (updates) => {
    const state = updates || {};
    if (state.state !== undefined) {
      text("kora-run-progress-state", state.state || "idle");
    }
    if (state.step !== undefined) {
      text("kora-run-progress-step", state.step || "No run selected");
    }
    if (state.event_status !== undefined) {
      text("kora-run-progress-event-status", state.event_status || "No generated events yet");
    }
    if (state.stream_status !== undefined) {
      text("kora-run-progress-stream-status", state.stream_status || "Generated event stream idle");
    }
    if (state.error !== undefined) {
      text("kora-run-progress-error", state.error || "No run error. Generated event stream is local harness events only, not model token streaming or provider output.");
    }
  };

  const getShellAccessibilityState = () => {
    return {
      left_rail_state: leftRail ? leftRail.getAttribute("data-kora-rail-state") : "missing",
      left_rail_expanded: leftRailToggle ? leftRailToggle.getAttribute("aria-expanded") : "missing",
      left_rail_inert: leftRail ? leftRail.hasAttribute("inert") : "missing",
      details_drawer_state: detailsDrawer ? detailsDrawer.getAttribute("data-kora-drawer-state") : "missing",
      details_drawer_expanded: detailsDrawerToggle ? detailsDrawerToggle.getAttribute("aria-expanded") : "missing",
      details_drawer_inert: detailsDrawer ? detailsDrawer.hasAttribute("inert") : "missing",
      model_selector_state: document.querySelector("[data-kora-model-selector]") ? document.querySelector("[data-kora-model-selector]").getAttribute("data-kora-model-selection-state") : "missing",
      selected_request_id: selectedRequestId || "none",
      keyboard_focus_pass: studioShell ? studioShell.getAttribute("data-kora-keyboard-focus-pass") : "missing"
    };
  };

  const renderSelectedRequest = () => {
    const request = requestById.get(selectedRequestId);
    if (!request) {
      text("kora-selected-request-id", "none");
      text("kora-composer-request-id", "none");
      setPrimaryResultSummary({request_id: "none"});
      text("kora-selected-request-text", "No approved request selected.");
      text("kora-selected-request-route", "unknown");
      text("kora-selected-request-model-needed", "unknown");
      return;
    }
    text("kora-selected-request-id", request.request_id);
    text("kora-composer-request-id", request.request_id);
    setPrimaryResultSummary({request_id: request.request_id});
    text("kora-selected-request-text", request.input_text || "Approved local sample request.");
    text("kora-selected-request-route", request.expected_route_class || "unknown");
    text("kora-selected-request-model-needed", request.expected_model_needed === true ? "true" : "false");
    setButtonState();
  };

  const renderRunError = (message) => {
    runError = message || "Local harness run failed.";
    text("kora-run-status", "failed");
    text("kora-composer-run-status", "failed");
    text("kora-composer-run-id", "not available");
    setRunProgressSummary({
      state: "failed",
      step: "Run failed",
      event_status: "Generated events unavailable",
      stream_status: "Generated event stream stopped",
      error: `${runError} No model execution was attempted. Provider calls remain disabled.`
    });
    setPrimaryResultSummary({
      run_id: "not available",
      status: "failed",
      comparison_status: "unavailable",
      report_status: "unavailable",
      boundary: `${runError} No model execution was attempted. Provider calls remain disabled. Retry uses the last approved request only.`
    });
    text("kora-run-claim-boundary", `${runError} No model execution was attempted. Provider calls remain disabled. Try again or inspect the local server logs.`);
    setRetryState(true, `${runError} Retry uses the last approved request only. No model execution was attempted. Provider calls remain disabled.`);
    renderCountersUnavailable("Selected-run counters unavailable.");
    renderComparisonUnavailable("Selected-run comparison unavailable.");
    renderReportMetadataUnavailable("Selected-run report metadata unavailable.");
    setShellSelectedRunSurfaceState({
      run_id: "not available",
      timeline: "unavailable",
      counters: "unavailable",
      comparison: "unavailable",
      report: "unavailable"
    });
  };

  const renderEventError = (message) => {
    selectedRunEvents = [];
    runError = message || "Generated events unavailable for this local run.";
    text("kora-selected-events-status", `${runError} No model execution was attempted. Provider calls remain disabled.`);
    setRunProgressSummary({
      state: "failed",
      step: "Generated events unavailable",
      event_status: "Generated events unavailable",
      stream_status: "Using local events endpoint fallback failed",
      error: `${runError} No model execution was attempted. Provider calls remain disabled.`
    });
    setRetryState(true, `${runError} Retry uses the last approved request only. No model execution was attempted. Provider calls remain disabled.`);
    const container = document.getElementById("kora-selected-run-events");
    if (container) {
      container.replaceChildren();
    }
    setShellSelectedRunSurfaceState({timeline: "unavailable"});
  };

  const clearSelectedCards = (id) => {
    const container = document.getElementById(id);
    if (container) {
      container.replaceChildren();
    }
  };

  const renderCountersUnavailable = (message) => {
    selectedRunCounters = {};
    text("kora-selected-counters-status", `${message} Generated local harness output only. No model execution. No provider calls.`);
    clearSelectedCards("kora-selected-run-counters");
    setShellSelectedRunSurfaceState({counters: "unavailable"});
  };

  const renderComparisonUnavailable = (message) => {
    selectedRunComparison = {};
    text("kora-selected-comparison-status", `${message} This is not production cost evidence. No model execution. No provider calls.`);
    clearSelectedCards("kora-selected-run-comparison");
    setShellSelectedRunSurfaceState({comparison: "unavailable"});
  };

  const renderReportMetadataUnavailable = (message) => {
    selectedRunReportMetadata = {};
    text("kora-selected-report-status", `${message} Report metadata preview only. No file export. No file writing.`);
    clearSelectedCards("kora-selected-run-report-metadata");
    setShellSelectedRunSurfaceState({report: "unavailable"});
  };

  const renderSelectedCounters = (counters, eventCount) => {
    selectedRunCounters = counters && typeof counters === "object" ? counters : {};
    const container = document.getElementById("kora-selected-run-counters");
    if (!container) {
      return;
    }
    container.replaceChildren();
    const counterKeys = [
      "total_requests",
      "baseline_model_calls",
      "kora_model_calls",
      "avoided_model_calls",
      "deterministic_routes",
      "model_escalations",
      "validation_pass_count",
      "validation_fail_count"
    ];
    if (!Object.keys(selectedRunCounters).length) {
      renderCountersUnavailable("Selected-run counters unavailable.");
      return;
    }
    text("kora-selected-counters-status", "Selected-run counters loaded from generated local harness output. Not production telemetry.");
    setShellSelectedRunSurfaceState({counters: "loaded from selected run"});
    counterKeys.concat(["event_count"]).forEach((key) => {
      const value = key === "event_count" ? eventCount : selectedRunCounters[key];
      const card = document.createElement("div");
      card.className = "card";
      const title = document.createElement("h3");
      title.textContent = key;
      const number = document.createElement("p");
      number.className = "status-value";
      number.textContent = String(value === undefined ? 0 : value);
      const note = document.createElement("p");
      note.textContent = "Generated local harness counters only. No cost or energy claim.";
      card.appendChild(title);
      card.appendChild(number);
      card.appendChild(note);
      container.appendChild(card);
    });
  };

  const renderSelectedComparison = (comparison, modelExecutionStatus) => {
    selectedRunComparison = comparison && typeof comparison === "object" ? comparison : {};
    const container = document.getElementById("kora-selected-run-comparison");
    if (!container) {
      return;
    }
    container.replaceChildren();
    const metrics = selectedRunComparison.metrics || selectedRunComparison.comparison_counters || {};
    const comparisonFields = [
      ["comparison_status", selectedRunComparison.comparison_status || "unknown"],
      ["baseline_model_calls", metrics.baseline_model_calls],
      ["kora_model_calls", metrics.kora_model_calls],
      ["avoided_model_calls", metrics.avoided_model_calls],
      ["model_escalations", metrics.model_escalations],
      ["deterministic_routes", metrics.deterministic_routes],
      ["model_execution_status", modelExecutionStatus || "execution_not_connected"]
    ];
    if (!Object.keys(selectedRunComparison).length) {
      renderComparisonUnavailable("Selected-run comparison unavailable.");
      return;
    }
    text("kora-selected-comparison-status", "Selected-run comparison loaded from approved local harness output. Not production cost evidence.");
    setShellSelectedRunSurfaceState({comparison: "loaded from selected run"});
    comparisonFields.forEach(([label, value]) => {
      const card = document.createElement("div");
      card.className = "card";
      const title = document.createElement("h3");
      title.textContent = label;
      const display = document.createElement("p");
      display.className = "status-value";
      display.textContent = String(value === undefined ? 0 : value);
      const note = document.createElement("p");
      note.textContent = "Comparison is generated from approved local harness output. This does not execute a model.";
      card.appendChild(title);
      card.appendChild(display);
      card.appendChild(note);
      container.appendChild(card);
    });
  };

  const renderSelectedReportMetadata = (report) => {
    selectedRunReportMetadata = report && typeof report === "object" ? report : {};
    const container = document.getElementById("kora-selected-run-report-metadata");
    if (!container) {
      return;
    }
    container.replaceChildren();
    if (!Object.keys(selectedRunReportMetadata).length) {
      renderReportMetadataUnavailable("Selected-run report metadata unavailable.");
      return;
    }
    text("kora-selected-report-status", "Selected-run report metadata loaded. Report metadata preview only. Not production evidence.");
    setShellSelectedRunSurfaceState({report: "preview loaded from selected run"});
    const fields = [
      ["report_status", selectedRunReportMetadata.report_status || selectedRunReportMetadata.report_viewer_status || "unknown"],
      ["report_source", selectedRunReportMetadata.report_source || "local_harness_summary"],
      ["run_id", selectedRunReportMetadata.run_id || selectedRunId || "unknown"],
      ["request_id", selectedRunReportMetadata.request_id || selectedRequestId || "unknown"],
      ["generated_at", selectedRunReportMetadata.generated_at || selectedRunReportMetadata.created_at || "unknown"],
      ["event_count", selectedRunReportMetadata.event_count === undefined ? 0 : selectedRunReportMetadata.event_count],
      ["counter_summary_status", selectedRunReportMetadata.counter_summary ? "available" : "not_available"],
      ["comparison_summary_status", selectedRunReportMetadata.comparison_summary_status || "unknown"],
      ["model_execution_status", selectedRunReportMetadata.model_execution_status || "execution_not_connected"],
      ["provider_calls_enabled", selectedRunReportMetadata.provider_calls_enabled === true ? "true" : "false"],
      ["cloud_sync_enabled", selectedRunReportMetadata.cloud_sync_enabled === true ? "true" : "false"],
      ["file_export_enabled", selectedRunReportMetadata.file_export_enabled === true ? "true" : "false"],
      ["file_written", selectedRunReportMetadata.file_written === true ? "true" : "false"]
    ];
    fields.forEach(([label, value]) => {
      const card = document.createElement("div");
      card.className = "card";
      const title = document.createElement("h3");
      title.textContent = label;
      const display = document.createElement("p");
      display.className = "status-value";
      display.textContent = String(value);
      const note = document.createElement("p");
      note.textContent = "Report metadata preview only. No file export. No file writing.";
      card.appendChild(title);
      card.appendChild(display);
      card.appendChild(note);
      container.appendChild(card);
    });
    const boundaryCard = document.createElement("div");
    boundaryCard.className = "card";
    const title = document.createElement("h3");
    title.textContent = "Report claim boundary";
    const boundary = document.createElement("p");
    boundary.textContent = selectedRunReportMetadata.claim_boundary || "Local deterministic harness output only. No model execution. No provider calls. No cloud sync. Not production evidence.";
    const noExport = document.createElement("p");
    noExport.textContent = "No file export. No file writing. No downloads.";
    boundaryCard.appendChild(title);
    boundaryCard.appendChild(boundary);
    boundaryCard.appendChild(noExport);
    container.appendChild(boundaryCard);
  };

  const renderSelectedEvents = (events) => {
    selectedRunEvents = Array.isArray(events) ? events : [];
    const container = document.getElementById("kora-selected-run-events");
    if (!container) {
      return;
    }
    container.replaceChildren();
    if (!selectedRunEvents.length) {
      text("kora-selected-events-status", "Generated events unavailable for this local run. No model execution was attempted. Provider calls remain disabled.");
      setShellSelectedRunSurfaceState({timeline: "unavailable"});
      return;
    }
    text("kora-selected-events-status", `Loaded ${selectedRunEvents.length} generated local harness events for the selected run.`);
    setRunProgressSummary({
      state: "completed",
      step: "Generated events received",
      event_status: `${selectedRunEvents.length} generated events loaded`,
      error: "No run error. Generated event stream is local harness events only, not model token streaming or provider output."
    });
    setShellSelectedRunSurfaceState({timeline: `loaded from selected run (${selectedRunEvents.length} events)`});
    selectedRunEvents.forEach((event) => {
      const card = document.createElement("div");
      card.className = "card";
      const fields = [
        ["Stage", event.stage_id || "unknown"],
        ["Name", event.stage_name || "Unknown stage"],
        ["Route class", event.route_class || "unknown"],
        ["Status", event.status || "unknown"],
        ["Model called", event.model_called === true ? "true" : "false"],
        ["Deterministic route used", event.deterministic_route_used === true ? "true" : "false"],
        ["Validation result", event.validation_result || "not_applicable"],
        ["Latency", `${event.latency_ms || 0} ms`],
        ["Model execution status", event.model_execution_status || "execution_not_connected"]
      ];
      const title = document.createElement("h3");
      title.textContent = event.stage_name || event.stage_id || "Selected run event";
      card.appendChild(title);
      fields.forEach(([label, value]) => {
        const row = document.createElement("p");
        row.textContent = `${label}: ${value}`;
        card.appendChild(row);
      });
      const boundary = document.createElement("p");
      boundary.textContent = "Generated local harness events only. No model execution. No provider output. No downloads.";
      card.appendChild(boundary);
      container.appendChild(card);
    });
  };

  const eventFromSsePayload = (payload) => {
    if (payload && payload.event && typeof payload.event === "object") {
      return payload.event;
    }
    if (!payload || !payload.stage_id) {
      return null;
    }
    return {
      run_id: payload.run_id || selectedRunId,
      request_id: payload.request_id || selectedRequestId,
      stage_id: payload.stage_id,
      stage_name: payload.stage_name || payload.stage_id,
      route_class: payload.route_class || "unknown",
      status: payload.status || "unknown",
      model_called: false,
      deterministic_route_used: false,
      validation_result: "not_applicable",
      latency_ms: 0,
      model_execution_status: "execution_not_connected"
    };
  };

  const renderSseEvents = () => {
    renderSelectedEvents(sseEvents);
    text("kora-selected-events-status", `Loaded ${sseEvents.length} generated harness events from the generated event stream. Not model token streaming. No provider streaming.`);
    setRunProgressSummary({
      state: "running",
      step: "Receiving generated events",
      event_status: `${sseEvents.length} generated events received`,
      stream_status: "Receiving generated events",
      error: "No run error. Generated event stream is local harness events only, not model token streaming or provider output."
    });
    setShellSelectedRunSurfaceState({timeline: `streamed from selected run (${sseEvents.length} events)`});
  };

  const renderRunHistory = () => {
    const container = document.getElementById("kora-local-run-history");
    text("kora-run-history-count", runHistory.length);
    text("kora-active-history-run-id", selectedRunId || "none");
    if (!container) {
      return;
    }
    container.replaceChildren();
    if (!runHistory.length) {
      text("kora-run-history-status", "No browser-local run history yet. Page-memory only. Clears on refresh. No backend records or files are deleted.");
      return;
    }
    text("kora-run-history-status", "Browser-local run history loaded. Active selected run is marked in page memory only. Not production evidence.");
    runHistory.forEach((record) => {
      const isActive = record.run_id === selectedRunId;
      const counters = record.generated_counters || {};
      const card = document.createElement("div");
      card.className = "card";
      if (isActive) {
        card.setAttribute("aria-current", "true");
      }
      const title = document.createElement("h3");
      title.textContent = isActive ? "Active selected local run" : "Recent local run";
      const activeState = document.createElement("p");
      activeState.textContent = `Active selected run: ${isActive ? "true" : "false"}`;
      const runId = document.createElement("p");
      runId.textContent = `Run id: ${record.run_id || "unknown"}`;
      const requestId = document.createElement("p");
      requestId.textContent = `Request id: ${record.request_id || "unknown"}`;
      const status = document.createElement("p");
      status.textContent = `Status: ${record.run_status || "unknown"}`;
      const eventCount = document.createElement("p");
      eventCount.textContent = `Event count: ${record.event_count || 0}`;
      const compactCounters = document.createElement("p");
      compactCounters.textContent = `Compact counters: avoided_model_calls=${counters.avoided_model_calls || 0}, kora_model_calls=${counters.kora_model_calls || 0}, deterministic_routes=${counters.deterministic_routes || 0}, model_escalations=${counters.model_escalations || 0}, validation_pass_count=${counters.validation_pass_count || 0}`;
      const modelStatus = document.createElement("p");
      modelStatus.textContent = `Model execution status: ${record.model_execution_status || "execution_not_connected"}`;
      const createdAt = document.createElement("p");
      createdAt.textContent = `Created at: ${record.created_at || "unknown"}`;
      const completedAt = document.createElement("p");
      completedAt.textContent = `Completed at: ${record.completed_at || "unknown"}`;
      const boundary = document.createElement("p");
      boundary.textContent = "Browser-local history item. Local deterministic harness output only. No model execution, provider calls, downloads, persistence, or cloud sync.";
      const selectButton = document.createElement("button");
      selectButton.className = "action-button";
      selectButton.type = "button";
      selectButton.textContent = "Select run";
      selectButton.setAttribute("data-kora-history-run-id", record.run_id || "");
      if (isActive) {
        selectButton.textContent = "Selected in page";
      }
      selectButton.addEventListener("click", () => {
        selectRunFromHistory(record.run_id || "");
      });
      card.appendChild(title);
      card.appendChild(activeState);
      card.appendChild(runId);
      card.appendChild(requestId);
      card.appendChild(status);
      card.appendChild(eventCount);
      card.appendChild(compactCounters);
      card.appendChild(modelStatus);
      card.appendChild(createdAt);
      card.appendChild(completedAt);
      card.appendChild(boundary);
      card.appendChild(selectButton);
      container.appendChild(card);
    });
  };

  const selectRunFromHistory = (runId) => {
    closeActiveEventSource();
    const record = runHistory.find((item) => item.run_id === runId);
    if (!record) {
      renderRunError("Selected browser-local run was not found.");
      return;
    }
    renderRunResponse(record, {updateHistory: false});
    renderSelectedEvents(record.generated_events || []);
    setSseState("idle", "Selected run restored from browser-local history. Generated stream not connected for restored history item.", false);
    setRetryState(false, "Selected run restored from browser-local page memory.");
    text("kora-run-history-status", "Selected run restored from browser-local page memory. Not production evidence.");
  };

  const addRunToHistory = (run) => {
    if (!run || !run.run_id || run.run_status !== "completed") {
      return;
    }
    runHistory = [run].concat(runHistory.filter((record) => record.run_id !== run.run_id)).slice(0, runHistoryLimit);
    renderRunHistory();
  };

  const clearLocalRunHistory = () => {
    closeActiveEventSource();
    runHistory = [];
    selectedRunId = "";
    selectedRunEvents = [];
    selectedRunCounters = {};
    selectedRunComparison = {};
    selectedRunReportMetadata = {};
    runError = "";
    text("kora-selected-run-id", "not run yet");
    text("kora-run-request-id", "not run yet");
    text("kora-run-status", "not_started");
    text("kora-composer-run-status", "not_started");
    text("kora-run-event-count", "0");
    text("kora-composer-run-id", "not run yet");
    text("kora-composer-request-id", selectedRequestId || "none");
    text("kora-run-model-execution-status", "not_connected");
    text("kora-run-provider-calls-enabled", "false");
    text("kora-run-cloud-sync-enabled", "false");
    text("kora-run-file-export-enabled", "false");
    text("kora-run-claim-boundary", "Cleared browser-local preview state only.");
    setRunProgressSummary({
      state: "idle",
      step: "No run selected",
      event_status: "No generated events yet",
      stream_status: "Generated event stream idle",
      error: "Cleared browser-local preview state only. No backend records, files, report exports, or server endpoints were deleted."
    });
    setPrimaryResultSummary({
      request_id: selectedRequestId || "none",
      run_id: "not run yet",
      status: "not_started",
      event_count: "0",
      avoided_model_calls: "0",
      deterministic_routes: "0",
      comparison_status: "not loaded",
      report_status: "not loaded",
      boundary: "Cleared browser-local preview state only. No backend records, files, report exports, or server endpoints were deleted."
    });
    text("kora-active-history-run-id", "none");
    text("kora-selected-events-status", "No selected run events loaded yet.");
    renderCountersUnavailable("Run an approved local harness request to view selected-run counters.");
    renderComparisonUnavailable("Run an approved local harness request to view selected-run comparison.");
    renderReportMetadataUnavailable("Run an approved local harness request to view selected-run report metadata.");
    clearSelectedCards("kora-selected-run-events");
    setShellSelectedRunSurfaceState({
      run_id: "not run yet",
      timeline: "not loaded",
      counters: "not loaded",
      comparison: "not loaded",
      report: "not loaded"
    });
    setRetryState(false, "Cleared browser-local preview state only.");
    sseEvents = [];
    setSseState("idle", "Cleared browser-local preview state only. No backend records, files, report exports, or server endpoints were deleted.", false);
    renderRunHistory();
  };

  const fetchSelectedEvents = async () => {
    if (!selectedRunId) {
      renderEventError("Generated events unavailable for this local run.");
      return;
    }
    text("kora-selected-events-status", "Loading generated local harness events.");
    try {
      const response = await fetch(`/api/harness/events?run_id=${encodeURIComponent(selectedRunId)}`);
      let payload;
      try {
        payload = await response.json();
      } catch (parseError) {
        throw new Error("The local response could not be parsed.");
      }
      if (!response.ok || payload.ok === false || !Array.isArray(payload.events)) {
        throw new Error(payload.message || "Generated events unavailable for this local run.");
      }
      renderSelectedEvents(payload.events);
    } catch (error) {
      const message = error instanceof TypeError ? "The local harness endpoint was unavailable." : (error && error.message ? error.message : "Generated events unavailable for this local run.");
      renderEventError(message);
    }
  };

  const fetchSelectedEventsFallback = async (message) => {
    sseFallbackUsed = true;
    setSseState("fallback", message || "Generated event stream unavailable; using local events endpoint fallback.", true);
    await fetchSelectedEvents();
  };

  const connectGeneratedEventStream = async () => {
    closeActiveEventSource();
    sseEvents = [];
    sseFallbackUsed = false;
    if (!selectedRunId) {
      await fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
      return;
    }
    if (!sseAvailable) {
      await fetchSelectedEventsFallback("Generated EventSource is unavailable; using local events endpoint fallback.");
      return;
    }
    setSseState("connecting", "Generated harness events only. No model execution was attempted. Provider calls remain disabled.", false);
    try {
      const eventSource = new EventSource(`/api/harness/sse?run_id=${encodeURIComponent(selectedRunId)}`);
      activeEventSource = eventSource;
      eventSource.addEventListener("stream_started", () => {
        if (eventSource !== activeEventSource) {
          return;
        }
        sseEvents = [];
        setSseState("streaming", "Generated harness events only. Not model token streaming. No provider streaming.", false);
      });
      eventSource.addEventListener("harness_stage", (event) => {
        if (eventSource !== activeEventSource) {
          return;
        }
        try {
          const payload = JSON.parse(event.data || "{}");
          const stageEvent = eventFromSsePayload(payload);
          if (!stageEvent) {
            throw new Error("Malformed generated stream event.");
          }
          sseEvents.push(stageEvent);
          renderSseEvents();
        } catch (parseError) {
          closeActiveEventSource();
          fetchSelectedEventsFallback("Generated event stream returned malformed data; using local events endpoint fallback.");
        }
      });
      eventSource.addEventListener("stream_completed", () => {
        if (eventSource !== activeEventSource) {
          return;
        }
        closeActiveEventSource();
        setSseState("completed", "Generated event stream completed. No model execution was attempted. Provider calls remain disabled.", false);
        if (sseEvents.length) {
          renderSseEvents();
        }
      });
      eventSource.onerror = () => {
        if (eventSource !== activeEventSource) {
          return;
        }
        closeActiveEventSource();
        fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
      };
    } catch (error) {
      closeActiveEventSource();
      await fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
    }
  };

  const renderRunResponse = (run, options) => {
    const shouldUpdateHistory = !options || options.updateHistory !== false;
    selectedRunId = run.run_id || "";
    const report = run.report_metadata_summary || {};
    setShellSelectedRunSurfaceState({run_id: selectedRunId || "not returned"});
    text("kora-selected-run-id", selectedRunId || "not returned");
    text("kora-composer-run-id", selectedRunId || "not returned");
    text("kora-run-request-id", run.request_id || selectedRequestId);
    text("kora-composer-request-id", run.request_id || selectedRequestId);
    text("kora-run-status", run.run_status || "unknown");
    text("kora-composer-run-status", run.run_status || "unknown");
    text("kora-run-event-count", run.event_count || (Array.isArray(run.generated_events) ? run.generated_events.length : 0));
    text("kora-run-model-execution-status", run.model_execution_status || "execution_not_connected");
    text("kora-run-provider-calls-enabled", run.provider_calls_enabled === true ? "true" : "false");
    text("kora-run-cloud-sync-enabled", run.cloud_sync_enabled === true ? "true" : "false");
    text("kora-run-file-export-enabled", report.file_export_enabled === true ? "true" : "false");
    text("kora-run-claim-boundary", run.claim_boundary || "Generated local harness output only. No model execution.");
    setRunProgressSummary({
      state: run.run_status || "completed",
      step: "Run response received",
      event_status: `${run.event_count || (Array.isArray(run.generated_events) ? run.generated_events.length : 0)} generated events available`,
      stream_status: "Generated event stream pending",
      error: "No run error. Generated event stream is local harness events only, not model token streaming or provider output."
    });
    const counters = run.generated_counters && typeof run.generated_counters === "object" ? run.generated_counters : {};
    const comparison = run.comparison_summary && typeof run.comparison_summary === "object" ? run.comparison_summary : {};
    setPrimaryResultSummary({
      request_id: run.request_id || selectedRequestId,
      run_id: selectedRunId || "not returned",
      status: run.run_status || "unknown",
      event_count: run.event_count || (Array.isArray(run.generated_events) ? run.generated_events.length : 0),
      avoided_model_calls: counters.avoided_model_calls === undefined ? 0 : counters.avoided_model_calls,
      deterministic_routes: counters.deterministic_routes === undefined ? 0 : counters.deterministic_routes,
      comparison_status: comparison.comparison_status || report.comparison_summary_status || "loaded from selected run",
      report_status: report.report_status || report.report_viewer_status || "preview loaded",
      boundary: run.claim_boundary || "Generated local harness output only. Not production telemetry, not production cost evidence, no model execution, no provider calls, no report export, and no file writing."
    });
    runError = "";
    setRetryState(false, "No selected-run error.");
    renderSelectedCounters(run.generated_counters, run.event_count || 0);
    renderSelectedComparison(run.comparison_summary, run.model_execution_status || "execution_not_connected");
    renderSelectedReportMetadata(run.report_metadata_summary);
    if (shouldUpdateHistory) {
      addRunToHistory(run);
    } else {
      renderRunHistory();
    }
  };

  const runLocalHarness = async (requestId) => {
    if (!requestById.has(requestId)) {
      renderRunError("No approved request is selected.");
      return;
    }
    selectedRequestId = requestId;
    lastApprovedRequestId = requestId;
    renderSelectedRequest();
    setRunLoading(true);
    setRetryState(false, "No selected-run error.");
    text("kora-run-status", "running");
    text("kora-composer-run-status", "running");
    text("kora-composer-request-id", requestId);
    text("kora-composer-run-id", "pending local harness response");
    text("kora-run-claim-boundary", "Local harness run requested for an approved request id only.");
    setRunProgressSummary({
      state: "running",
      step: "Run submitted",
      event_status: "Waiting for generated events",
      stream_status: "Generated event stream not connected yet",
      error: "No run error. Waiting for local harness response."
    });
    setPrimaryResultSummary({
      request_id: requestId,
      run_id: "pending local harness response",
      status: "running",
      comparison_status: "pending",
      report_status: "pending",
      boundary: "Local harness run requested for an approved request id only. No arbitrary prompt execution, model execution, provider calls, downloads, report export, or file writing."
    });
    setShellSelectedRunSurfaceState({
      run_id: "pending local harness response",
      timeline: "pending",
      counters: "pending",
      comparison: "pending",
      report: "pending"
    });
    try {
      const response = await fetch("/api/harness/run", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({request_id: requestId})
      });
      let payload;
      try {
        payload = await response.json();
      } catch (parseError) {
        throw new Error("The local response could not be parsed.");
      }
      if (!response.ok || payload.ok === false) {
        throw new Error(payload.message || "Local harness run failed.");
      }
      if (!payload.run_id || !payload.run_status) {
        throw new Error("The local response was missing selected-run fields.");
      }
      renderRunResponse(payload);
      await connectGeneratedEventStream();
    } catch (error) {
      const message = error instanceof TypeError ? "The local harness endpoint was unavailable." : (error && error.message ? error.message : "Local harness run failed.");
      renderRunError(message);
    } finally {
      setRunLoading(false);
    }
  };

  document.querySelectorAll("[data-kora-request-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const requestId = button.getAttribute("data-kora-request-id") || "";
      if (requestById.has(requestId)) {
        selectedRequestId = requestId;
        renderSelectedRequest();
      }
    });
  });

  const runButton = document.getElementById("kora-run-local-harness-button");
  if (runButton) {
    runButton.addEventListener("click", async () => {
      await runLocalHarness(selectedRequestId);
    });
  }

  const composerRunButton = document.getElementById("kora-composer-run-local-harness-button");
  if (composerRunButton) {
    composerRunButton.addEventListener("click", async () => {
      await runLocalHarness(selectedRequestId);
    });
  }

  const retryButton = document.getElementById("kora-retry-last-approved-request-button");
  const shellRetryButton = document.getElementById("kora-shell-retry-last-approved-request-button");
  [retryButton, shellRetryButton].forEach((button) => {
    if (!button) {
      return;
    }
    button.setAttribute("data-kora-retry-last-approved-request-button", "true");
    button.addEventListener("click", async () => {
      if (!requestById.has(lastApprovedRequestId)) {
        renderRunError("Retry is unavailable because no approved request has been selected.");
        return;
      }
      await runLocalHarness(lastApprovedRequestId);
    });
  });

  const clearHistoryButton = document.getElementById("kora-clear-run-history-button");
  if (clearHistoryButton) {
    clearHistoryButton.addEventListener("click", () => {
      clearLocalRunHistory();
    });
  }

  renderSelectedRequest();
  setPrimaryResultSummary({
    request_id: selectedRequestId || "none",
    run_id: "not run yet",
    status: "not_started",
    event_count: "0",
    avoided_model_calls: "0",
    deterministic_routes: "0",
    comparison_status: "not loaded",
    report_status: "not loaded",
    boundary: "Generated local harness output only. Not production telemetry, not production cost evidence, no model execution, no provider calls, no report export, and no file writing."
  });
  setRunProgressSummary({
    state: "idle",
    step: "No run selected",
    event_status: "No generated events yet",
    stream_status: "Generated event stream idle",
    error: "No run error. Generated event stream is local harness events only, not model token streaming or provider output."
  });
  setRetryState(false, "No selected-run error.");
  setShellSelectedRunSurfaceState({
    run_id: "not run yet",
    timeline: "not loaded",
    counters: "not loaded",
    comparison: "not loaded",
    report: "not loaded"
  });
  renderRunHistory();
  window.koraStudioAccessibilityState = {
    get shell_state() { return getShellAccessibilityState(); }
  };
  window.koraStudioSelectedRunState = {
    get selected_request_id() { return selectedRequestId; },
    get selected_run_id() { return selectedRunId; },
    get selected_run_record() { return runHistory.find((record) => record.run_id === selectedRunId) || null; },
    get run_loading() { return runLoading; },
    get run_error() { return runError; },
    get last_approved_request_id() { return lastApprovedRequestId; },
    get retry_available() { return retryAvailable; },
    get run_history() { return runHistory.slice(); },
    get run_history_limit() { return runHistoryLimit; },
    get sse_available() { return sseAvailable; },
    get sse_status() { return sseStatus; },
    get sse_error() { return sseError; },
    get sse_events() { return sseEvents.slice(); },
    get sse_fallback_used() { return sseFallbackUsed; },
    get selected_run_events() { return selectedRunEvents.slice(); },
    get selected_run_counters() { return Object.assign({}, selectedRunCounters); },
    get selected_run_comparison() { return Object.assign({}, selectedRunComparison); },
    get selected_run_report_metadata() { return Object.assign({}, selectedRunReportMetadata); }
  };
  window.koraStudioScriptStatus = {status: "ready", error: ""};
})();
