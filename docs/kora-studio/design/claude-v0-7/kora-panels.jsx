/* eslint-disable */
// KORA Studio — data, icons, picker & inspector drawer.
// Exports to window for the main app script.

const { useState, useRef, useEffect } = React;

/* ----------------------------- icons ----------------------------- */
const I = {
  search: (p) => (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" {...p}>
      <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="1.7"/>
      <path d="M20 20l-3.4-3.4" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"/>
    </svg>
  ),
  chevDown: (p) => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" {...p}>
      <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  chevRight: (p) => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" {...p}>
      <path d="M9 6l6 6-6 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  panel: (p) => (
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" {...p}>
      <rect x="3" y="4" width="18" height="16" rx="2.5" stroke="currentColor" strokeWidth="1.6"/>
      <path d="M15 4v16" stroke="currentColor" strokeWidth="1.6"/>
      <rect x="15.6" y="4.6" width="5.4" height="14.8" rx="1.6" fill="currentColor" opacity="0.5"/>
    </svg>
  ),
  close: (p) => (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" {...p}>
      <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"/>
    </svg>
  ),
  arrowUp: (p) => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" {...p}>
      <path d="M12 19V6M6 12l6-6 6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  check: (p) => (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" {...p}>
      <path d="M5 12.5l4.5 4.5L19 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
};

/* ----------------------------- model catalog ----------------------------- */
// Honest taxonomy. Nothing is "installed" or "execution connected" yet.
//   stateKey: catalog | estimated | installed | connected
const STATES = {
  catalog:   { tag: "Catalog example", cls: "gray",  dot: "gray"  },
  estimated: { tag: "Estimated runnable", cls: "blue", dot: "blue" },
  installed: { tag: "Installed locally", cls: "green", dot: "green" },
  connected: { tag: "Execution connected", cls: "green", dot: "green" },
};

const MODELS = [
  { id: "qwen25-7b",  name: "Qwen 2.5 7B Instruct",  size: "~4.7 GB", quant: "Q4_K_M",
    state: "estimated", note: "estimated runnable on this profile" },
  { id: "mistral-7b", name: "Mistral 7B Instruct",   size: "~4.4 GB", quant: "Q4_K_M",
    state: "estimated", note: "estimated runnable on this profile" },
  { id: "llama31-8b", name: "Llama 3.1 8B Instruct", size: "~4.9 GB", quant: "Q4_K_M",
    state: "estimated", note: "estimated runnable on this profile" },
  { id: "phi3-mini",  name: "Phi-3 Mini 3.8B",       size: "~2.3 GB", quant: "Q4_K_M",
    state: "estimated", note: "lighter footprint estimate" },
  { id: "gemma2-9b",  name: "Gemma 2 9B Instruct",   size: "~5.4 GB", quant: "Q4_K_M",
    state: "catalog",   note: "catalog example — fit not estimated yet" },
  { id: "qwen25-14b", name: "Qwen 2.5 14B Instruct", size: "~8.9 GB", quant: "Q4_K_M",
    state: "catalog",   note: "catalog example — likely exceeds local profile" },
];

