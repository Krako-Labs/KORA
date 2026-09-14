(() => {
"use strict";
const $=id=>document.getElementById(id), text=(id,v)=>{$(id).textContent=String(v);};
const storageKey="kora-festa-replay-v1";
let pack=null,data=null,cursor=-1,timer=null,busy=false,blocked=true,serial=0,controller=null;
const reduced=()=>window.matchMedia("(prefers-reduced-motion: reduce)").matches;
function saved(){try{return JSON.parse(sessionStorage.getItem(storageKey));}catch{return null;}}
function persist(){try{sessionStorage.setItem(storageKey,JSON.stringify({identity:data.identity,build:pack.software_sha256,cursor,mode:data.mode}));}catch{/* In-memory replay remains usable when storage is unavailable. */}}
function pause(){if(timer)clearInterval(timer);timer=null;text("play","Play replay");}
function controls(){
 const usable=!!data&&!blocked&&!busy;
 ["previous","next","restart","play"].forEach(id=>{$(id).disabled=!usable;});
 $("previous").disabled=!usable||cursor<=0;$("next").disabled=!usable||cursor>=data?.frames.length-1;
 $("play").disabled=!usable||cursor>=data?.frames.length-1;
 $("recover").disabled=busy;$("fallback").disabled=busy||!pack?.fixture||data?.mode==="fixture";
 $("retained").disabled=busy||data?.mode!=="fixture";
}
function expose(){window.koraFestaState={mode:data?.mode||null,cursor,identity:data?.identity||null,build:pack?.software_sha256||null,blocked,busy,playing:!!timer,new_model_calls:0};}
function render(){
 if(!data){controls();expose();return;}
 const frame=data.frames[cursor], p=frame.projection;
 text("mode",data.mode==="fixture"?"FIXTURE FALLBACK · SYNTHETIC":"RETAINED EVIDENCE · REPLAY");
 document.body.dataset.mode=data.mode;
 text("boundary",data.boundary);text("request",data.request);
 text("source-calls",data.mode==="fixture"?"Not measured":"Mac "+data.source_model_calls.mac+" · H100 "+data.source_model_calls.h100);
 text("source-date",data.mode==="fixture"?"Synthetic events · no model calls":Object.entries(data.source_dates).map(([k,v])=>k+": "+v).join(" / "));
 text("cursor",(cursor+1)+" / "+data.frames.length);
 text("phase","Recorded event: "+frame.event.event_type+" · "+p.run_state);
 const tasks=Object.values(p.tasks), groups=data.mode==="retained"?
 [["Mac source",t=>t.task_id==="mac"],["H100 source",t=>t.task_id==="h100"],["Evidence review",t=>!["mac","h100"].includes(t.task_id)]]:
 [["Deterministic / reuse",t=>["deterministic","exact_reuse"].includes(t.executor_class)||!t.executor_class],["Local AI fixture",t=>t.executor_class==="local_ai"],["Review fixture",t=>t.executor_class==="frontier_ai"]];
 $("lanes").replaceChildren(...groups.map(([label,select])=>{
  const a=document.createElement("article");a.className="lane";const h=document.createElement("h3");h.textContent=label;a.append(h);
  tasks.filter(select).forEach(t=>{const el=document.createElement("div");el.className="task";el.dataset.state=t.state;
   const name=document.createElement("strong");name.textContent=t.label;const state=document.createElement("span");state.textContent=t.state+(t.dependencies.length?" · after "+t.dependencies.join(", "):"");el.append(name,state);a.append(el);});return a;
 }));
 const answer=frame.view.answer;
 text("answer",answer?(typeof answer==="string"?answer:JSON.stringify(answer,null,2)):"Waiting for the recorded merge event.");
 text("outcome",p.accepted_outcome?(data.mode==="fixture"?"Fixture completed · not measured":"Recorded objective pass · historical"):(p.verification_state==="not_started"?"Not started":p.verification_state));
 text("event",JSON.stringify(frame.event,null,2));
 text("evidence",JSON.stringify({mode:data.mode,identity:data.identity,source_digests:data.source_digests||null,source_restoration:data.source_restoration||null,source_usage:data.source_usage||null,new_model_calls:0,live_runtime_status:"not_checked"},null,2));
 persist();controls();expose();
}
function fail(message){
 pause();blocked=true;document.body.dataset.blocked="true";text("status","Playback blocked");text("notice",message);text("outcome","Unavailable · revalidation required");controls();expose();
}
function select(next,restore=true){
 pause();const prior=saved();data=next;cursor=0;blocked=false;document.body.dataset.blocked="false";
 let note=next.mode==="fixture"?"Explicit fixture fallback. No measured execution or recovery result.":"Source objective pass is historical; current runtime availability is not checked.";
 if(restore&&prior?.mode===next.mode){
  if(prior.identity===next.identity&&prior.build===pack.software_sha256&&Number.isInteger(prior.cursor)&&prior.cursor>=0&&prior.cursor<next.frames.length){cursor=prior.cursor;note="Viewer restored at the last displayed event. No new inference.";}
  else note="Source or build changed. Old replay cursor discarded; starting from event 1.";
 }
 text("status",next.mode==="fixture"?"Fixture playback ready":"Retained replay ready");text("notice",note);render();
}
async function preflight(returnToRetained=false){
 pause();const generation=++serial;controller?.abort();controller=new AbortController();busy=true;blocked=true;controls();expose();
 text("status","Checking preflight");text("notice","Verifying build, retained evidence and replay identity.");
 const timeout=setTimeout(()=>controller.abort(),8000);
 try{
  const response=await fetch("/api/hero/festa",{cache:"no-store",signal:controller.signal});
  if(!response.ok)throw Error("Preflight rejected ("+response.status+").");
  const value=await response.json();
  if(generation!==serial)return;
  if(value.schema_version!=="hero.festa-preflight.v1"||!value.fixture?.frames?.length)throw Error("Invalid preflight response.");
  pack=value;text("checks",JSON.stringify(value.checks,null,2));text("lock-status",value.checks.lock);text("build",value.software_sha256||"Unavailable");
  if(!returnToRetained&&data?.mode==="fixture"){select(value.fixture);return;}
  if(!value.ready||!value.retained)throw Error("Retained replay unavailable. Check preflight details, recover, or explicitly choose fixture fallback.");
  select(value.retained);
 }catch(error){if(generation===serial)fail(error.name==="AbortError"?"Connection timed out. Recover the viewer or explicitly use the cached fixture.":error.message);}
 finally{clearTimeout(timeout);if(generation===serial){busy=false;controls();expose();}}
}
$("recover").onclick=()=>preflight(false);
$("retained").onclick=()=>preflight(true);
$("fallback").onclick=()=>{if(pack?.fixture&&!busy)select(pack.fixture,false);};
$("next").onclick=()=>{pause();cursor++;render();};
$("previous").onclick=()=>{pause();cursor--;render();};
$("restart").onclick=()=>{pause();cursor=0;render();};
$("play").onclick=()=>{
 if(timer){pause();controls();expose();return;}
 text("play","Pause replay");
 timer=setInterval(()=>{if(blocked||busy||cursor>=data.frames.length-1){pause();controls();expose();return;}cursor++;render();if(cursor===data.frames.length-1){pause();controls();expose();}},reduced()?1000:650);
 controls();expose();
};
window.addEventListener("offline",()=>{
 ++serial;controller?.abort();busy=false;
 if(data?.mode!=="fixture")fail("Connection lost. Playback paused. Recover after reconnecting, or explicitly use the cached fixture.");
});
window.addEventListener("online",()=>{if(blocked)text("notice","Connection restored. Use Check & recover viewer to revalidate before replaying.");});
document.addEventListener("visibilitychange",()=>{if(document.hidden){pause();controls();expose();}});
window.addEventListener("pagehide",()=>{pause();controller?.abort();});
preflight();
})();
