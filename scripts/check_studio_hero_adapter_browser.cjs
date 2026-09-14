/* Localhost-only mock review QC; no model runtime is used. */
const {chromium}=require(process.env.KORA_PLAYWRIGHT_MODULE || "playwright");
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const base=process.argv[2] || "http://127.0.0.1:8796";
const output=process.argv[3] || "/tmp/kora-adapter-review-qc";
assert(["127.0.0.1","localhost"].includes(new URL(base).hostname));
assert.equal(new URL(base).protocol,"http:");
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[],external=[],checks=[];
 page.on("pageerror",e=>errors.push(e.message));
 page.on("request",r=>{if(new URL(r.url()).origin!==new URL(base).origin)external.push(r.url());});
 const state=()=>page.evaluate(()=>window.koraHeroState);
 const ready=()=>page.waitForFunction(()=>!document.querySelector("#step").disabled);
 const step=()=>page.locator("#step").click();
 const api=async s=>(await context.request.get(base+"/api/hero/adapter/events?scenario="+s)).json();
 await page.goto(base+"/hero");
 await ready();
 assert.equal(await page.locator('a[href="/hero/adapter"]').count(),1);
 await page.locator('a[href="/hero/adapter"]').click();
 await ready();
 assert((await page.locator("h1").innerText()).includes("Follow the lifecycle"));
 assert.equal(await page.locator("#adapter-state").innerText(),"Awaiting plan");
 for(let i=0;i<7;i++)await step();
 assert.equal(await page.locator("#adapter-state").innerText(),"running");
 const before=await state(),history=await page.locator("#history").innerText();
 await page.screenshot({path:path.join(output,"adapter-running.png"),fullPage:true,animations:"disabled"});
 await page.reload();await ready();
 assert.deepEqual(await state(),before);
 assert.equal(await page.locator("#history").innerText(),history);
 assert.deepEqual(await state(),(await api("success")).frames[6]);
 checks.push("Opt-in review; partial reload equals canonical frame and retains history");
 await page.locator("#play").click();
 await page.waitForFunction(()=>window.koraHeroState?.event.sequence>=7);
 if(await page.locator("#play").innerText()==="Pause")await page.locator("#play").click();
 const paused=(await state()).event.sequence;
 await page.waitForTimeout(750);assert.equal((await state()).event.sequence,paused);
 checks.push("Play and pause pace canonical mock events");
 while((await state()).event.sequence<9)await step();
 await page.reload();await page.waitForFunction(()=>window.koraHeroState?.view.adapter_state==="closed");
 assert.deepEqual(await state(),(await api("success")).frames.at(-1));
 assert.equal(await page.locator("#adapter-accepted").innerText(),"Not accepted");
 assert((await page.locator("#adapter-telemetry").innerText()).includes("Unavailable"));
 checks.push("Completed reload retains mock output; unknown telemetry stays unavailable; no acceptance");
 const scenarios=["cancelled","load_failed","execute_failed","finish_failed","cleanup_failed_then_retried","placement_unresolved"];
 for(const scenario of scenarios){
   await page.locator("#scenario").selectOption(scenario);await ready();
   const data=await api(scenario);
   for(let i=0;i<data.event_count;i++){
     await step();
     assert.deepEqual(await state(),data.frames[i]);
     if(scenario==="cleanup_failed_then_retried" && i===data.event_count-2){
       assert((await page.locator("#allocation").innerText()).includes("retained"));
       await page.screenshot({path:path.join(output,"adapter-cleanup-failed.png"),fullPage:true,animations:"disabled"});
     }
   }
   assert.equal(await page.locator("#adapter-accepted").innerText(),"Not accepted");
   assert((await page.locator("#allocation").innerText()).includes("No mock"));
   if(scenario==="cleanup_failed_then_retried")assert((await page.locator("#lifecycle").innerText()).includes("adapter.cleanup.failed"));
   if(scenario==="placement_unresolved"){
     assert.equal(await page.locator("#adapter-state").innerText(),"blocked");
     assert((await page.locator("#adapter-reason").innerText()).includes("placement_unresolved"));
     assert.equal(await page.locator("#lifecycle li").count(),0);
     await page.screenshot({path:path.join(output,"adapter-placement-blocked.png"),fullPage:true,animations:"disabled"});
   }
 }
 checks.push("Every frame in all six lifecycle paths and blocked placement equals canonical projection");
 checks.push("Cleanup failure/retry remains visible; blocked placement has no session allocation");
 await page.route("**/api/hero/adapter/sse?*",r=>r.abort());
 await page.locator("#scenario").selectOption("success");await ready();
 await page.waitForFunction(()=>document.querySelector("#transport").textContent.includes("Recovered"));
 for(let i=0;i<6;i++)await step();
 assert.deepEqual(await state(),(await api("success")).frames[5]);
 await page.unroute("**/api/hero/adapter/sse?*");
 checks.push("SSE failure recovers from canonical bounded event endpoint");
 await page.emulateMedia({reducedMotion:"reduce"});
 await page.locator("#step").focus();await page.keyboard.press("Enter");
 assert.equal((await state()).event.sequence,6);
 assert.equal(await page.locator("#lifecycle li").last().evaluate(el=>getComputedStyle(el).animationName),"none");
 checks.push("Keyboard stepping and reduced-motion preference work");
 for(const viewport of [{width:1440,height:1000},{width:1024,height:768},{width:390,height:844}]){
   await page.setViewportSize(viewport);
   await page.locator("summary").click();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),"horizontal overflow");
   for(const id of ["play","step","reset","scenario"]){
     const box=await page.locator("#"+id).boundingBox();
     assert(box && box.width>20 && box.x>=0 && box.x+box.width<=viewport.width+1,id+" clipped");
   }
   if(viewport.width===390)await page.screenshot({path:path.join(output,"adapter-mobile-reduced-motion.png"),fullPage:true,animations:"disabled"});
   await page.locator("summary").click();
 }
 checks.push("Desktop/tablet/mobile controls and expanded identity have no horizontal overflow");
 await page.goto(base+"/hero");await ready();
 assert.equal(await page.locator("#scenario").inputValue(),"apple");
 assert.equal(await page.locator("#adapter-state").count(),0);
 checks.push("Existing Hero fixture view and its saved cursor remain independent");
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
 fs.writeFileSync(path.join(output,"adapter-browser-qc.json"),JSON.stringify({ok:true,checks,errors,external_requests:external,human_visual_review:"not_performed"},null,2)+"\n");
 console.log(JSON.stringify({ok:true,checks},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
