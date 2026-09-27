import os,re
os.chdir('/tmp/claude-0/-home-claude/f551496a-6099-53c0-bb40-c24e871c007b/scratchpad')
p='cc/src.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
SPARK='<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z" fill="currentColor"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z" fill="currentColor"/></svg>'
# markup: floating button + popup, before the closing wrap div's script
rep('<script>\n(function(){', '''<button type="button" class="fab" id="fab" aria-haspopup="dialog" aria-controls="pop">'''+SPARK+'''<span>Claude</span></button>
<div class="pop" id="pop" hidden role="dialog" aria-modal="false" aria-labelledby="popTitle">
  <div class="poph"><span class="spark">'''+SPARK+'''</span><div class="pt"><b id="popTitle">Claude</b><span id="popCtx">Ask anything, or finish a task here</span></div>
    <button type="button" class="pbtn" id="popNew" title="Start a new chat">New</button><button type="button" class="pbtn x" id="popClose" aria-label="Close Claude chat">×</button></div>
  <div class="pthread" id="pthread" aria-live="polite"></div>
  <form class="pform" id="pform"><textarea id="pask" rows="1" placeholder="Message Claude" aria-label="Message Claude"></textarea><button type="submit" class="psend" id="psend">Send</button></form>
  <p class="pfoot">Reads Gmail, Outlook, calendar and Teams. Saves drafts, never sends.</p>
</div>
<script>
(function(){''')
rep(".sempty{margin:0;", """.fab{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:40;display:inline-flex;align-items:center;gap:8px;border:0;border-radius:999px;padding:12px 18px 12px 14px;background:var(--ink);color:var(--bg);font:600 15px/1 "Outfit",sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.25)}
.fab svg{color:var(--red)}
.fab:hover{transform:translateY(-1px)}
.fab.busy::after{content:"";width:8px;height:8px;border-radius:50%;background:var(--red);animation:pulse 1s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
.pop{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:50;width:min(440px,calc(100vw - 32px));height:min(640px,calc(100vh - 40px));background:var(--panel);border:1px solid var(--line);border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.28);display:flex;flex-direction:column;overflow:hidden;animation:rise .2s ease-out}
.poph{display:flex;align-items:center;gap:10px;padding:12px 12px 12px 16px;border-bottom:1px solid var(--line)}
.poph .spark{width:32px;height:32px;border-radius:10px;display:grid;place-items:center;background:var(--red);color:var(--red-ink)}
.poph .pt{display:flex;flex-direction:column;min-width:0;margin-right:auto}
.poph .pt b{font:600 16px/1.2 "Outfit",sans-serif}
.poph .pt span{font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:260px}
.pbtn{border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:4px 10px;font-size:13px}
.pbtn.x{border:0;font-size:20px;padding:0 8px;color:var(--muted)}
.pthread{flex:1;overflow-y:auto;padding:14px 16px;display:flex;flex-direction:column;gap:12px;background:var(--bg)}
.pu{align-self:flex-end;max-width:85%;background:var(--ink);color:var(--bg);padding:8px 12px;border-radius:14px 14px 4px 14px;font-size:14.5px;white-space:pre-wrap;overflow-wrap:anywhere}
.pa{align-self:flex-start;max-width:95%;font-size:14.5px;line-height:1.5;overflow-wrap:anywhere}
.pa .psteps{font-size:12px;color:var(--muted);margin-bottom:4px}
.pa .err{margin-top:6px}
.pwelcome{color:var(--muted);font-size:14px;margin:auto 0;text-align:center;padding:20px}
.pform{display:grid;grid-template-columns:1fr auto;gap:8px;padding:10px 12px;border-top:1px solid var(--line)}
.pform textarea{font:inherit;font-size:15px;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:9px 11px;resize:none;min-height:42px;max-height:150px}
.pform textarea:focus{outline:none;border-color:var(--red)}
.psend{border:0;border-radius:12px;padding:0 16px;background:var(--red);color:var(--red-ink);font-weight:600;align-self:end;height:42px}
.psend.stop{background:var(--ink);color:var(--bg)}
.pfoot{margin:0;padding:0 14px 10px;font-size:11.5px;color:var(--muted)}
body.pop-on .fab{display:none}
@media (max-width:560px){.pop{right:0;bottom:0;width:100vw;height:100%;border-radius:0;border:0}}
.mini.claude{border-color:color-mix(in srgb,var(--red) 40%,var(--line));color:var(--red);font-weight:600}
.sempty{margin:0;""")

