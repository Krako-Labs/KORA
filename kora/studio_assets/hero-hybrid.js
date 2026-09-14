(() => {
"use strict";
const $=id=>document.getElementById(id);
const show=(id,value)=>{$(id).textContent=String(value);};
let data=null,cursor=0;
function render(){
 const events=data.event_log.events;
 const tasks=new Map();
 for(const e of events.slice(0,cursor+1)){
  if(e.event_type==="task.created")tasks.set(e.task_id,{label:e.payload.label,state:"created"});
  if(e.task_id&&tasks.has(e.task_id)&&e.event_type!=="task.created"){
   const states={"task.ready":"ready","task.started":"running","task.completed":"completed","task.failed":"failed"};
   if(states[e.event_type])tasks.get(e.task_id).state=states[e.event_type];
  }
 }
 $("tasks").replaceChildren(...Array.from(tasks.values(),t=>{
  const li=document.createElement("li");li.textContent=t.label+" · "+t.state;return li;
 }));
 show("cursor",(cursor+1)+" / "+events.length);
 show("event",JSON.stringify(events[cursor],null,2));
 $("previous").disabled=cursor===0;$("next").disabled=cursor===events.length-1;
 $("end").disabled=cursor===events.length-1;
}
$("previous").onclick=()=>{cursor--;render();};
$("next").onclick=()=>{cursor++;render();};
$("end").onclick=()=>{cursor=data.event_log.events.length-1;render();};
fetch("/api/hero/hybrid",{cache:"no-store"}).then(r=>{
 if(!r.ok)throw Error("Integrated evidence rejected ("+r.status+").");return r.json();
}).then(value=>{
 if(!value.available){show("status","Not configured");return;}
 data=value;window.koraHeroHybridState=value;
 show("status",value.accepted_outcome?"Objective pass":"Incomplete");
 show("boundary",value.claim_boundary);
 show("calls","Mac "+value.mac.model_calls+" + H100 "+value.h100.model_calls);
 show("providers",value.commercial_provider_calls);
 show("restored",value.restoration.restored_health?"Health verified":"Pending");
 show("lease",value.restoration.lease_released?"Lease released":"Lease retained");
 show("mac-date",value.mac.recorded_at);show("h100-date",value.h100.recorded_at);
 show("mac-output",JSON.stringify(value.mac.output,null,2));show("h100-output",JSON.stringify(value.h100.output,null,2));
 show("config",JSON.stringify(value.h100.plan,null,2));
 show("usage",JSON.stringify({mac:value.mac.usage,h100:value.h100.usage},null,2));
 show("digests",JSON.stringify(value.source_digests,null,2));
 render();
}).catch(error=>{show("status","Evidence rejected");show("error",error.message);$("error").hidden=false;});
})();
