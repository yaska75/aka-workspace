const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 let html=fs.readFileSync(__dirname+'/../../build/team-board.html','utf8');
 const b=await chromium.launch(); const errs=[];
 async function open(who){
   const ctx=await b.newContext({viewport:{width:1440,height:860}});
   const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(who+': '+e.message));
   await p.route('https://todo.test/', r=>r.fulfill({contentType:'text/html',body:html}));
   await p.addInitScript(()=>{ window.claude={use:(n)=>Promise.resolve(n==='artifact'?{publish:(h)=>{window.__pub=h;return Promise.resolve({});}}:null)}; });
   await p.goto('https://todo.test/'); await p.waitForTimeout(300);
   if(await p.isVisible('#whoList')) await p.click(`#whoList button:has-text("${who}")`);
   await p.waitForTimeout(500); return p;
 }
 const Y=await open('Yasser'), M=await open('Mich');
 await Y.click('#chatBtn'); await Y.click('.chan.dm:has-text("Mich")'); await Y.click('#alertBtn'); await Y.click('#startCall');
 await Y.waitForTimeout(2300); html=await Y.evaluate(()=>window.__pub);
 await M.reload(); await M.waitForTimeout(900);
 console.log('stored alarm', await M.isVisible('#alarmBox'), await M.textContent('#alarmBox h2'));
 console.log(JSON.stringify(errs)); await b.close();
})();
