/* The browser displays canonical server projections of explicitly synthetic events. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const names = {deterministic:"Deterministic",exact_reuse:"Exact Reuse",local_ai:"Local AI",frontier_ai:"Frontier AI"};
  const runtimeNames = {"mlx-lm":"MLX-LM","llama.cpp":"llama.cpp",freetoken:"FreeToken",ktransformers:"KTransformers"};
  const adapterMode = document.body.dataset.heroMode === "adapter";
  const api = adapterMode ? "/api/hero/adapter" : "/api/hero";
  const key = adapterMode ? "kora.hero.adapter.cursor.v1" : "kora.hero.fixture.cursor.v1";
  const fixtureDigest = data => data.event_digest || data.planning_bundle.evidence_digest;
  let fixture, cursor = -1, queue = [], source = null, epoch = 0, timer = null, playing = false;
  let history = [], recovering = false;
  function readSaved() { try { return JSON.parse(sessionStorage.getItem(key) || "null"); } catch { return null; } }
  function save() { try { sessionStorage.setItem(key, JSON.stringify({scenario:fixture.scenario,cursor,digest:fixtureDigest(fixture)})); } catch { /* Playback works without persistence. */ } }
  function text(id, value) { $(id).textContent = value; }
  function element(tag, content, className) { const node=document.createElement(tag); if(content !== undefined) node.textContent=content; if(className) node.className=className; return node; }
  async function get(url) { const response=await fetch(url,{cache:"no-store"}); if(!response.ok) throw new Error("Fixture request failed ("+response.status+")."); return response.json(); }
  function controls() {
    const ended = fixture && cursor === fixture.event_count - 1;
    $("play").disabled = !fixture || ended || !queue.length;
    $("step").disabled = !fixture || ended || !queue.length || playing;
    $("reset").disabled = !fixture;
    text("play",playing?"Pause":"Play fixture");
  }
  function stop() { playing=false; clearTimeout(timer); timer=null; controls(); }
  function clearScreen() {
    if(adapterMode) {
      history=[]; $("history").replaceChildren(); $("lifecycle").replaceChildren();
      text("adapter-state","Awaiting plan");$("adapter-state").dataset.state="awaiting_plan";text("mock-outcome","None");text("adapter-accepted","Not accepted");
      text("allocation","No mock allocation");text("adapter-reason","");text("adapter-output","No mock response yet.");
      text("adapter-identity","Identity appears after the plan is sealed.");
      $("adapter-telemetry").replaceChildren(element("dt","Telemetry"),element("dd","Not supplied yet"));
      text("phase","Intake");text("event-position","No events played");text("event-kind","");
      $("error").hidden=true;window.koraHeroState=null;return;
    }
    document.querySelectorAll(".task").forEach(node=>node.remove());
    $("candidates").replaceChildren(element("p","Waiting for the plan event."));
    $("history").replaceChildren(); history=[];
    text("memory","—"); text("footprint","—"); text("memory-detail","Waiting for the analysis event");
    text("model-detail","Model-weight bytes · not runtime peak memory");
    text("selected","Awaiting analysis"); text("plan-detail","Candidate decisions appear when the plan event arrives.");
    text("phase","Intake"); text("event-position","No events played"); text("event-kind","");
    text("merge","Not started"); text("verification","Not started"); text("outcome","Pending · fixture");
    for(const id of ["merge-node","verify-node","outcome-node"]) $(id).dataset.state="not_started";
    text("quality","Service acceptance: not started"); text("answer","The answer appears after the merge event. Acceptance remains pending until verification and service acceptance pass.");
    text("reason",""); text("counts","No task completions yet.");
    $("error").hidden=true; window.koraHeroState=null;
  }
  function renderAdapter(frame, record) {
    const {event,view:v}=frame;
    if(event.run_id!==fixture.run_id || event.evidence_level!=="fixture" ||
       v.accepted_outcome!==false || v.B_local_execution.execution_performed!==false ||
       v.A_workload_control.actual_model_calls!==0 || v.A_workload_control.actual_provider_calls!==0)
      throw new Error("Invalid mock review frame.");
    cursor=event.sequence;
    text("phase",event.phase);text("event-position",(cursor+1)+" / "+fixture.event_count+" fixture events");text("event-kind",event.event_type);
    text("adapter-state",v.adapter_state.replaceAll("_"," "));
    $("adapter-state").dataset.state=v.adapter_state;
    text("mock-outcome",v.mock_outcome || "None");
    text("allocation",v.mock_allocation_retained?"Mock allocation retained · cleanup required":"No mock allocation");
    text("adapter-reason",v.compatibility && !v.compatibility.compatible ? v.compatibility.reason_codes.join(" · ") : v.failures.map(f=>f.reason_code).join(" → "));
    text("adapter-output",v.output ?? "No mock response yet.");
    text("adapter-identity",v.runtime_identity?JSON.stringify(v.runtime_identity,null,2):"No identity bound.");
    const labels={input_tokens:"Input tokens",output_tokens:"Output tokens",peak_host_bytes:"Peak host bytes",peak_gpu_bytes:"Peak GPU bytes",load_ms:"Load ms",ttft_ms:"TTFT ms",end_to_end_ms:"End-to-end ms"};
    $("adapter-telemetry").replaceChildren(...Object.entries(labels).flatMap(([name,label])=>[
      element("dt",label),element("dd",v.telemetry ? v.telemetry[name]===null?"Unavailable":String(v.telemetry[name])+" · fixture":"Not supplied yet")
    ]));
    if(record)history.push(event);
    $("lifecycle").replaceChildren(...history.filter(e=>e.event_type.startsWith("adapter.")).map(e=>{
      const node=element("li",e.sequence+" · "+e.event_type+" · "+(e.payload.state || "extension"));
      node.dataset.status=e.status;return node;
    }));
    $("history").replaceChildren(...history.map(e=>element("li",e.sequence+" · "+e.event_type+" · fixture")));
    window.koraHeroState=frame;save();controls();
  }
  function render(frame, record=true) {
    if(adapterMode){renderAdapter(frame,record);return;}
    const {event,projection:p,view:v} = frame;
    if(event.run_id !== fixture.run_id || event.evidence_level !== "fixture") throw new Error("Unexpected event identity.");
    cursor=event.sequence;
    text("phase",event.phase); text("event-position",(cursor+1)+" / "+fixture.event_count+" fixture events");
    text("event-kind",event.event_type);
    if(v.profiles_visible) {
      const domains=fixture.hardware.memory_domains;
      const gpu=domains.find(d=>d.kind==="dedicated_gpu");
      const host=domains.find(d=>d.kind==="unified" || d.kind==="system");
      text("memory",(gpu || host).total_bytes / 1024**3 + " GiB");
      text("memory-detail",gpu ? "Dedicated GPU · fixture / "+host.total_bytes/1024**3+" GiB system RAM · fixture" : "Unified memory · synthetic Mac profile");
      text("footprint",fixture.model.model_weight_bytes / 1024**3 + " GiB");
      text("model-detail",fixture.model.artifact_format+" model-weight bytes · fixture");
    }
    if(v.candidates_visible) {
      const plan=fixture.planning_bundle.plan;
      text("selected",plan.selected_adapter_id ? runtimeNames[plan.selected_adapter_id] : "No selection");
      text("plan-detail",plan.selected_adapter_id ? "Selected for planning only. Runtime has not started." : "Unknown or unsupported inputs fail closed.");
      $("candidates").replaceChildren(...plan.candidates.map(candidate=>{
        const selected=candidate.adapter_id===plan.selected_adapter_id;
        const card=element("article",undefined,"candidate "+(selected?"selected":candidate.rejected?"rejected":"eligible"));
        card.dataset.adapter=candidate.adapter_id;
        card.append(element("strong",runtimeNames[candidate.adapter_id] || candidate.adapter_id));
        card.append(element("p",selected?"Selected · fixture":candidate.rejected?"Rejected · fixture":"Eligible, not selected · fixture","decision"));
        for(const reason of candidate.reason_codes) card.append(element("code",reason));
        return card;
      }));
    }
    for(const task of Object.values(p.tasks)) {
      let node=document.getElementById("hero-task-"+task.task_id);
      if(!node) { node=element("article",undefined,"task"); node.id="hero-task-"+task.task_id; }
      node.dataset.state=task.state; node.dataset.attempt=String(task.attempt);
      node.replaceChildren(element("strong",task.label),element("span",task.state+" · attempt "+task.attempt,"state"),
        element("p",task.dependencies.length?"Needs: "+task.dependencies.join(" + "):"From workload input"),
        element("p",task.adapter_id || "Awaiting route"));
      if(v.outputs[task.task_id]) node.append(element("p",v.outputs[task.task_id]));
      const lane=task.executor_class;
      const parent=lane ? document.querySelector('[data-lane="'+lane+'"] .tasks') : $("pending");
      if(node.parentElement !== parent) parent.append(node);
    }
    text("merge",p.merge_state.replaceAll("_"," "));
    text("verification",p.verification_state+" · fixture");
    text("outcome",v.fixture_accepted_outcome?"Accepted · fixture":p.run_state==="failed"?"Not accepted · fixture":"Pending · fixture");
    $("merge-node").dataset.state=p.merge_state;
    $("verify-node").dataset.state=p.verification_state;
    $("outcome-node").dataset.state=v.fixture_accepted_outcome?"passed":p.run_state==="failed"?"failed":"pending";
    text("quality","Service acceptance: "+v.service_acceptance);
    if(v.answer) text("answer",v.answer);
    text("reason",v.reason);
    $("counts").replaceChildren(...Object.entries(v.A_workload_control.fixture_completed_tasks).map(([lane,count])=>element("span",names[lane]+": "+count)));
    if(record) history.push(event);
    $("history").replaceChildren(...history.map(item=>element("li",item.sequence+" · "+item.event_type+" · "+(item.task_id || item.phase)+" · fixture")));
    window.koraHeroState={event,projection:p,view:v};
    save(); controls();
  }
  function accept(frame) {
    if(frame.event.sequence !== cursor+1) throw new Error("Event gap detected. Reconnect to restore ordered playback.");
    render(frame);
  }
  function next() {
    if(!queue.length) { stop(); return; }
    try { accept(queue.shift()); }
    catch(error) { stop(); fail(error); return; }
    if(cursor===fixture.event_count-1) stop();
    controls();
  }
  function tick() {
    if(!playing) return;
    next();
    if(playing) timer=setTimeout(tick,650);
  }
  function fail(error) { text("error",String(error.message || error)); $("error").hidden=false; text("transport","Playback paused · restore with Replay"); }
  function enqueue(frame) {
    const expected=queue.length ? queue[queue.length-1].event.sequence+1 : cursor+1;
    if(frame.event.sequence < expected) return; // reconnect duplicates are harmless
    if(frame.event.sequence !== expected || frame.event.run_id !== fixture.run_id || frame.event.evidence_level !== "fixture") throw new Error("Invalid fixture event sequence.");
    queue.push(frame); controls();
  }
  async function fallback(token) {
    if(recovering || token!==epoch) return;
    recovering=true; source?.close();
    try {
      const payload=await get(api+"/events?scenario="+fixture.scenario+"&after="+cursor);
      if(token!==epoch) return;
      queue=[]; payload.frames.forEach(enqueue);
      text("transport","Recovered ordered events · fixture");
    } catch(error) { if(token===epoch){stop();fail(error);} }
    finally { if(token===epoch) recovering=false; }
  }
  function connect(token) {
    text("transport","Connecting fixture event stream…");
    source=new EventSource(api+"/sse?scenario="+fixture.scenario+"&after="+cursor);
    source.addEventListener("hero",message=>{
      if(token!==epoch) return;
      try { enqueue(JSON.parse(message.data)); text("transport","Fixture events ready · SSE"); }
      catch { fallback(token); }
    });
    source.addEventListener("end",()=>{
      if(token!==epoch) return;
      source.close(); text("transport","Fixture events ready · SSE");
      if(cursor+queue.length+1 !== fixture.event_count) fallback(token);
    });
    source.onerror=()=>fallback(token);
  }
  async function load(scenario, restore) {
    const token=++epoch;
    stop(); source?.close(); queue=[]; fixture=null; cursor=-1; recovering=false; controls();clearScreen();
    text("transport","Loading fixture…");
    try {
      const data=await get(api+"/fixture?scenario="+scenario);
      if(token!==epoch) return;
      fixture=data; if(!adapterMode)text("request",data.request); text("digest",(adapterMode?"Event log SHA-256 · ":"Planning SHA-256 · ")+fixtureDigest(data));
      $("evidence-link").href=api+"/fixture?scenario="+scenario;
      const saved=restore ? readSaved() : null;
      if(saved && saved.scenario===scenario && saved.digest===fixtureDigest(data) &&
          Number.isInteger(saved.cursor) && saved.cursor>=0 && saved.cursor<data.event_count) {
        const payload=await get(api+"/events?scenario="+scenario);
        if(token!==epoch) return;
        for(const frame of payload.frames.slice(0,saved.cursor+1)) accept(frame);
        text("transport","Restored identical fixture state · paused");
      }
      save();controls();
      if(cursor<data.event_count-1) connect(token);
      else text("transport","Restored completed fixture · paused");
    } catch(error) { if(token===epoch) fail(error); }
  }
  $("play").addEventListener("click",()=>{if(playing)stop();else{playing=true;controls();tick();}});
  $("step").addEventListener("click",next);
  $("reset").addEventListener("click",()=>load($("scenario").value,false));
  $("scenario").addEventListener("change",()=>load($("scenario").value,false));
  window.addEventListener("pagehide",()=>{stop();source?.close();});
  const saved=readSaved();
  if(saved && Array.from($("scenario").options).some(option=>option.value===saved.scenario)) $("scenario").value=saved.scenario;
  load($("scenario").value,true);
})();
