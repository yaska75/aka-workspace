p='cc/src.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
start=s.index('  <form class="cmd" id="cmd">'); end=s.index('  <p class="foot">')
I = {
 'email':'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'calendar':'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.5 10h17M8 3v4M16 3v4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 'team':'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="9" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.5 19c.6-3 2.8-4.6 5.5-4.6s4.9 1.6 5.5 4.6M14.5 15.2c.8-.5 1.6-.7 2.5-.7 2 0 3.6 1.3 4 3.8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 'social':'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h11v8H9l-4 3.5V13H4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M15 9h5v8h-1v3l-3.5-3H11v-2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'claude':'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z" fill="currentColor"/></svg>'}
dock = '  <nav class="dock" id="dock" aria-label="Sections">\n' + ''.join(
 '    <button type="button" class="dk" data-sec="%s" aria-pressed="false"><span class="ic">%s</span><b>%s</b><span class="n" hidden></span></button>\n' % (k, I[k], lbl)
 for k,lbl in [('email','Email'),('calendar','Calendar'),('team','Team'),('social','Social'),('claude','Claude')]) + '  </nav>\n'
def sec(k, title, refresh, extra=''):
    rb = '<button type="button" class="sr" data-ask="%s">Refresh</button>' % refresh if refresh else ''
    return ('  <section class="sec" data-sec="%s" hidden aria-label="%s">\n    <div class="sh"><h2>%s</h2>%s<button type="button" class="sc" aria-label="Close %s">×</button></div>\n%s    <div class="canvas" id="cv-%s"></div>\n    <p class="sempty" id="se-%s" hidden></p>\n  </section>\n') % (k, title, title, rb, title, extra, k, k)
social_extra = '''    <div class="apps">
      <a class="app" href="https://web.whatsapp.com/" target="_blank" rel="noopener noreferrer"><b>WhatsApp</b><small>Not linked · open WhatsApp Web ↗</small></a>
      <a class="app" href="https://www.instagram.com/direct/inbox/" target="_blank" rel="noopener noreferrer"><b>Instagram</b><small>Can connect later · open DMs ↗</small></a>
      <a class="app" href="https://www.linkedin.com/messaging/" target="_blank" rel="noopener noreferrer"><b>LinkedIn</b><small>Not linked · open messages ↗</small></a>
    </div>
'''
team_extra = '''    <div class="apps">
      <a class="app" href="https://claude.ai/artifact/8GwGDwq8AAmCDmQAqEZjif" target="_blank" rel="noopener noreferrer"><b>Team board</b><small>To-do lists, chat, calls and alerts ↗</small></a>
      <a class="app" href="https://drive.google.com/drive/folders/1ZeCn53_VgPlSZ0ybts4QlBoIxexRxjFh" target="_blank" rel="noopener noreferrer"><b>Team files</b><small>AKATEAMFILEEXCHANGE on Drive ↗</small></a>
    </div>
'''
claude_sec = '''  <section class="sec" data-sec="claude" hidden aria-label="Claude">
    <div class="sh"><h2>Claude</h2><button type="button" class="sc" aria-label="Close Claude">×</button></div>
    <form class="cmd" id="cmd">
      <textarea id="ask" rows="1" placeholder="Tell Claude what you need. For example: what needs my reply, prep me for Tuesday, draft a note to Pieter" aria-label="Ask Claude"></textarea>
      <button class="brief" type="button" id="briefBtn" title="Claude pulls what matters right now into your sections">Brief me</button>
      <button class="go" type="submit" id="goBtn">Ask</button>
    </form>
    <div class="sugg">
      <button class="chip" type="button">Brief me</button>
      <button class="chip" type="button">What needs my reply?</button>
      <button class="chip" type="button">My week ahead</button>
      <button class="chip" type="button">Draft a note to Pieter</button>
    </div>
    <div class="reply" id="reply" hidden aria-live="polite">
      <div class="hd"><b>Claude</b><span class="steps" id="steps"></span><button class="x" type="button" id="logBtn">Conversation</button></div>
      <p class="q" id="lastQ"></p>
      <div class="body" id="answer"></div>
      <div class="log" id="log" hidden></div>
    </div>
    <div class="canvas" id="cv-claude"></div>
  </section>
'''
body = dock + '  <div class="blank" id="blank"><p>Choose a section to open.</p></div>\n' + claude_sec + \
  sec('email','Email','Refresh my email: pull emails from the last 3 days that need my reply or attention from Gmail and Outlook into email cards.') + \
  sec('calendar','Calendar','Pull my calendar for today and the next 7 days into a calendar card.') + \
  sec('team','Team','Pull recent Microsoft Teams messages and anything my team needs from me into team cards.', team_extra) + \
  sec('social','Social','', social_extra)
