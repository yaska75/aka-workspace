const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   const cards={};
   window.__actions=[];
   const listeners=[];
   const snap=()=>({docs:Object.keys(cards).map(k=>({id:k,data:()=>cards[k]}))});
   const db={collection:(n)=>({onSnapshot:(cb)=>{ if(n==='cards'){listeners.push(cb); setTimeout(()=>cb(snap()),10);} return ()=>{}; }, doc:(id)=>({set:(d)=>{cards[id]=d; listeners.forEach(l=>l(snap())); return Promise.resolve();}, delete:()=>{delete cards[id]; return Promise.resolve();}, get:()=>Promise.resolve({exists:false})}), add:(d)=>{window.__actions.push(d); return Promise.resolve({});}}), doc:(p)=>({get:()=>Promise.resolve({exists:true,data:()=>({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})})}), set:()=>Promise.resolve()})};
   const mcp={callTool:()=>Promise.resolve({payload:{}}), watchTool:()=>()=>{}, invalidate:()=>Promise.resolve()};
   window.claude={use:(n)=>Promise.resolve(n==='db'?db:n==='mcp'?mcp:null)};
   window.__pushCard=(c)=>{ cards[c.key]=c; listeners.forEach(l=>l(snap())); };
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="make"]'); await p.waitForTimeout(200);
 console.log('empty state', await p.textContent('#se-make'));
 // clicking with no brief and no file link should not queue anything
 await p.click('#mkQuoteGo'); await p.waitForTimeout(100);
 console.log('empty-brief note', await p.textContent('#mkQuoteNote'), 'actions', JSON.stringify(await p.evaluate(()=>window.__actions)));
 // a non-Drive link should be rejected without queuing
 await p.fill('#mkQuoteFileLink', 'https://example.com/brief.pdf');
 await p.click('#mkQuoteGo'); await p.waitForTimeout(100);
 console.log('bad-link note', await p.textContent('#mkQuoteNote'), 'actions', JSON.stringify(await p.evaluate(()=>window.__actions)));
 await p.fill('#mkQuoteFileLink', '');
 // now with a real brief
 await p.fill('#mkQuoteBrief', 'Client: Rakan. 2-day shoot, Dubai, 6 crew, drone add-on.');
 await p.click('#mkQuoteGo'); await p.waitForTimeout(150);
 console.log('queued', JSON.stringify(await p.evaluate(()=>window.__actions)));
 console.log('note after queue', await p.textContent('#mkQuoteNote'), 'brief cleared', await p.inputValue('#mkQuoteBrief') === '');
 // a brief-less job with just a Drive file link should also queue
 await p.fill('#mkQuoteFileLink', 'https://drive.google.com/file/d/abc123/view');
 await p.click('#mkQuoteGo'); await p.waitForTimeout(150);
 console.log('queued (file link only)', JSON.stringify(await p.evaluate(()=>window.__actions)));
 console.log('file link cleared', await p.inputValue('#mkQuoteFileLink') === '');
 // simulate the scheduled task coming back with a card
 await p.evaluate(()=>window.__pushCard({key:'make-quote-1', title:'Quote: Rakan', source:'make', summary:'Built from your standard template.', items:[{title:'AKA Quote - Rakan', url:'https://docs.google.com/spreadsheets/d/xyz/edit', linkLabel:'Open the quote ↗', priority:'med'}], pulledAt:new Date().toISOString()}));
 await p.waitForTimeout(150);
 console.log('result card', await p.locator('#cv-make .card h3').allTextContents());
 await p.screenshot({path:__dirname+'/make.png'});
 console.log(JSON.stringify(errs)); await b.close();
})();
