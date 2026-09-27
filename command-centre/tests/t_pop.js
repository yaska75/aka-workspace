const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 for (const [w,name] of [[1440,'pop.png'],[390,'pop_m.png']]){
 const p=await b.newPage({viewport:{width:w,height:860}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   localStorage.setItem('cc-cards', JSON.stringify({t:{key:'t',title:'My to-do list',source:'todo',items:[{title:'Write email to Dolly about the mini series',when:'2026-09-28',priority:'med'}],pulledAt:new Date().toISOString(),order:-200}}));
   window.__prompts=[];
   const s=(input,o)=>{ window.__prompts.push(input); return new Promise(res=>{ setTimeout(()=>{ o.onText({text:'Sure. What\'s Dolly\'s email, and which mini series pitch should I mention?',delta:''}); res({text:'Sure. What\'s Dolly\'s email, and which mini series pitch should I mention?',truncated:false}); },100); }); };
   const mcp={callTool:()=>Promise.resolve({payload:{}}),watchTool:()=>()=>{},invalidate:()=>Promise.resolve()};
   window.claude={use:(n)=>Promise.resolve(n==='sample'?s:n==='mcp'?mcp:null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="todo"]');
 await p.click('#cv-todo .mini.claude'); await p.waitForTimeout(400);
 console.log(w,'pop open', await p.isVisible('#pop'), 'ctx', await p.textContent('#popCtx'));
 console.log('bubbles', await p.locator('#pthread .pu').allTextContents(), await p.locator('#pthread .pa').allTextContents());
 const last=await p.evaluate(()=>window.__prompts.at(-1)); console.log('prompt ok', last.at(-1).content.includes('Write email to Dolly'), 'rules first', last[0].content.startsWith('You run'));
 await p.fill('#pask','dolly@example.com, the Alchemist one'); await p.press('#pask','Enter'); await p.waitForTimeout(300);
 console.log('turns', await p.locator('#pthread .pu').count());
 await p.screenshot({path:__dirname+'/../../build/'+name});
 await p.close(); }
 console.log(JSON.stringify(errs)); await b.close();
})();