s = s[:start] + body + s[end:]

# CSS
rep(".empty{border:1.5px dashed", """.dock{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.dk{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:10px;padding:16px;border:1px solid var(--line);border-radius:18px;background:var(--panel);text-align:left;box-shadow:var(--shadow);transition:border-color .15s,transform .15s}
.dk:hover{border-color:var(--red);transform:translateY(-1px)}
.dk .ic{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--soft);color:var(--ink)}
.dk b{font:600 17px/1.1 "Outfit",sans-serif;letter-spacing:-.01em}
.dk .n{position:absolute;top:14px;right:14px;min-width:22px;height:22px;padding:0 7px;border-radius:999px;background:var(--red);color:var(--red-ink);font-size:12px;font-weight:700;display:grid;place-items:center}
.dk[aria-pressed=true]{border-color:var(--red);box-shadow:0 0 0 2px color-mix(in srgb,var(--red) 25%,transparent)}
.dk[aria-pressed=true] .ic{background:var(--red);color:var(--red-ink)}
.blank{min-height:38vh;display:grid;place-items:center;color:var(--muted);font-size:14px}
.blank p{margin:0;letter-spacing:.04em}
.sec{background:var(--panel);border:1px solid var(--line);border-radius:22px;padding:14px 16px 18px;display:flex;flex-direction:column;gap:12px;animation:rise .25s ease-out}
.sh{display:flex;align-items:center;gap:10px}
.sh h2{margin:0;font:700 22px/1.1 "Outfit",sans-serif;letter-spacing:-.02em;margin-right:auto}
.sr{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:5px 12px;font-size:13px}
.sr:hover{border-color:var(--red);color:var(--red)}
.sc{border:0;background:none;color:var(--muted);font-size:20px;width:32px;height:32px;border-radius:9px}
.sc:hover{background:var(--soft);color:var(--ink)}
.sec .card{box-shadow:none}
.sec .cmd{box-shadow:none}
.sec .reply{border-color:var(--line)}
.sempty{margin:0;color:var(--muted);font-size:14px}
.apps{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr));gap:10px}
.app{display:flex;flex-direction:column;gap:3px;padding:12px 14px;border:1px solid var(--line);border-radius:14px;text-decoration:none;color:var(--ink)}
.app:hover{border-color:var(--red)}
.app b{font:600 15px/1.2 "Outfit",sans-serif}
.app small{color:var(--muted);font-size:13px}
@media (max-width:760px){.dock{grid-template-columns:repeat(3,minmax(0,1fr))}.dk{padding:12px}.dk .ic{width:34px;height:34px}}
@media (max-width:420px){.dock{grid-template-columns:repeat(2,minmax(0,1fr))}}
.empty{border:1.5px dashed""")

# render cards into sections
rep("""  function renderCanvas(){
    var cv = $('canvas'), list = cardList(); cv.textContent = '';
    $('empty').hidden = list.length > 0;
    list.forEach(function(c){""", """  var SECS = ['email', 'calendar', 'team', 'social', 'claude'];
  function secOf(c){ var s0 = String(c.source || '').toLowerCase(); if(s0 === 'gmail' || s0 === 'outlook' || s0 === 'email') return 'email'; if(s0 === 'calendar') return 'calendar'; if(s0 === 'teams' || s0 === 'team') return 'team'; if(s0 === 'social' || s0 === 'instagram' || s0 === 'whatsapp' || s0 === 'linkedin') return 'social'; return 'claude'; }
  var SEC_EMPTY = { email: 'Nothing pulled yet. Press Refresh or ask Claude.', calendar: 'Nothing pulled yet. Press Refresh or ask Claude.', team: 'No team updates pulled yet.', social: 'Message apps can\\u2019t be read yet; open them from here.', claude: '' };
  function renderCanvas(){
    var list = cardList();
    SECS.forEach(function(k){ var el = $('cv-' + k); if(el) el.textContent = ''; });
    var counts = {}; SECS.forEach(function(k){ counts[k] = 0; });
    list.forEach(function(c){
      var sk = secOf(c), cv = $('cv-' + sk); if(!cv) return;
      counts[sk] += (Array.isArray(c.items) && c.items.length) ? c.items.filter(function(it){ return it.priority === 'high' || it.priority === 'med'; }).length || c.items.length : 1;""")
