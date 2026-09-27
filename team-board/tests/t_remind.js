// Verifies peer-set task reminders: only someone else's tasks can be reminded (not your own), setting one
// shows "remind-set" (dashed) on the task, and a reminder already due shows "remind-due" (solid red, pulsing)
// and pops the same sound+full-screen alarm for the task's own person, with Snooze/Done controls.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const root = path.join(__dirname, '..', '..');
  const now = Date.now();
  const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'fixtures', 'sample-state.json'), 'utf8'));
  const pieter = fixture.people.find(p => p.id === 'pieter');
  pieter.tasks = [
    { id: 'rm-task-1', text: 'Cut the sizzle reel', done: false, due: '2026-09-29', createdAt: now - 3600000, addedBy: 'pieter' },
  ];
  // a reminder already overdue, set by Yasser, targeting Pieter's task above
  fixture.reminders = {
    'rm1': { taskId: 'rm-task-1', pid: 'pieter', by: 'yasser', title: 'Cut the sizzle reel', due: now - 60000, status: 'pending' },
  };
  const fixturePath = path.join(__dirname, '..', 'fixtures', 'sample-state.json');
  const original = fs.readFileSync(fixturePath, 'utf8');
  fs.writeFileSync(fixturePath, JSON.stringify(fixture));
  try {
    execFileSync('python3', [path.join(root, 'team-board', 'build.py')]); // no-arg = fixture build, never published
  } finally {
    fs.writeFileSync(fixturePath, original);
  }

  const html = fs.readFileSync(path.join(root, 'build', 'team-board.html'), 'utf8');
  const b = await chromium.launch(); const errs = [];
  const p = await b.newPage({ viewport: { width: 1300, height: 950 } });
  p.on('pageerror', e => errs.push(e.message));
  await p.route('https://todo.test/', r => r.fulfill({ contentType: 'text/html', body: html }));
  await p.addInitScript(() => { window.claude = { use: (n) => Promise.resolve(n === 'artifact' ? { publish: () => Promise.resolve({}) } : null) }; });

  let firstSignIn = true;
  async function signIn(name) {
    if (firstSignIn) { await p.goto('https://todo.test/'); await p.waitForTimeout(300); firstSignIn = false; }
    else {
      // already signed in as someone else on this "device" — switch accounts instead of reloading,
      // so the shared board state (reminders etc.) carries over exactly as it would for real teammates
      await p.click('#meBtn'); await p.waitForTimeout(200);
      await p.click('.lg-acts .out'); await p.waitForTimeout(300);
    }
    if (await p.isVisible('#whoList')) await p.click('#whoList button:has-text("' + name + '")');
    await p.waitForTimeout(400);
    const pwInputs = await p.$$('input[type="password"]');
    if (pwInputs.length) {
      for (const inp of pwInputs) await inp.fill('testpass');
      await p.click('button:has-text("Create and sign in")');
    }
    await p.waitForTimeout(500);
  }

  // ---- Signed in as Pieter (the reminder's own person): the overdue reminder should already be ringing.
  await signIn('Pieter');
  await p.waitForTimeout(1200);
  console.log('task class on load (should be remind-due)', await p.evaluate(() => { const li = document.querySelector('li[data-key="rm-task-1"]'); return li ? li.className : 'NOT FOUND'; }));
  console.log('alarm visible on load', await p.isVisible('#alarmBox'));
  console.log('alarm text', await p.textContent('#alarmBox h2').catch(() => null));
  console.log('own task never shows a Remind button', (await p.locator('#col-pieter li[data-key="rm-task-1"] button:has-text("Remind")').count()) === 0);
  // Stop it
  await p.click('#alarmBox .ack');
  await p.waitForTimeout(200);
  console.log('alarm gone after Done', await p.isVisible('#alarmBox'));
  console.log('task class after Done (should lose remind-due)', await p.evaluate(() => { const li = document.querySelector('li[data-key="rm-task-1"]'); return li ? li.className : 'NOT FOUND'; }));

  // ---- Signed in as Yasser: reminding Pieter (someone else) should be offered; reminding himself should not.
  await signIn('Yasser');
  await p.click('#col-pieter .foldBtn'); await p.waitForTimeout(200);
  const remindBtn = p.locator('#col-pieter li[data-key="rm-task-1"] button:has-text("Remind")');
  console.log('Yasser can see a Remind control on Pieter\'s task', await remindBtn.count() > 0);
  await remindBtn.first().click(); await p.waitForTimeout(150);
  console.log('remind panel opened', await p.isVisible('#col-pieter .remindpanel'));
  await p.click('#col-pieter .remindpanel .opts button:has-text("1 hour")');
  await p.click('#col-pieter .remindpanel button:has-text("Set reminder")');
  await p.waitForTimeout(200);
  console.log('task class after setting a future reminder (should be remind-set, dashed)', await p.evaluate(() => { const li = document.querySelector('li[data-key="rm-task-1"]'); return li ? li.className : 'NOT FOUND'; }));
  // Yasser has his own task too (from fixture); he should never see a Remind button on it.
  console.log('no Remind button on own (Yasser\'s) tasks', (await p.locator('#col-yasser .item button:has-text("Remind")').count()) === 0);

  await p.screenshot({ path: __dirname + '/remind.png' });
  console.log(JSON.stringify(errs)); await b.close();
})();
