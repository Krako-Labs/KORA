const {chromium}=require(process.env.KORA_PLAYWRIGHT_MODULE||"playwright");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const base=process.argv[2]||"http://127.0.0.1:8799";
const output=process.argv[3]||"/tmp/kora-hybrid-qc";
assert.equal(new URL(base).hostname,"127.0.0.1");
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try {
 const context=await browser.newContext({viewport:{width:1440,height:1080}});
 const page=await context.newPage();
 const errors=[],external=[],mutations=[];
 page.on("pageerror",e=>errors.push(e.message));
 page.on("console",m=>{if(m.type()==="error")errors.push(m.text());});
 page.on("request",r=>{
  if(new URL(r.url()).origin!==new URL(base).origin)external.push(r.url());
  if(r.method()!=="GET")mutations.push(r.method());
 });
 await page.goto(base+"/hero/hybrid");
 await page.waitForFunction(()=>window.koraHeroHybridState?.available);
 const state=await page.evaluate(()=>window.koraHeroHybridState);
 assert.equal(state.accepted_outcome,true);
 assert.equal(state.h100.privacy_mode,"private_network");
 assert.equal(state.mac.mode,"retained_observed");
 assert.equal(state.commercial_provider_calls,0);
 assert.equal(state.semantic_quality,"not_measured");
 assert.equal(state.restoration.lease_released,true);
 assert.equal(await page.locator("#status").innerText(),"Objective pass");
 assert.match(await page.locator("#boundary").innerText(),/Sequential/);
 assert.match(await page.locator("#mac-output").innerText(),/headline/);
 assert.match(await page.locator("#h100-output").innerText(),/headline/);
 assert.equal(await page.locator("#previous").isDisabled(),true);
 await page.locator("#next").focus();
 await page.keyboard.press("Enter");
 assert.match(await page.locator("#cursor").innerText(),/^2 \/ /);
 await page.locator("#end").click();
 assert.equal(await page.locator("#tasks li").count(),3);
 assert.equal(await page.locator("#next").isDisabled(),true);
 assert((await page.locator("#tasks").innerText()).includes("completed"));
 assert.deepEqual(await(await context.request.get(base+"/api/hero/hybrid")).json(),state);
 await page.screenshot({path:path.join(output,"hybrid-desktop.png"),fullPage:true,animations:"disabled"});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:path.join(output,"hybrid-mobile.png"),fullPage:true,animations:"disabled"});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
 assert.equal(overflow,false,"no horizontal overflow on mobile");
 assert.equal(errors.length,0);assert.equal(external.length,0);assert.equal(mutations.length,0);
 fs.writeFileSync(path.join(output,"summary.json"),JSON.stringify({
  checks:20,run_id:state.run_id,mac_calls:state.mac.model_calls,h100_calls:state.h100.model_calls,
  errors,external,mutations,mobile_overflow:overflow},null,2)+"\n");
 console.log("Hybrid browser QC: 20 checks passed");
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