/* ----------------------------- Model Picker ----------------------------- */
function ModelPicker({ selectedId, onSelect, onClose }) {
  const [q, setQ] = useState("");
  const inputRef = useRef(null);
  useEffect(() => { inputRef.current && inputRef.current.focus(); }, []);

  const rows = MODELS.filter((m) => m.name.toLowerCase().includes(q.trim().toLowerCase()));

  return (
    <React.Fragment>
      <div className="scrim" onClick={onClose}></div>
      <div className="picker" role="listbox" aria-label="Open-source LLM catalog">
        <div className="picker-search">
          {I.search()}
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search or select open-source LLM"
            spellCheck="false"
          />
        </div>
        <div className="picker-list">
          {rows.map((m) => {
            const st = STATES[m.state];
            return (
              <button
                key={m.id}
                className={"model-row" + (selectedId === m.id ? " selected" : "")}
                onClick={() => onSelect(m)}
                role="option"
                aria-selected={selectedId === m.id}
              >
                <div className="mr-main">
                  <div className="mr-name">{m.name}</div>
                  <div className="mr-meta">
                    <span className={"dot " + st.dot}></span>
                    <span>{m.note}</span>
                    <span className="sep">·</span>
                    <span>not installed</span>
                  </div>
                </div>
                <div className="mr-right">
                  <span className="mr-size">{m.size}</span>
                  <span className={"state-tag " + st.cls}>{st.tag}</span>
                  <span className="check">{I.check()}</span>
                </div>
              </button>
            );
          })}
          {rows.length === 0 && (
            <div style={{ padding: "26px 14px", textAlign: "center", color: "var(--text-4)", fontSize: 13 }}>
              No catalog match for “{q}”.
            </div>
          )}
        </div>
        <div className="picker-foot">
          <span className="legend-item"><span className="dot gray"></span>Catalog example</span>
          <span className="legend-item"><span className="dot blue"></span>Estimated runnable</span>
          <span className="legend-item"><span className="dot ring"></span>Installed locally</span>
          <span className="legend-item"><span className="dot green"></span>Execution connected</span>
        </div>
      </div>
    </React.Fragment>
  );
}

/* ----------------------------- Drawer sections ----------------------------- */
function Section({ title, badge, open, onToggle, children }) {
  return (
    <div className={"sec" + (open ? " open" : "")}>
      <button className="sec-head" onClick={onToggle} aria-expanded={open}>
        <span className="sec-chev">{I.chevRight()}</span>
        <span className="sec-title">{title}</span>
        {badge && <span className="sec-badge">{badge}</span>}
      </button>
      <div className="sec-body"><div><div className="sec-content">{children}</div></div></div>
    </div>
  );
}

function KV({ k, v, dot }) {
  return (
    <div className="kv">
      <span className="kv-k">{k}</span>
      <span className="kv-v">{dot && <span className={"dot " + dot}></span>}{v}</span>
    </div>
  );
}

const ROUTE = [
  { name: "Deterministic route", desc: "Local rule + template paths resolved without a model.", state: "done", flag: "generated harness" },
  { name: "Structured lookup", desc: "Catalog / profile lookups against local data.", state: "done", flag: "generated harness" },
  { name: "Validation", desc: "Shape & claim checks on the generated result.", state: "done", flag: "generated harness" },
  { name: "Model-needed boundary", desc: "Steps requiring a model stop here until execution is connected.", state: "boundary", flag: "deferred · not connected" },
];

