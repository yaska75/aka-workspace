const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[]; const pages=[];
 async function open(ctx, tz){
   const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
   await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
   await p.exposeFunction('__save', h=>{html=h;});
   p.__notifs = [];
   await p.exposeFunction('__notifCreated', (title, body) => { p.__notifs.push({title, body}); });
   await p.addInitScript(() => {
     window.claude = { use: function(n){ return Promise.resolve(n === 'artifact' ? {publish:function(h){window.__save(h);return Promise.resolve({});}} : null); } };
     // Mock the Notification API: auto-grant permission, and record every notification created.
     window.Notification = function(title, opts){ window.__notifCreated(title, (opts||{}).body); this.onclick = null; this.close = function(){}; };
     window.Notification.permission = localStorage.getItem('__mock_notif_perm') || 'default';
     window.Notification.requestPermission = function(){
       window.Notification.permission = 'granted'; localStorage.setItem('__mock_notif_perm', 'granted'); return Promise.resolve('granted');
     };
   });
   await p.goto('https://todo.test/'); await p.waitForTimeout(500);
   pages.push(p);
   return p;
 }
 // Daytime Dubai context (~13:00 local -> well within the 9-21 window regardless of host TZ, since the app reads Asia/Dubai explicitly)
 const Y=await b.newContext({viewport:{width:1440,height:900}});
 const P=await b.newContext({viewport:{width:1440,height:900}});
 const y=await open(Y);
 await y.click('#whoList button:has-text("Yasser")'); await y.fill('#lgPw','aka1'); await y.fill('#lgPw2','aka1'); await y.click('.lg-form .go'); await y.waitForTimeout(400);

 const p=await open(P);
 await p.click('#whoList button:has-text("Pieter")'); await p.fill('#lgPw','pp11'); await p.fill('#lgPw2','pp11'); await p.click('.lg-form .go'); await p.waitForTimeout(400);

 // Pieter turns notifications on for this device
 await p.click('#notifBtn'); await p.waitForTimeout(150);
 console.log('notif button pressed after opt-in', await p.getAttribute('#notifBtn', 'aria-pressed'));
 // the opt-in confirmation notification itself
 console.log('confirmation notification shown', p.__notifs.length > 0);

 // Pieter backgrounds his tab (so a real notification would be useful) and Yasser gives him a task
 p.__notifs = [];
 await p.evaluate(() => { Object.defineProperty(document, 'hidden', { value: true, configurable: true }); document.dispatchEvent(new Event('visibilitychange')); });
 await y.click('#col-pieter .foldBtn'); // Pieter's column is folded by default on Yasser's screen; open it first
 await y.click('#col-pieter .newText'); await y.fill('#col-pieter .newText', 'Send the Q4 budget to finance');
 await y.click('#col-pieter .addBtn'); await y.waitForTimeout(2000);

 // simulate the periodic resync: reload Pieter's page against the freshly saved html
 await new Promise(r => setTimeout(r, 300));
 await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.reload();
 await p.evaluate(() => { Object.defineProperty(document, 'hidden', { value: true, configurable: true }); });
 await p.waitForTimeout(600);
 console.log('task notification fired (daytime, tab hidden)', p.__notifs.some(n => /Q4 budget/.test(n.body)));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
