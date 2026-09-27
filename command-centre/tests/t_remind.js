const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{
   localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})}));
   localStorage.setItem('cc-cards', JSON.stringify({t:{key:'t',title:'My to-do list',source:'todo',items:[
     {title:'Call the printer about the poster', when:'2026-09-27', priority:'high'}
   ],pulledAt:new Date().toISOString(),order:-200}}));
   window.claude={use:()=>Promise.resolve(null)};
 });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 await p.click('.dk[data-sec="todo"]');

 // open the remind picker
 await p.click('#cv-todo .item .rembtn'); await p.waitForTimeout(150);
 console.log('picker open', await p.isVisible('#rempick'));
 console.log('picker title', await p.textContent('#rempickTitle'));
 console.log('clear hidden (no reminder yet)', await p.isHidden('#rempickClear'));

 // set a custom time 2 seconds from now so we can watch it fire
 const soon = new Date(Date.now() + 2000);
 const pad = n => String(n).padStart(2, '0');
 const val = soon.getFullYear() + '-' + pad(soon.getMonth() + 1) + '-' + pad(soon.getDate()) + 'T' + pad(soon.getHours()) + ':' + pad(soon.getMinutes());
 await p.fill('#rempickCustom', val);
 await p.click('#rempickSet'); await p.waitForTimeout(150);
 console.log('picker closed after set', await p.isHidden('#rempick'));
 console.log('remind button marked set', await p.getAttribute('#cv-todo .item .rembtn', 'class'));

 // re-open: clear button should now show, since a reminder exists
 await p.click('#cv-todo .item .rembtn'); await p.waitForTimeout(150);
 console.log('clear visible (reminder exists)', await p.isVisible('#rempickClear'));
 await p.click('#rempickCancel'); await p.waitForTimeout(150);

 // wait for the alarm to fire (checker runs every 5s)
 await p.waitForTimeout(6500);
 console.log('alarm visible', await p.isVisible('#alarm'));
 console.log('alarm title', await p.textContent('#alarmTitle'));
 console.log('item flashing', await p.locator('#cv-todo .item.ringing').count());

 // snooze: alarm closes, item stops flashing, reminder still marked set
 await p.click('#alarmSnooze'); await p.waitForTimeout(200);
 console.log('alarm hidden after snooze', await p.isHidden('#alarm'));
 console.log('item stopped flashing after snooze', await p.locator('#cv-todo .item.ringing').count());
 console.log('still marked set after snooze', await p.getAttribute('#cv-todo .item .rembtn', 'class'));

 // set another near-term reminder (the snooze one is 10 min out, too slow to wait for) and let it ring, then Stop clears it entirely
 await p.click('#cv-todo .item .rembtn'); await p.waitForTimeout(150);
 const soon2 = new Date(Date.now() + 2000);
 const val2 = soon2.getFullYear() + '-' + pad(soon2.getMonth() + 1) + '-' + pad(soon2.getDate()) + 'T' + pad(soon2.getHours()) + ':' + pad(soon2.getMinutes());
 await p.fill('#rempickCustom', val2);
 await p.click('#rempickSet'); await p.waitForTimeout(150);
 await p.waitForTimeout(6000);
 console.log('alarm visible again', await p.isVisible('#alarm'));
 await p.click('#alarmStop'); await p.waitForTimeout(200);
 console.log('alarm hidden after stop', await p.isHidden('#alarm'));
 console.log('reminder cleared after stop', await p.getAttribute('#cv-todo .item .rembtn', 'class'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
