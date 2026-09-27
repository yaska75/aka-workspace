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
 console.log('locked at start', await y.isVisible('#whoOverlay.lock'));
 await y.screenshot({path:__dirname+'/../../build/login1.png'});
 await y.click('#whoList button:has-text("Yasser")'); await y.screenshot({path:__dirname+'/../../build/login2.png'});
 await y.fill('#lgPw','aka1'); await y.fill('#lgPw2','aka2'); await y.click('.lg-form .go'); console.log('mismatch caught:', await y.textContent('#lgErr'));
 await y.fill('#lgPw2','aka1'); await y.click('.lg-form .go'); await y.waitForTimeout(600);
 console.log('signed in as', await y.textContent('#meBtn'), 'overlay hidden', await y.isHidden('#whoOverlay'));
 await y.waitForTimeout(1900); console.log('saved key', /"yasser":\{"pw":"aka1"/.test(html));
 await y.reload(); await y.waitForTimeout(700); console.log('after reload', await y.textContent('#meBtn'), await y.isHidden('#whoOverlay'));

 // Pieter self sign-up on his phone
 let p=await open(P);
 await p.click('#whoList button:has-text("Yasser")'); console.log('picking Yasser shows password prompt:', await p.textContent('#whoTitle'));
 await p.fill('#lgPw','guess'); await p.click('.lg-form .go'); await p.waitForTimeout(600); console.log('wrong password:', await p.textContent('#lgErr'));
 await p.click('.lg-back'); await p.click('#whoList button:has-text("Pieter")'); await p.fill('#lgPw','pp11'); await p.fill('#lgPw2','pp11'); await p.click('.lg-form .go'); await p.waitForTimeout(600);
 console.log('pieter in', await p.textContent('#meBtn')); await p.screenshot({path:__dirname+'/../../build/login_m.png'});
 await p.waitForTimeout(1900);

 // Yasser (superuser) reloads, opens Team panel: sees & can see Pieter's real password (admin, not member)
 await y.reload(); await y.waitForTimeout(700);
 await y.click('#teamBtn');
 const pieterPwField = y.locator('.trow[data-pid="pieter"] .pwcell input');
 console.log('yasser sees pieter pw field value', await pieterPwField.inputValue());
 // Yasser changes Pieter's password directly (not a blind reset)
 await pieterPwField.fill('newpw9'); await pieterPwField.dispatchEvent('change');
 await y.click('#teamDone'); await y.waitForTimeout(1900);
 console.log('new password saved', /"pieter":\{"pw":"newpw9"/.test(html));

 // Pieter's own device reloads: must be forced to re-enter (old remembered password no longer matches)
 // even though his own local ops-queue still holds his original self-signup op (this is the bug we hit before)
 await p.reload(); await p.waitForTimeout(700);
 console.log('pieter locked out after admin changed his pw', await p.isVisible('#whoOverlay.lock'));
 const stillNew = /"pieter":\{"pw":"newpw9"/.test(html);
 console.log('admin-set password survived pieter\'s stale local queue replay', stillNew);
 // sign back in with the NEW password Yasser set
 await p.click('#whoList button:has-text("Pieter")'); await p.fill('#lgPw','newpw9'); await p.click('.lg-form .go'); await p.waitForTimeout(600);
 console.log('pieter back in with admin-set password', await p.textContent('#meBtn'));

 // member (Srijeeth, finance) should NOT be able to see admin/superuser passwords, only member ones
 let s=await open(await b.newContext());
 await s.click('#whoList button:has-text("Srijeeth")'); await s.fill('#lgPw','fin1'); await s.fill('#lgPw2','fin1'); await s.click('.lg-form .go'); await s.waitForTimeout(1900);
 console.log('srijeeth is member, teamBtn hidden', await s.isHidden('#teamBtn'));

 // sign out / sign in cycle
 await y.click('#meBtn'); await y.screenshot({path:__dirname+'/../../build/login3.png'}); await y.click('.lg-acts .out'); console.log('locked after sign out', await y.isVisible('#whoOverlay.lock'));
 await y.click('#whoList button:has-text("Yasser")'); await y.fill('#lgPw','aka1'); await y.press('#lgPw','Enter'); await y.waitForTimeout(600); console.log('back in', await y.textContent('#meBtn'));

 // lockout after 5 wrong tries
 let l=await open(await b.newContext());
 await l.click('#whoList button:has-text("Mich")'); await l.fill('#lgPw','mich1'); await l.fill('#lgPw2','mich1'); await l.click('.lg-form .go'); await l.waitForTimeout(600);
 await l.click('#meBtn'); await l.click('.lg-acts .out');
 for(let i=0;i<5;i++){ await l.click('#whoList button:has-text("Mich")'); await l.fill('#lgPw','wrong'); await l.click('.lg-form .go'); await l.waitForTimeout(150); await l.click('.lg-back'); }
 await l.click('#whoList button:has-text("Mich")'); await l.fill('#lgPw','wrong'); await l.click('.lg-form .go'); await l.waitForTimeout(300);
 console.log('locked out message', await l.textContent('#lgErr'));

 console.log('errors', JSON.stringify(errs)); await b.close();
})();
