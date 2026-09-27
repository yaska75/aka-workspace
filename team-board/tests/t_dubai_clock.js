const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[];
 const ctx=await b.newContext({viewport:{width:1440,height:900}, timezoneId:'America/Toronto'});
 const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.exposeFunction('__save', h=>{html=h;});
 await p.addInitScript(() => { window.claude = { use: function(n){ return Promise.resolve(n === 'artifact' ? {publish:function(h){window.__save(h);return Promise.resolve({});}} : null); } }; });
 await p.goto('https://todo.test/'); await p.waitForTimeout(500);
 await p.click('#whoList button:has-text("Yasser")'); await p.fill('#lgPw','aka1'); await p.fill('#lgPw2','aka1'); await p.click('.lg-form .go'); await p.waitForTimeout(400);

 // Yasser sets his own location manually to Toronto
 await p.click('#col-yasser .where'); await p.waitForTimeout(150);
 await p.fill('#col-yasser .where-edit input', 'Toronto');
 await p.click('#col-yasser .where-edit .primary'); await p.waitForTimeout(300);
 console.log('location set', await p.textContent('#col-yasser .where b'));
 console.log('local clock shown', await p.isVisible('#col-yasser .clock:not(.dubai)'));
 console.log('dubai comparison clock shown', await p.isVisible('#col-yasser .clock.dubai'));
 console.log('dubai clock text', await p.textContent('#col-yasser .clock.dubai'));

 // Someone already in Dubai shouldn't see a redundant "Dubai" comparison badge
 await p.click('#col-yasser .where'); await p.waitForTimeout(150);
 await p.fill('#col-yasser .where-edit input', 'Dubai');
 await p.click('#col-yasser .where-edit .primary'); await p.waitForTimeout(300);
 console.log('dubai comparison hidden when already in Dubai', await p.isHidden('#col-yasser .clock.dubai'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
