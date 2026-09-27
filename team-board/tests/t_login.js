const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[];
 async function open(ctx){ const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
   await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
   await p.exposeFunction('__save',h=>{html=h;});
   await p.addInitScript(()=>{ window.claude={use:(n)=>Promise.resolve(n==='artifact'?{publish:(h)=>{window.__save(h);return Promise.resolve({});}}:null)}; });
   await p.goto('https://todo.test/'); await p.waitForTimeout(600); return p; }
 const Y=await b.newContext({viewport:{width:1440,height:860}}), P=await b.newContext({viewport:{width:390,height:800}});
 let y=await open(Y);
 console.log('locked', await p_(y));
 await y.screenshot({path:__dirname+'/../../build/login1.png'});
 await y.click('#whoList button:has-text("Yasser")'); await y.screenshot({path:__dirname+'/../../build/login2.png'});
 await y.fill('#lgPw','aka1'); await y.fill('#lgPw2','aka2'); await y.click('.lg-form .go'); console.log('mismatch:', await y.textContent('#lgErr'));
 await y.fill('#lgPw2','aka1'); await y.click('.lg-form .go'); await y.waitForTimeout(800);
 console.log('signed in as', await y.textContent('#meBtn'), 'overlay hidden', await y.isHidden('#whoOverlay'));
 await y.waitForTimeout(2500); console.log('saved keys', /"keys":\{"yasser"/.test(html));
 await y.reload(); await y.waitForTimeout(700); console.log('after reload', await y.textContent('#meBtn'), await y.isHidden('#whoOverlay'));
 // pieter on phone
 let p=await open(P);
 await p.click('#whoList button:has-text("Yasser")'); console.log('pieter sees yasser needs password:', await p.textContent('#whoTitle'));
 await p.fill('#lgPw','guess'); await p.click('.lg-form .go'); await p.waitForTimeout(800); console.log('wrong:', await p.textContent('#lgErr'));
 await p.click('.lg-back'); await p.click('#whoList button:has-text("Pieter")'); await p.fill('#lgPw','pp11'); await p.fill('#lgPw2','pp11'); await p.click('.lg-form .go'); await p.waitForTimeout(800);
 console.log('pieter in', await p.textContent('#meBtn')); await p.screenshot({path:__dirname+'/../../build/login_m.png'});
 await p.waitForTimeout(2500);
 // yasser reloads to get pieter key, resets it
 await y.reload(); await y.waitForTimeout(700);
 await y.click('#teamBtn'); const rs=y.locator('.pwreset'); console.log('reset buttons', await rs.count());
 await rs.first().click(); await rs.first().click(); await y.click('#teamDone'); await y.waitForTimeout(2500);
 console.log('pieter key gone', !/"pieter":\{"s"/.test(html));
 await p.reload(); await p.waitForTimeout(700); console.log('pieter signed out', await p.isVisible('#whoOverlay.lock'));
 // yasser sign out & in
 await y.click('#meBtn'); await y.screenshot({path:__dirname+'/../../build/login3.png'}); await y.click('.lg-acts .out'); console.log('locked after sign out', await y.isVisible('#whoOverlay.lock'));
 await y.click('#whoList button:has-text("Yasser")'); await y.fill('#lgPw','aka1'); await y.press('#lgPw','Enter'); await y.waitForTimeout(800); console.log('back in', await y.textContent('#meBtn'));
 console.log(JSON.stringify(errs)); await b.close();
 async function p_(pg){ return await pg.isVisible('#whoOverlay.lock'); }
})();
