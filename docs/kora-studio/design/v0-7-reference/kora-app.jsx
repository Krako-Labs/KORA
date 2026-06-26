/* eslint-disable */
// KORA Studio — main app shell.

const { useState: useStateA, useRef: useRefA, useEffect: useEffectA } = React;
const I = window.KORA_I;
const STATES = window.KORA_STATES;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "blue",
  "density": "comfortable",
  "showPills": true
}/*EDITMODE-END*/;

const ACCENTS = {
  blue:    "oklch(0.70 0.085 235)",
  green:   "oklch(0.72 0.085 156)",
  neutral: "oklch(0.78 0.012 250)",
};

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [selected, setSelected] = useStateA(null);
  const [pickerOpen, setPickerOpen] = useStateA(false);
  const [drawerOpen, setDrawerOpen] = useStateA(false);
  const [text, setText] = useStateA("");
  const taRef = useRefA(null);

  // apply accent token
  useEffectA(() => {
    document.documentElement.style.setProperty("--accent", ACCENTS[t.accent] || ACCENTS.blue);
  }, [t.accent]);

  // esc closes overlays
  useEffectA(() => {
    const onKey = (e) => {
      if (e.key === "Escape") { setPickerOpen(false); setDrawerOpen(false); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const grow = (el) => { if (!el) return; el.style.height = "auto"; el.style.height = Math.min(el.scrollHeight, 180) + "px"; };
  const st = selected ? STATES[selected.state] : null;

  return (
    <div className={"app" + (drawerOpen ? " drawer-open" : "") + (t.density === "compact" ? " compact" : "")}>
      {/* ---------------- Top bar ---------------- */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark"></div>
          <div className="brand-name">KORA <span>Studio</span></div>
        </div>

        <button
          className={"model-control" + (pickerOpen ? " active" : "") + (selected ? " selected" : "")}
          onClick={() => setPickerOpen((v) => !v)}
        >
          <span className="mc-icon">{selected ? <span className={"dot " + st.dot}></span> : I.search()}</span>
          <span className="mc-text">{selected ? selected.name : "Search or select open-source LLM"}</span>
          <span className="mc-chev">{I.chevDown()}</span>
        </button>

        <div className="top-right">
          {selected && (
            <div className="status-chip" title={st.tag}>
              <span className={"dot " + st.dot}></span>
              <span className="sc-name">{st.tag}</span>
            </div>
          )}
          <button
            className={"icon-btn" + (drawerOpen ? " on" : "")}
            onClick={() => setDrawerOpen((v) => !v)}
            aria-label="Open details"
            title="Details"
          >
            {I.panel()}
          </button>
        </div>
      </header>

      {/* ---------------- Work area ---------------- */}
      <main className="work">
        <div className="work-inner">
          <h1 className="headline">What do you want to work on?</h1>
          <p className="subline">Choose a local model once. KORA keeps routing details out of the way.</p>

          <div className="composer">
            <textarea
              ref={taRef}
              value={text}
              onChange={(e) => { setText(e.target.value); grow(e.target); }}
              placeholder="Ask KORA…"
              rows="1"
            ></textarea>
            <div className="composer-bar">
              <div className="composer-hint">
                {selected ? (
                  <React.Fragment><span className={"dot " + st.dot}></span>{selected.name} · model execution not connected yet</React.Fragment>
                ) : (
                  <React.Fragment><span className="dot gray"></span>Select a local model to begin</React.Fragment>
                )}
              </div>
              <button className={"send-btn" + (text.trim() ? " ready" : "")} aria-label="Run" disabled={!text.trim()} title={text.trim() ? "Routing runs locally; model steps stay deferred" : "Type a task"}>
                {I.arrowUp()}
              </button>
            </div>
          </div>

          <div className={"pills" + (t.showPills ? "" : " hidden-pills")}>
            <span className="pill"><span className="dot blue"></span>Local preview</span>
            <span className="pill"><span className="dot gray"></span>Provider calls disabled</span>
            <span className="pill"><span className="dot amber"></span>Model execution not connected yet</span>
          </div>
        </div>
      </main>

      {/* ---------------- Picker ---------------- */}
      {pickerOpen && (
        <window.KoraPicker
          selectedId={selected ? selected.id : null}
          onSelect={(m) => { setSelected(m); setPickerOpen(false); }}
          onClose={() => setPickerOpen(false)}
        />
      )}

      {/* ---------------- Drawer ---------------- */}
      <window.KoraDrawer open={drawerOpen} model={selected} onClose={() => setDrawerOpen(false)} />

      {/* ---------------- Tweaks ---------------- */}
      <TweaksPanel>
        <TweakSection label="Accent" />
        <TweakColor
          label="Accent color"
          value={t.accent === "blue" ? "#5a9fd6" : t.accent === "green" ? "#52a87a" : "#c2c7d0"}
          options={["#5a9fd6", "#52a87a", "#c2c7d0"]}
          onChange={(v) => setTweak("accent", v === "#5a9fd6" ? "blue" : v === "#52a87a" ? "green" : "neutral")}
        />
        <TweakSection label="Layout" />
        <TweakRadio label="Density" value={t.density} options={["comfortable", "compact"]} onChange={(v) => setTweak("density", v)} />
        <TweakToggle label="Show status pills" value={t.showPills} onChange={(v) => setTweak("showPills", v)} />
      </TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
