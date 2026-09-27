const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[]; const pages=[];
 async function open(ctx){
   const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
   await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
   await p.exposeFunction('__save', h=>{html=h;});
   await p.exposeFunction('__roomEmit', (event, data) => {
     pages.forEach(other => { if(other !== p){ other.evaluate(function(args){ if(window.__roomDeliver) window.__roomDeliver(args.ev, args.d); }, { ev: event, d: data }).catch(()=>{}); } });
     return Promise.resolve();
   });
   await p.addInitScript(() => {
     window.__roomListeners = {};
     window.__roomDeliver = function(event, data){ (window.__roomListeners[event]||[]).forEach(function(cb){ cb({data:data, sameTab:false}); }); };
     var roomObj = {
       emit: function(event, data){ return window.__roomEmit(event, data); },
       on: function(event, cb){ window.__roomListeners[event] = window.__roomListeners[event] || []; window.__roomListeners[event].push(cb); }
     };
     window.claude = { use: function(n){ return Promise.resolve(n === 'artifact' ? {publish:function(h){window.__save(h);return Promise.resolve({});}} : n === 'room' ? roomObj : null); } };
   });
   await p.goto('https://todo.test/'); await p.waitForTimeout(600);
   pages.push(p);
   return p;
 }
 const Y=await b.newContext({viewport:{width:1440,height:900}}), P=await b.newContext({viewport:{width:1440,height:900}});
 const y=await open(Y);
 await y.click('#whoList button:has-text("Yasser")'); await y.fill('#lgPw','aka1'); await y.fill('#lgPw2','aka1'); await y.click('.lg-form .go'); await y.waitForTimeout(400);

 const p=await open(P);
 await p.click('#whoList button:has-text("Pieter")'); await p.fill('#lgPw','pp11'); await p.fill('#lgPw2','pp11'); await p.click('.lg-form .go'); await p.waitForTimeout(600);

 // presence: both signed in with visible tabs -> both should show Online to each other
 console.log('yasser sees pieter presence', await y.locator('#col-pieter .presence').textContent());
 console.log('pieter sees yasser presence', await p.locator('#col-yasser .presence').textContent());

 // Pieter backgrounds his tab -> Yasser should see him go Asleep
 await p.evaluate(() => {
   Object.defineProperty(document, 'hidden', { value: true, configurable: true });
   document.dispatchEvent(new Event('visibilitychange'));
 });
 await y.waitForTimeout(400);
 console.log('yasser sees pieter asleep after backgrounding', await y.locator('#col-pieter .presence').textContent());

 // Pieter returns -> Online again
 await p.evaluate(() => {
   Object.defineProperty(document, 'hidden', { value: false, configurable: true });
   document.dispatchEvent(new Event('visibilitychange'));
 });
 await y.waitForTimeout(400);
 console.log('yasser sees pieter online again', await y.locator('#col-pieter .presence').textContent());

 // Urgent chat: Yasser DMs Pieter with the urgent toggle on -> Pieter gets a full alarm
 if(await y.isHidden('#chatPanel')) await y.click('#chatBtn');
 await y.click('.chan:has-text("Pieter")').catch(async()=>{ /* fallback: open chat list if channel switcher differs */ });
 await y.fill('#chatText', 'Need you on a call now');
 await y.click('#urgentBtn');
 console.log('urgent toggled on', await y.getAttribute('#urgentBtn', 'aria-pressed'));
 await y.click('#composer button[type=submit]');
 await y.waitForTimeout(600);
 console.log('urgent resets after send', await y.getAttribute('#urgentBtn', 'aria-pressed'));
 console.log('pieter alarm visible', await p.isVisible('#alarmBox'));
 console.log('alarm text', (await p.textContent('#alarmBox .msgtxt').catch(()=>'')) || '');
 if(await p.isVisible('#alarmBox')) await p.click('#alarmBox .ack');
 await p.waitForTimeout(200);
 console.log('alarm dismissed', await p.isHidden('#alarmBox'));

 // Task progress + note
 await y.click('#col-yasser .newText'); await y.fill('#col-yasser .newText', 'Draft Q4 budget');
 await y.click('#col-yasser .addBtn'); await y.waitForTimeout(200);
 const item = y.locator('#col-yasser .item', { hasText: 'Draft Q4 budget' });
 console.log('progress bar starts at 0%', await item.locator('.pct').textContent());
 await item.locator('input[type=range]').fill('60');
 await item.locator('input[type=range]').dispatchEvent('change');
 await y.waitForTimeout(200);
 console.log('progress after set', await item.locator('.pct').textContent());
 console.log('bar fill width', await item.locator('.bar-fill').evaluate(el => el.style.width));

 await item.locator('button:has-text("Add note")').click(); await y.waitForTimeout(150);
 await item.locator('.noteedit textarea').fill('Waiting on finance numbers from Srijeeth');
 await item.locator('.noteedit button:has-text("Save note")').click(); await y.waitForTimeout(200);
 console.log('note saved and shown', await item.locator('.tasknote').textContent());
 console.log('note button now says Edit note', await item.locator('button:has-text("Edit note")').count());

 // reload: progress + note persist (state is embedded, but this session's html var was updated via __save on debounced save)
 await y.waitForTimeout(2000);
 console.log('progress persisted in saved html', /"progress":60/.test(html));
 console.log('note persisted in saved html', /Waiting on finance numbers/.test(html));

 // Remove from list: requires a confirm tap, then the task disappears
 console.log('remove button label', await item.locator('button.del').textContent());
 await item.locator('button.del').click(); await y.waitForTimeout(150);
 console.log('remove button confirms', await item.locator('button.del').textContent());
 await item.locator('button.del').click(); await y.waitForTimeout(300);
 console.log('task gone after confirming remove', await y.locator('#col-yasser .item', { hasText: 'Draft Q4 budget' }).count());

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
