const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[];
 const ctx=await b.newContext({viewport:{width:1440,height:860}});
 const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
 let loads=0; p.on('load',()=>loads++);
 await p.clock.install();
 await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.addInitScript(()=>{ window.claude={use:(n)=>Promise.resolve(n==='artifact'?{publish:(h)=>{window.__pub=h;return Promise.resolve({});}}:null)}; });
 await p.goto('https://todo.test/'); await p.clock.runFor(500);
 await p.click('#whoList button:has-text("Pieter")'); 
 await p.evaluate(()=>window.scrollTo(0,600));
 await p.clock.runFor(125000); await p.waitForTimeout(500);
 console.log('loads after idle 2min', loads, 'scroll restored', await p.evaluate(()=>window.scrollY));
 // now type in chat and ensure no reload
 const before=loads;
 await p.click('#chatBtn'); await p.fill('#chatText','half typed');
 await p.clock.runFor(185000); await p.waitForTimeout(300);
 console.log('reloads while typing', loads-before);
 console.log(JSON.stringify(errs)); await b.close();
})();