rep("""      cv.appendChild(el);
    });
  }""", """      cv.appendChild(el);
    });
    SECS.forEach(function(k){
      var b = document.querySelector('.dk[data-sec="' + k + '"] .n'); if(b){ b.hidden = !counts[k]; b.textContent = counts[k] > 99 ? '99+' : counts[k]; }
      var e = $('se-' + k); if(e){ var has = $('cv-' + k).children.length > 0; e.hidden = has || !SEC_EMPTY[k]; e.textContent = SEC_EMPTY[k]; }
    });
  }
  // sections: nothing open until chosen
  var openSecs = [];
  try { openSecs = JSON.parse(lsGet('cc-open') || '[]') || []; } catch(e){ openSecs = []; }
  function paintSecs(){
    SECS.forEach(function(k){
      var on = openSecs.indexOf(k) >= 0;
      var b = document.querySelector('.dk[data-sec="' + k + '"]'); if(b) b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var s1 = document.querySelector('.sec[data-sec="' + k + '"]'); if(s1) s1.hidden = !on;
    });
    // keep the page order the same as the dock
    var wrap = $('blank').parentNode; SECS.forEach(function(k){ var s1 = document.querySelector('.sec[data-sec="' + k + '"]'); if(s1) wrap.insertBefore(s1, $('blank').nextSibling && null || document.querySelector('.foot')); });
    $('blank').hidden = openSecs.length > 0;
    lsSet('cc-open', JSON.stringify(openSecs));
  }
  function openSec(k){ if(openSecs.indexOf(k) < 0) openSecs.push(k); openSecs.sort(function(a, b){ return SECS.indexOf(a) - SECS.indexOf(b); }); paintSecs(); }
  function toggleSec(k){ var i = openSecs.indexOf(k); if(i >= 0) openSecs.splice(i, 1); else { openSec(k); var s1 = document.querySelector('.sec[data-sec="' + k + '"]'); if(s1) s1.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; } paintSecs(); }
  Array.prototype.forEach.call(document.querySelectorAll('.dk'), function(b){ b.addEventListener('click', function(){ toggleSec(b.dataset.sec); if(b.dataset.sec === 'claude') setTimeout(function(){ $('ask').focus(); }, 50); }); });
  Array.prototype.forEach.call(document.querySelectorAll('.sec .sc'), function(b){ b.addEventListener('click', function(){ var k = b.closest('.sec').dataset.sec; var i = openSecs.indexOf(k); if(i >= 0){ openSecs.splice(i, 1); paintSecs(); } }); });
  Array.prototype.forEach.call(document.querySelectorAll('.sec .sr'), function(b){ b.addEventListener('click', function(){ ask(b.dataset.ask); }); });
  paintSecs();""")
# ask opens Claude section unless auto
rep("""    $('reply').hidden = false; $('lastQ').textContent = auto ? 'Daily brief' : text;""",
    """    if(!auto) openSec('claude');
    $('reply').hidden = false; $('lastQ').textContent = auto ? 'Daily brief' : text;""")
# rules: sections
rep("'How to work: decide yourself what to pull.", "'The workspace starts empty; Yasser opens sections from a row of buttons: Email (cards with source gmail or outlook), Calendar (source calendar), Team (source teams: Microsoft Teams and team matters), Social (source social), Claude (source claude: notes, drafts, plans). Choose each card\\'s source so it lands in the right section.\\n' + 'How to work: decide yourself what to pull.")
rep("source: gmail, outlook, calendar, teams or claude.", "source: gmail or outlook (Email section), calendar, teams (Team section), social, or claude (notes, drafts, plans).")
open(p,'w').write(s); print('ok')
