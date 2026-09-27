// Verifies open-task age color coding: age-fresh (<24h), age-warn (24-48h), age-stale (>48h since createdAt).
// Builds a temp fixture with three open tasks for Yasser at controlled ages, plus one done task (should get no age class).
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const root = path.join(__dirname, '..', '..');
  const now = Date.now();
  const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'fixtures', 'sample-state.json'), 'utf8'));
  const yasser = fixture.people.find(p => p.id === 'yasser');
  yasser.tasks = [
    { id: 'age-fresh', text: 'Fresh task (2h old)', done: false, due: '2026-09-29', createdAt: now - 2 * 3600000, addedBy: 'pieter' },
    { id: 'age-warn', text: 'Warn task (30h old)', done: false, due: '2026-09-29', createdAt: now - 30 * 3600000, addedBy: 'pieter' },
    { id: 'age-stale', text: 'Stale task (60h old)', done: false, due: '2026-09-29', createdAt: now - 60 * 3600000, addedBy: 'pieter' },
    { id: 'age-done', text: 'Old but done', done: true, due: '2026-09-27', createdAt: now - 90 * 3600000, addedBy: 'pieter' },
  ];
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
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  p.on('pageerror', e => errs.push(e.message));
  await p.route('https://todo.test/', r => r.fulfill({ contentType: 'text/html', body: html }));
  await p.addInitScript(() => { window.claude = { use: (n) => Promise.resolve(n === 'artifact' ? { publish: () => Promise.resolve({}) } : null) }; });
  await p.goto('https://todo.test/'); await p.waitForTimeout(300);
  if (await p.isVisible('#whoList')) await p.click('#whoList button:has-text("Yasser")');
  await p.waitForTimeout(400);
  const pwInputs = await p.$$('input[type="password"]');
  if (pwInputs.length) {
    for (const inp of pwInputs) await inp.fill('testpass');
    await p.click('button:has-text("Create and sign in")');
  }
  await p.waitForTimeout(600);

  async function cls(id) { return await p.evaluate((id) => { const li = document.querySelector(`li[data-key="${id}"]`); return li ? li.className : 'NOT FOUND'; }, id); }
  console.log('fresh', await cls('age-fresh'));
  console.log('warn', await cls('age-warn'));
  console.log('stale', await cls('age-stale'));
  console.log('done (no age class expected)', await cls('age-done'));
  console.log(JSON.stringify(errs));
  await b.close();
})();
