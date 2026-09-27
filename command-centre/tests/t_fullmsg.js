const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   localStorage.setItem('cc-cards', JSON.stringify({'linkedin-inbox':{key:'linkedin-inbox',title:'LinkedIn messages',source:'social',items:[
     {title:'Priya Menon', subtitle:'Asking about a shoot quote', body:'Hi Yasser, following up on the Dubai shoot quote we discussed — can you confirm the day rate and whether the drone add-on is included? Need to lock this in by Friday.', when:'2026-09-26', priority:'high', url:'https://www.linkedin.com/messaging/', linkLabel:'Open LinkedIn ↗'},
     {title:'Sam Cold Outreach', subtitle:'Selling SEO services', when:'2026-09-20', priority:'low', url:'https://www.linkedin.com/messaging/', linkLabel:'Open LinkedIn ↗'}
   ],pulledAt:new Date().toISOString(),order:-90}}));
   window.__prompts=[]; const s=(convo,o)=>{ window.__prompts.push(convo[convo.length-1] && convo[convo.length-1].content); var t='Got it.'; o&&o.onText&&o.onText({text:t,delta:t}); return Promise.resolve({text:t,truncated:false}); };
   window.claude={use:(n)=>Promise.resolve(n==='sample'?s:n==='mcp'?{callTool:()=>Promise.resolve({}),watchTool:()=>()=>{},invalidate:()=>Promise.resolve()}:null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="social"]');

 // item with a full message: "Read full message" toggles the exact text
 const priyaItem = p.locator('#cv-social .item', { hasText: 'Priya Menon' });
 console.log('full message hidden by default', await priyaItem.locator('.itembody').isHidden());
 await priyaItem.locator('.mini.fullmsg').click(); await p.waitForTimeout(150);
 console.log('full message shown', await priyaItem.locator('.itembody').isVisible(), await priyaItem.locator('.itembody').textContent());
 console.log('button now says hide', await priyaItem.locator('.mini.fullmsg').textContent());
 await priyaItem.locator('.mini.fullmsg').click(); await p.waitForTimeout(150);
 console.log('full message hidden again', await priyaItem.locator('.itembody').isHidden());

 // "Do it with Claude" on the item with a body: prompt should carry the exact text, no "ask me to paste"
 await priyaItem.locator('.mini.claude:has-text("Do it with Claude")').click(); await p.waitForTimeout(200);
 const pr1 = await p.evaluate(()=>window.__prompts[0]);
 console.log('prompt has exact body', pr1.includes('day rate and whether the drone add-on is included'));
 console.log('prompt has no paste hedge', !pr1.includes('ask me to paste'));
 await p.click('#popClose');

 // item without a body: falls back to the old "ask me to paste" behaviour
 const samItem = p.locator('#cv-social .item', { hasText: 'Sam Cold Outreach' });
 console.log('no full-message button when there is no body', await samItem.locator('.mini.fullmsg').count());
 await samItem.locator('.mini.claude:has-text("Do it with Claude")').click(); await p.waitForTimeout(200);
 const pr2 = await p.evaluate(()=>window.__prompts[1]);
 console.log('fallback prompt asks to paste', pr2.includes('ask me to paste'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
