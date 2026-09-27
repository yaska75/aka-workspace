const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 const p=await b.newPage({viewport:{width:1440,height:900}, timezoneId:'America/Edmonton'}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{ window.claude={use:()=>Promise.resolve(null)}; });
 await p.goto('https://cc.test/'); await p.waitForTimeout(500);
 console.log('local label', await p.textContent('#bcLocalLabel'));
 console.log('local time looks like HH:MM', /^\d{2}:\d{2}$/.test(await p.textContent('#bcLocal')));
 console.log('dubai time looks like HH:MM', /^\d{2}:\d{2}$/.test(await p.textContent('#bcDubai')));
 // Dubai (UTC+4) should read ahead of Edmonton (UTC-6/-7) at any time of day
 const [lh, lm] = (await p.textContent('#bcLocal')).split(':').map(Number);
 const [dh, dm] = (await p.textContent('#bcDubai')).split(':').map(Number);
 console.log('dubai is ahead of local', ((dh * 60 + dm) - (lh * 60 + lm) + 1440) % 1440 > 500);

 // manual override: device timezone is wrong (says Edmonton) but user is really in Toronto
 await p.click('#bcEditBtn'); await p.waitForTimeout(150);
 console.log('picker open', await p.isVisible('#bcPick'));
 await p.fill('#bcPickCity', 'Toronto');
 console.log('tz picker hidden for known city', await p.isHidden('#bcPickTz'));
 await p.click('#bcPickSave'); await p.waitForTimeout(150);
 console.log('label after override', await p.textContent('#bcLocalLabel'));
 console.log('picker closed', await p.isHidden('#bcPick'));

 // persists after reload
 await p.reload(); await p.waitForTimeout(500);
 console.log('label survives reload', await p.textContent('#bcLocalLabel'));

 // unknown city falls back to a manual timezone select
 await p.click('#bcEditBtn'); await p.waitForTimeout(150);
 await p.fill('#bcPickCity', 'Somewhere Remote');
 console.log('tz picker shown for unknown city', await p.isVisible('#bcPickTz'));
 await p.selectOption('#bcPickTz', 'America/Toronto');
 await p.click('#bcPickSave'); await p.waitForTimeout(150);
 console.log('label after custom tz', await p.textContent('#bcLocalLabel'));

 await p.screenshot({path:__dirname+'/../../build/clocks.png', clip:{x:0,y:0,width:1440,height:900}});
 console.log('errors', JSON.stringify(errs)); await b.close();
})();
