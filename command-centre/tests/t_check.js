const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   window.__calls=[]; window.__json=0;
   const s=(input,o)=>new Promise(res=>{ setTimeout(async()=>{
       const t=o.tools.find(x=>x.name==='propose_draft');
       const r=await t.execute({mailbox:'gmail',kind:'reply',to:['sam@example.com'],subject:'Re: Call',body:'Hi Sam,\nTuesday at 3pm works. I\'ll send the budget by Friday.\nYasser',threadId:'th1',replyToMessageId:'m9',basis:'Sam asked: free Tuesday for a call? Yasser said yes 3pm.'},{signal:new AbortController().signal});
       o.onText({text:'Draft is ready for your review below.',delta:''}); res({text:'Draft is ready for your review below.',truncated:false}); },50); });
   s.json=(prompt)=>{ window.__json++; const bad=prompt.includes('Names, dates')||prompt.includes('every date'); return new Promise(r=>setTimeout(()=>r(bad?{ok:false,issues:['"send the budget by Friday" is a promise not in the source']}:{ok:true,issues:[]}),80)); };
   const mcp={callTool:(sv,t,i)=>{ window.__calls.push([sv,t,i]); if(t==='get_thread') return Promise.resolve({payload:{messages:[{sender:'sam@example.com',toRecipients:['yasser.khasan@gmail.com'],date:'2026-09-26',subject:'Call',plaintextBody:'Free Tuesday for a call?'}]}}); return Promise.resolve({payload:{viewUrl:'https://mail.google.com/mail/#drafts/abc'}}); },watchTool:()=>()=>{},invalidate:()=>Promise.resolve()};
   window.claude={use:(n)=>Promise.resolve(n==='sample'?s:n==='mcp'?mcp:null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('#fab'); await p.fill('#pask','Reply to Sam yes Tuesday 3pm'); await p.press('#pask','Enter');
 await p.waitForTimeout(900);
 console.log('checks run', await p.evaluate(()=>window.__json), 'rows', await p.locator('.rev .ck').allTextContents());
 console.log('status', await p.textContent('.revst'), 'save label', await p.textContent('.rev .psend'));
 console.log('saved before click?', JSON.stringify(await p.evaluate(()=>window.__calls.map(c=>c[1]))));
 await p.screenshot({path:__dirname+'/check.png'});
 await p.click('.rev .psend'); await p.waitForTimeout(300);
 console.log('after save', JSON.stringify(await p.evaluate(()=>window.__calls.map(c=>c[1]))), await p.textContent('.revst'));
 // writer path
 await p.click('#popClose'); await p.click('.dk[data-sec="claude"]'); await p.click('#rw summary');
 await p.fill('#rwIn','Can we meet Tuesday?'); 
 await p.evaluate(()=>{ const s=window.claude; });
 console.log(JSON.stringify(errs)); await b.close();
})();