function Drawer({ open, model, onClose }) {
  const [secs, setSecs] = useState({ runtime: true, model: true, catalog: false, route: false, counters: false, report: false, claims: false });
  const toggle = (k) => setSecs((s) => ({ ...s, [k]: !s[k] }));
  const st = model ? STATES[model.state] : null;

  return (
    <aside className={"drawer" + (open ? " open" : "")} aria-hidden={!open}>
      <div className="drawer-head">
        <div>
          <h2>Details</h2>
          <div className="dh-sub">Inspector · local preview</div>
        </div>
        <button className="icon-btn" onClick={onClose} aria-label="Close details">{I.close()}</button>
      </div>

      <div className="drawer-body">
        {/* Runtime status */}
        <Section title="Runtime status" open={secs.runtime} onToggle={() => toggle("runtime")}>
          <KV k="Local runtime" v="Not connected" dot="amber" />
          <KV k="Model execution" v="Not connected yet" dot="amber" />
          <KV k="Provider calls" v="Disabled" dot="gray" />
          <KV k="Cloud sync" v="Disabled" dot="gray" />
          <KV k="Mode" v="Local preview" dot="blue" />
        </Section>

        {/* Selected model */}
        <Section title="Selected model" open={secs.model} onToggle={() => toggle("model")}>
          {model ? (
            <React.Fragment>
              <KV k="Model" v={model.name} />
              <KV k="Source" v={st.tag} dot={st.dot} />
              <KV k="Est. download" v={model.size} />
              <KV k="Suggested quant" v={model.quant} />
              <KV k="Validated" v="No" dot="amber" />
              <div className="note">Model recommendations are estimates until validated. KORA does not remove model memory requirements.</div>
            </React.Fragment>
          ) : (
            <div style={{ fontSize: 12.5, color: "var(--text-4)", padding: "4px 0" }}>
              No model selected. Pick one from the top control — selecting does not install or run it.
            </div>
          )}
        </Section>

        {/* Catalog vs installed */}
        <Section title="Catalog vs installed" open={secs.catalog} onToggle={() => toggle("catalog")}>
          <div className="compare">
            <div className="compare-card">
              <h4>Catalog</h4>
              <div className="compare-val">{MODELS.length} examples</div>
              <div className="compare-sub">reference entries only</div>
            </div>
            <div className="compare-card">
              <h4>Installed</h4>
              <div className="compare-val">0 models</div>
              <div className="compare-sub">nothing on this machine yet</div>
            </div>
          </div>
          <div className="note">Catalog examples are not installed models.</div>
        </Section>

        {/* Route trace */}
        <Section title="Route trace" badge="sample" open={secs.route} onToggle={() => toggle("route")}>
          <div className="route">
            {ROUTE.map((r, i) => (
              <div key={i} className={"route-step " + r.state}>
                <div className="route-rail">
                  <span className="route-node"></span>
                  <span className="route-line"></span>
                </div>
                <div className="route-main">
                  <div className="route-name">{r.name}</div>
                  <div className="route-desc">{r.desc}</div>
                  <span className="route-flag">{r.flag}</span>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* Generated counters */}
        <Section title="Generated counters" badge="generated" open={secs.counters} onToggle={() => toggle("counters")}>
          <div className="counters">
            <div className="counter"><div className="counter-n">12</div><div className="counter-l">routes evaluated</div></div>
            <div className="counter"><div className="counter-n">7</div><div className="counter-l">deterministic hits</div></div>
            <div className="counter"><div className="counter-n">4</div><div className="counter-l">structured lookups</div></div>
            <div className="counter"><div className="counter-n">1</div><div className="counter-l">model-needed deferrals</div></div>
          </div>
          <div className="note">Counters come from a generated harness, not live model execution.</div>
        </Section>

        {/* Report metadata */}
        <Section title="Report metadata" badge="preview" open={secs.report} onToggle={() => toggle("report")}>
          <div className="meta-block">
            <div><span className="mk">report.kind</span>: routing_preview</div>
            <div><span className="mk">source</span>: <span className="mv-str">catalog_example</span></div>
            <div><span className="mk">model.validated</span>: <span className="mv-false">false</span></div>
            <div><span className="mk">execution.connected</span>: <span className="mv-false">false</span></div>
            <div><span className="mk">provider.calls</span>: disabled</div>
            <div><span className="mk">cloud.sync</span>: disabled</div>
          </div>
          <div className="note">Preview only. Not an execution record.</div>
        </Section>

        {/* Claim boundaries */}
        <Section title="Claim boundaries" open={secs.claims} onToggle={() => toggle("claims")}>
          <div className="claims">
            {[
              "Catalog examples are not installed models.",
              "Model recommendations are estimates until validated.",
              "KORA does not remove model memory requirements.",
              "Provider calls disabled · Cloud sync disabled.",
              "Model execution not connected yet.",
            ].map((c, i) => (
              <div className="claim" key={i}><span className="dot ring cdot"></span><span>{c}</span></div>
            ))}
          </div>
        </Section>
      </div>

      <div className="drawer-foot">
        <span className="dot blue"></span>
        <span>Local preview — no provider calls made.</span>
      </div>
    </aside>
  );
}

Object.assign(window, { KORA_I: I, KORA_MODELS: MODELS, KORA_STATES: STATES, KoraPicker: ModelPicker, KoraDrawer: Drawer });
