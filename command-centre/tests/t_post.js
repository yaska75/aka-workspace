const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   localStorage.setItem('cc-cards', JSON.stringify({'posting-rhythm':{key:'posting-rhythm',title:'Posting rhythm',source:'social',summary:'Aim: one post a week on each.',items:[{title:'LinkedIn',lastPost:'2026-09-21',lastPostTitle:'DIFF is coming back.',url:'https://www.linkedin.com/in/me/recent-activity/all/'},{title:'Instagram',lastPost:'2026-09-20',lastPostTitle:'This photo takes me back.',url:'https://www.instagram.com/yas.obeid/'}],pulledAt:new Date().toISOString(),order:-70}}));
   window.__prompts=[]; const s=(i,o)=>{window.__prompts.push(i); return new Promise(()=>{});};
   const mcp={callTool:()=>Promise.resolve({payload:{}}),watchTool:()=>()=>{},invalidate:()=>Promise.resolve()}; window.claude={use:(n)=>Promise.resolve(n==='sample'?s:n==='mcp'?mcp:null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 console.log('pill', await p.isVisible('#postPill'), await p.textContent('#postPill'));
 console.log('badge', await p.textContent('.dk[data-sec="social"] .n'));
 await p.click('#postPill'); await p.waitForTimeout(300);
 console.log(await p.locator('#cv-social .item').allInnerTexts());
 await p.screenshot({path:__dirname+'/../../build/post.png'});
 await p.locator('#cv-social .item').nth(1).locator('text=I just posted').click(); await p.waitForTimeout(200);
 console.log('after', await p.isVisible('#postPill'), (await p.locator('#cv-social .item').nth(1).innerText()).split('\n').slice(0,2));
 await p.locator('#cv-social .item').nth(0).locator('text=Draft a post').click(); await p.waitForTimeout(300);
 await p.waitForTimeout(800); console.log('pop', await p.isVisible('#pop'), await p.locator('#pthread').innerText()); const last=await p.evaluate(()=>window.__prompts.at(-1)); console.log('prompt', last && last.at(-1).content.slice(0,160));
 console.log(JSON.stringify(errs)); await b.close();
})();
