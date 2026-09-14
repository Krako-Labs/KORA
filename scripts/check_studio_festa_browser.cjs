const {chromium}=require(process.env.KORA_PLAYWRIGHT_MODULE||"playwright");
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const base=process.argv[2],output=process.argv[3];
assert.equal(new URL(base).hostname,"127.0.0.1");assert(output);
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const start=Date.now(),browser=await chromium.launch({headless:true});
 const checks=[],errors=[],external=[],mutations=[];
 const check=(name,condition)=>{assert(condition,name);checks.push(name);};
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1080}});
  const page=await context.newPage();
  page.on("pageerror",e=>errors.push(e.message));
  page.on("request",r=>{if(new URL(r.url()).origin!==new URL(base).origin)external.push(r.url());if(r.method()!=="GET")mutations.push(r.method());});
  const ready=()=>page.waitForFunction(()=>window.koraFestaState&&!window.koraFestaState.busy&&!window.koraFestaState.blocked);
  await page.goto(base+"/hero/festa");await ready();
  const initial=await page.evaluate(()=>window.koraFestaState);
  check("locked retained mode",initial.mode==="retained");
  check("new model calls zero",initial.new_model_calls===0);
  check("preflight lock verified",(await page.locator("#lock-status").innerText())==="verified");
  check("source dates visible",(await page.locator("#source-date").innerText()).includes("2026-09"));
  await page.locator("#next").focus();await page.keyboard.press("Enter");
  check("keyboard next event",(await page.evaluate(()=>window.koraFestaState.cursor))===1);
  await page.reload();await ready();
  check("reload resumes identical cursor",(await page.evaluate(()=>window.koraFestaState.cursor))===1);
  await page.locator("#play").click();
  await page.waitForFunction(()=>document.getElementById("outcome").textContent==="Recorded objective pass · historical",{},{timeout:30000});
  check("full retained replay reaches historical objective pass",await page.locator("#next").isDisabled());
  check("split source and review lanes",await page.locator(".lane").count()===3);
  check("all tasks complete",await page.locator('.task[data-state="completed"]').count()===3);
  check("merge answer displayed",(await page.locator("#answer").innerText()).includes("headline"));
  await page.screenshot({path:path.join(output,"retained-desktop.png"),fullPage:true});
  const last=await page.evaluate(()=>window.koraFestaState.cursor);
  await context.setOffline(true);
  await page.waitForFunction(()=>window.koraFestaState.blocked);
  check("offline stops replay",await page.locator("#play").isDisabled());
  check("offline removes success label",(await page.locator("#outcome").innerText()).includes("Unavailable"));
  await page.screenshot({path:path.join(output,"disconnected.png"),fullPage:true});
  await context.setOffline(false);await page.locator("#recover").click();await ready();
  check("one-button recovery preserves cursor",(await page.evaluate(()=>window.koraFestaState.cursor))===last);
  check("recovery labels viewer only",(await page.locator("#notice").innerText()).includes("No new inference"));
  await context.setOffline(true);await page.waitForFunction(()=>window.koraFestaState.blocked);
  await page.locator("#fallback").click();await ready();
  check("explicit cached offline fallback",(await page.evaluate(()=>window.koraFestaState.mode))==="fixture");
  check("fixture visible in persistent mode",(await page.locator("#mode").innerText()).includes("SYNTHETIC"));
  check("fixture source calls unknown",(await page.locator("#source-calls").innerText())==="Not measured");
  while(!(await page.locator("#next").isDisabled()))await page.locator("#next").click();
  check("fixture completion never measured",(await page.locator("#outcome").innerText())==="Fixture completed · not measured");
  await page.screenshot({path:path.join(output,"fixture-desktop.png"),fullPage:true});
  await context.setOffline(false);await page.locator("#retained").click();await ready();
  check("explicit return to retained",(await page.evaluate(()=>window.koraFestaState.mode))==="retained");
  check("fixture cursor not copied to retained",(await page.evaluate(()=>window.koraFestaState.cursor))===0);
  // Inject an old cursor identity; fresh preflight must discard it.
  await page.evaluate(()=>sessionStorage.setItem("kora-festa-replay-v1",JSON.stringify({identity:"old",build:"old",mode:"retained",cursor:15})));
  await page.reload();await ready();
  check("mismatched identity cursor discarded",(await page.evaluate(()=>window.koraFestaState.cursor))===0);
  check("identity change reported",(await page.locator("#notice").innerText()).includes("discarded"));
  // Explicit browser fault injection; this is not a measured source failure.
  const normal=await(await context.request.get(base+"/api/hero/festa")).json();
  for(const reason of ["rejected","not_configured","mismatch"]){
   await page.route("**/api/hero/festa",route=>route.fulfill({json:{...normal,ready:false,retained:null,checks:{...normal.checks,lock:reason}}}));
   await page.locator("#recover").click();
   await page.waitForFunction(()=>window.koraFestaState.blocked&&!window.koraFestaState.busy);
   check("blocked "+reason+" never auto falls back",(await page.evaluate(()=>window.koraFestaState.mode))==="retained");
   check("blocked "+reason+" disables playback",await page.locator("#play").isDisabled());
   await page.unroute("**/api/hero/festa");await page.locator("#recover").click();await ready();
  }
  // Delay one preflight: controls must prevent overlapping source switches.
  let release;
  const gate=new Promise(resolve=>{release=resolve;});
  await page.route("**/api/hero/festa",async route=>{await gate;await route.continue();});
  await page.locator("#recover").click();
  check("inflight recovery disables fallback",await page.locator("#fallback").isDisabled());
  check("inflight recovery disables second recovery",await page.locator("#recover").isDisabled());
  release();await ready();await page.unroute("**/api/hero/festa");
  await page.emulateMedia({reducedMotion:"reduce"});
  await page.setViewportSize({width:390,height:844});
  check("mobile no overflow",await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check("reduced motion active",await page.evaluate(()=>matchMedia("(prefers-reduced-motion: reduce)").matches));
  await page.screenshot({path:path.join(output,"retained-mobile.png"),fullPage:true});
  await page.locator("#fallback").click();await ready();
  check("mobile fixture no overflow",await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:path.join(output,"fixture-mobile.png"),fullPage:true});
  check("no uncaught browser errors",errors.length===0);check("no external requests",external.length===0);check("no mutating requests",mutations.length===0);
  fs.writeFileSync(path.join(output,"rehearsal.json"),JSON.stringify({checks,elapsed_ms:Date.now()-start,software_sha256:normal.software_sha256,retained_identity:normal.retained.identity,fixture_identity:normal.fixture.identity,new_model_calls:0,rehearsal_mode:"retained_replay_and_explicit_fixture",fault_injection:"browser network emulation and rejected preflight responses",errors,external,mutations,human_visual_review:false},null,2)+"\n");
  console.log("Festa rehearsal: "+checks.length+" checks passed");
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
