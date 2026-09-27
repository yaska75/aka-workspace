const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   if(!localStorage.getItem('cc-cards')) localStorage.setItem('cc-cards', JSON.stringify({t:{key:'t',title:'My to-do list',source:'todo',items:[
     {title:'Write email to Dolly', when:'2026-09-28', priority:'med'},
     {title:'Call the printer about the poster', when:'2026-09-27', priority:'high'},
     {title:'Book flights for Berlin', when:'2026-09-29', priority:'low'}
   ],pulledAt:new Date().toISOString(),order:-200}}));
   window.claude={use:()=>Promise.resolve(null)}; // no db -> memOnly, localStorage-backed
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="todo"]');
 console.log('badge before', await p.textContent('.dk[data-sec="todo"] .n'));
 console.log('items before', await p.locator('#cv-todo .item b').allTextContents());

 // pin "Call the printer"
 const printerItem = p.locator('#cv-todo .item', { hasText: 'Call the printer about the poster' });
 await printerItem.locator('.pinhide .pin').click(); await p.waitForTimeout(300);
 console.log('order after pin (pinned should be first)', await p.locator('#cv-todo .item b').allTextContents());
 console.log('pinned class', await printerItem.evaluate(el=>el.className));

 // hide "Book flights for Berlin"
 const flightsItem = p.locator('#cv-todo .item', { hasText: 'Book flights for Berlin' });
 await flightsItem.locator('.pinhide .hide').click(); await p.waitForTimeout(300);
 console.log('hidden class', await flightsItem.evaluate(el=>el.className));
 console.log('badge after hide (low-priority hide, count unaffected as expected)', await p.textContent('.dk[data-sec="todo"] .n'));
 console.log('order after hide (hidden should be last)', await p.locator('#cv-todo .item b').allTextContents());
 console.log('acts hidden for collapsed item', await flightsItem.locator('.acts').isHidden());

 // reload: flags persisted via localStorage cc-flags
 await p.reload(); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="todo"]');
 const flightsItem2 = p.locator('#cv-todo .item', { hasText: 'Book flights for Berlin' });
 console.log('still hidden after reload', await flightsItem2.evaluate(el=>el.className));
 console.log('badge after reload', await p.textContent('.dk[data-sec="todo"] .n'));

 // simulate a scheduled-task resync: card wholesale-overwritten (new items array), flags must survive since they're keyed separately
 await p.evaluate(()=>{
   const cards = JSON.parse(localStorage.getItem('cc-cards'));
   cards.t.items.push({title:'New task from the sync', when:'2026-09-30', priority:'med'});
   cards.t.pulledAt = new Date().toISOString();
   localStorage.setItem('cc-cards', JSON.stringify(cards));
 });
 await p.reload(); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="todo"]');
 console.log('items after resync', await p.locator('#cv-todo .item b').allTextContents());
 const flightsItem3 = p.locator('#cv-todo .item', { hasText: 'Book flights for Berlin' });
 console.log('still hidden after simulated resync', await flightsItem3.evaluate(el=>el.className));
 console.log('new synced item shows normally', await p.locator('#cv-todo .item', { hasText: 'New task from the sync' }).evaluate(el=>el.className));

 // unhide restores full display
 await flightsItem3.locator('.pinhide .hide').click(); await p.waitForTimeout(300);
 const flightsItem4 = p.locator('#cv-todo .item', { hasText: 'Book flights for Berlin' });
 console.log('unhidden class', await flightsItem4.evaluate(el=>el.className));
 console.log('acts visible again', await flightsItem4.locator('.acts').isVisible());
 console.log('badge after unhide', await p.textContent('.dk[data-sec="todo"] .n'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