# new ask(): popup for manual asks, reply panel only for the silent daily brief
old_start = s.index("  function ask(text, auto){")
old_end = s.index("  // ---- send an email to Promotions")
s = s[:old_start] + r"""  // ---- pop-up Claude chat
  function popOpen(){ return !$('pop').hidden; }
  function openPop(ctx){
    $('pop').hidden = false; document.body.classList.add('pop-on'); lsSet('cc-pop', '1');
    if(ctx) $('popCtx').textContent = ctx;
    renderPop(); setTimeout(function(){ $('pask').focus(); }, 30);
  }
  function closePop(){ $('pop').hidden = true; document.body.classList.remove('pop-on'); lsSet('cc-pop', ''); $('fab').focus(); }
  function shown(t){ return t.content === BRIEF ? 'Daily brief' : (t.label || t.content); }
  function renderPop(){
    var th = $('pthread'); th.textContent = '';
    if(!history.length){ var w = document.createElement('p'); w.className = 'pwelcome'; w.textContent = 'Ask me anything, or press “Do it with Claude” on a task, email or message to finish it here.'; th.appendChild(w); }
    history.forEach(function(t){
      var d = document.createElement('div');
      if(t.role === 'user'){ d.className = 'pu'; d.textContent = shown(t); } else { d.className = 'pa body'; md(d, t.content); }
      th.appendChild(d);
    });
    th.scrollTop = th.scrollHeight;
  }
  $('fab').addEventListener('click', function(){ openPop(); });
  $('popClose').addEventListener('click', closePop);
  $('popNew').addEventListener('click', function(){ if(busy) busy.abort(); history = []; saveHistory(); $('popCtx').textContent = 'Ask anything, or finish a task here'; renderPop(); $('pask').focus(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && popOpen() && !busy) closePop(); });
  $('pform').addEventListener('submit', function(e){ e.preventDefault(); if(busy){ busy.abort(); return; } var t = $('pask').value; $('pask').value = ''; $('pask').style.height = 'auto'; ask(t); });
  $('pask').addEventListener('keydown', function(e){ if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); $('pform').requestSubmit(); } });
  $('pask').addEventListener('input', function(){ var t = $('pask'); t.style.height = 'auto'; t.style.height = Math.min(150, t.scrollHeight) + 'px'; });
  // start a task in the pop-up with its context
  function doWithClaude(label, prompt){ openPop(label); ask(prompt, false, label); }

  function setBusyUi(on){
    var ps = $('psend'), go = $('goBtn');
    ps.textContent = on ? 'Stop' : 'Send'; ps.classList.toggle('stop', on);
    go.textContent = on ? 'Stop' : 'Ask'; go.classList.toggle('stop', on);
    $('fab').classList.toggle('busy', on);
  }
  function ask(text, auto, label){
    text = String(text || '').trim(); if(!text) return;
    if(busy) return;
    var target, steps;
    if(auto){
      $('reply').hidden = false; $('lastQ').textContent = 'Daily brief';
      target = $('answer'); steps = $('steps');
    } else {
      if(!popOpen()) openPop();
      var th = $('pthread'); var wl = th.querySelector('.pwelcome'); if(wl) wl.remove();
      var u = document.createElement('div'); u.className = 'pu'; u.textContent = label || text; th.appendChild(u);
      var a = document.createElement('div'); a.className = 'pa'; a.innerHTML = '<div class="psteps"></div><div class="body"></div>'; th.appendChild(a);
      target = a.querySelector('.body'); steps = a.querySelector('.psteps'); th.scrollTop = th.scrollHeight;
    }
    if(!sample || !mcp){ target.innerHTML = '<p class="err">' + (!sample ? 'Claude isn’t available in this view. Open the page in claude.ai while signed in.' : 'The connectors aren’t available in this view.') + '</p>'; return; }
    currentRequest = text;
    var turn = { role: 'user', content: text }; if(label) turn.label = label;
    history.push(turn); saveHistory();
    target.innerHTML = '<p class="thinking">Thinking…</p>'; steps.textContent = '';
    busy = new AbortController(); var signal = busy.signal; setBusyUi(true);
    var convo = [{ role: 'user', content: rules() }].concat(history.slice(-12).map(function(t){ return { role: t.role, content: t.content }; }));
    var scroll = function(){ if(!auto){ var th = $('pthread'); th.scrollTop = th.scrollHeight; } };
    sample(convo, { signal: signal, tools: tools(function(x){ steps.textContent = x; scroll(); }, signal), onText: function(u2){ md(target, u2.text); scroll(); } }).then(function(r){
      history.push({ role: 'assistant', content: r.text }); saveHistory();
      if(r.truncated){ var n = document.createElement('p'); n.className = 'err'; n.textContent = 'Cut short. Ask for less at a time.'; target.appendChild(n); }
      if(auto) saveMeta({ lastBrief: dubaiDay() });
    }, function(e){
      if(e && e.text){ md(target, e.text); history.push({ role: 'assistant', content: e.text }); saveHistory(); } else if(!(e && e.code === 'cancelled')) target.textContent = '';
      if(e && e.code === 'cancelled'){ if(!e.text) target.innerHTML = '<p class="thinking">Stopped.</p>'; return; }
      var n = document.createElement('p'); n.className = 'err'; n.textContent = copyFor(e && e.code); target.appendChild(n);
    }).then(function(){ busy = null; steps.textContent = ''; setBusyUi(false); scroll(); if(!$('log').hidden) renderLog(); });
  }
""" + s[old_end:]

