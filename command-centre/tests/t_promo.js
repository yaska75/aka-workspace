const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   const cards={
    t:{key:'t',title:'My to-do list',source:'todo',items:[{title:'Write email to Dolly',when:'2026-09-28',priority:'med'}],pulledAt:new Date().toISOString(),order:-200},
    g:{key:'g',title:'Gmail',source:'gmail',items:[{title:'Promo thing',mailbox:'gmail',threadId:'abc',messageId:'m1',priority:'low'}],pulledAt:new Date().toISOString(),order:-1},
    o:{key:'o',title:'Work inbox',source:'outlook',items:[{title:'LE BOOK wrap',subtitle:'newsletter',when:'2026-09-25',priority:'low'}],pulledAt:new Date().toISOString(),order:-100}};
   window.__calls=[]; window.__actions=[];
   const listeners=[];
   const snap=()=>({docs:Object.keys(cards).map(k=>({id:k,data:()=>cards[k]}))});
   const db={collection:(n)=>({onSnapshot:(cb)=>{ if(n==='cards'){listeners.push(cb); setTimeout(()=>cb(snap()),10);} return ()=>{}; }, doc:(id)=>({set:(d)=>{cards[id]=d; listeners.forEach(l=>l(snap())); return Promise.resolve();}, delete:()=>{delete cards[id]; return Promise.resolve();}, get:()=>Promise.resolve({exists:false})}), add:(d)=>{window.__actions.push(d); return Promise.resolve({});}}), doc:(p)=>({get:()=>Promise.resolve({exists:true,data:()=>({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})})}), set:()=>Promise.resolve()})};
   const mcp={callTool:(s,t,i)=>{window.__calls.push([s,t,i]); return Promise.resolve({payload:{}});}, watchTool:()=>()=>{}, invalidate:()=>Promise.resolve()};
   window.claude={use:(n)=>Promise.resolve(n==='db'?db:n==='mcp'?mcp:null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 console.log('dock', await p.locator('.dk b').allTextContents(), 'todo badge', await p.textContent('.dk[data-sec="todo"] .n'));
 await p.click('.dk[data-sec="todo"]'); await p.click('.dk[data-sec="email"]'); await p.waitForTimeout(200);
 console.log('todo items', await p.locator('#cv-todo .item b').allTextContents());
 await p.click('#cv-email .item:has-text("Promo thing") .mini:has-text("To Promotions")'); await p.waitForTimeout(200);
 console.log('gmail calls', JSON.stringify(await p.evaluate(()=>window.__calls)));
 console.log('gmail item gone', await p.locator('#cv-email .item:has-text("Promo thing")').count());
 await p.click('#cv-email .item:has-text("LE BOOK") .mini:has-text("To Promotions")'); await p.waitForTimeout(200);
 console.log('queued', JSON.stringify(await p.evaluate(()=>window.__actions)), await p.textContent('#cv-email .item:has-text("LE BOOK") .qn'));
 await p.screenshot({path:__dirname+'/promo.png'});
 console.log(JSON.stringify(errs)); await b.close();
})();
