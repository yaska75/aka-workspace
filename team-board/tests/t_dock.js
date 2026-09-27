const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[];
 const ctx=await b.newContext({viewport:{width:1440,height:900}});
 const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.exposeFunction('__save', h=>{html=h;});
 await p.addInitScript(() => {
   window.claude = { use: function(n){ return Promise.resolve(n === 'artifact' ? {publish:function(h){window.__save(h);return Promise.resolve({});}} : null); } };
 });
 await p.goto('https://todo.test/'); await p.waitForTimeout(500);
 // sign in as Yasser
 await p.click('#whoList button:has-text("Yasser")'); await p.fill('#lgPw','aka1'); await p.fill('#lgPw2','aka1'); await p.click('.lg-form .go'); await p.waitForTimeout(400);
 console.log('chat panel visible on wide screen after sign-in', await p.isVisible('#chatPanel'));
 console.log('body has chat-on class', await p.evaluate(()=>document.body.classList.contains('chat-on')));
 const wrapMR = await p.locator('.wrap').evaluate(el=>getComputedStyle(el).marginRight);
 console.log('wrap reserves space for docked panel', wrapMR);

 // narrow viewport: should NOT auto-open on reload as a fresh (no-pref) session
 const freshHtml = fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const ctx2=await b.newContext({viewport:{width:600,height:900}});
 const p2=await ctx2.newPage(); p2.on('pageerror',e=>errs.push(e.message));
 await p2.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:freshHtml}));
 await p2.addInitScript(() => { window.claude = { use: function(){ return Promise.resolve(null); } }; });
 await p2.goto('https://todo.test/'); await p2.waitForTimeout(500);
 await p2.click('#whoList button:has-text("Pieter")'); await p2.fill('#lgPw','pp11'); await p2.fill('#lgPw2','pp11'); await p2.click('.lg-form .go'); await p2.waitForTimeout(400);
 console.log('chat panel hidden on narrow screen after sign-in', await p2.isHidden('#chatPanel'));

 // user can still explicitly close the docked panel on wide screen, and it stays closed on reload
 await p.click('#chatClose'); await p.waitForTimeout(200);
 console.log('closed after clicking Close', await p.isHidden('#chatPanel'));
 await p.reload(); await p.waitForTimeout(500);
 console.log('stays closed after reload (explicit pref respected)', await p.isHidden('#chatPanel'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