# "Do it with Claude" on items
rep("""          if(secOf(c) === 'email' && !it.queued){""", """          var dsec = secOf(c);
          if((dsec === 'todo' || dsec === 'email' || dsec === 'social' || dsec === 'calendar') && it.title && !/^Open the team chat$/.test(it.title)){
            var dw = document.createElement('button'); dw.type = 'button'; dw.className = 'mini claude'; dw.textContent = 'Do it with Claude';
            dw.addEventListener('click', function(){
              var ttl = it.title, sub = it.subtitle ? ' (' + it.subtitle + ')' : '';
              var ref = it.threadId ? ' Gmail threadId ' + it.threadId + (it.messageId ? ', messageId ' + it.messageId : '') + '.' : it.uri ? ' Outlook uri ' + it.uri + (it.messageId ? ', messageId ' + it.messageId : '') + '.' : '';
              var prompt, label;
              if(dsec === 'todo'){ label = 'Task: ' + ttl; prompt = 'Help me get this task from my to-do list done right now: "' + ttl + '"' + (it.when ? ' (due ' + it.when + ')' : '') + sub + '. Work out what it needs, look up any emails or context you need, draft any email as a draft in the right mailbox, and ask me for anything only I know. Keep each step short and tell me when it is ready to tick off on the team board.'; }
              else if(dsec === 'email'){ label = 'Email: ' + ttl; prompt = 'Help me deal with this email now: "' + ttl + '"' + sub + '.' + ref + (ref ? ' Read it first.' : ' It is in my akamedia.ae work inbox, which you cannot open, so work from these details and ask me to paste the text if you need it.') + ' Tell me in two lines what it needs from me, then write a short human reply in my voice and save it as a draft in the same mailbox if you can.'; }
              else if(dsec === 'social'){ label = 'LinkedIn: ' + ttl; prompt = 'Help me reply to this LinkedIn message from ' + ttl + sub + '. You cannot open LinkedIn, so work from this; ask me to paste the message if you need more. Write a short, human LinkedIn reply in my voice that I can paste.'; }
              else { label = 'Meeting: ' + ttl; prompt = 'Help me prepare for this: "' + ttl + '"' + sub + (it.when ? ' at ' + it.when : '') + '. Pull any related emails, give me a short brief and anything I should send beforehand as drafts.'; }
              doWithClaude(label, prompt);
            });
            acts.appendChild(dw);
          }
          if(secOf(c) === 'email' && !it.queued){""")
# Claude section ask bar routes to popup (ask() already does); suggestion chips too. Reopen pop after reload
rep("  paintSecs();", "  paintSecs();\n  if(lsGet('cc-pop') === '1') setTimeout(function(){ openPop(); }, 0);")
open(p,'w').write(s)
s=s.replace('LOGO_L',open('logo_light.txt').read()).replace('LOGO_D',open('logo_dark.txt').read())
open('cc/command-centre.html','w').write(s)
open('cc/a.js','w').write(re.search(r'<script>\n\(function\(\)\{(.*)</script>',s,re.S).group(1)[:-0] if False else re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
print('ok')
