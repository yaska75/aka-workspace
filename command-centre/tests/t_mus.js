const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const html='<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(__dirname+'/../../build/command-centre.html','utf8')+'</body></html>';
 const b=await chromium.launch(); const errs=[];
 for (const [w,name] of [[1440,'mus.png'],[390,'mus_m.png']]){
 const p=await b.newPage({viewport:{width:w,height:860}}); p.on('pageerror',e=>errs.push(e.message));
 await p.route('https://cc.test/', r=>r.fulfill({contentType:'text/html',body:html}));
 await p.route('https://open.spotify.com/embed/**', r=>r.fulfill({contentType:'text/html',body:'<body style="background:#333;color:#fff;font:20px sans-serif">Spotify embed stub</body>'}));
 await p.addInitScript(()=>{ localStorage.setItem('cc-meta', JSON.stringify({lastBrief:new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dubai'})})); window.claude={use:()=>Promise.resolve(null)}; });
 await p.goto('https://cc.test/'); await p.waitForTimeout(400);
 console.log(w,'iframes before', await p.locator('#musSlot iframe').count());
 await p.click('#musBtn'); await p.waitForTimeout(300);
 console.log('open', await p.isVisible('#mus iframe'), await p.getAttribute('#mus iframe','src'));
 await p.screenshot({path:__dirname+'/../../build/'+name});
 await p.click('#musHide'); console.log('hidden keeps iframe', await p.locator('#musSlot iframe').count(), 'btn on', await p.getAttribute('#musBtn','class'));
 await p.click('#musBtn'); await p.click('#musStop'); console.log('stopped', await p.locator('#musSlot iframe').count());
 await p.close(); }
 console.log(JSON.stringify(errs)); await b.close();
})();
