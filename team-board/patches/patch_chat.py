p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, (s.count(a), a[:80])
    s=s.replace(a,b)

# ---- CSS
rep(".mv{background:none;", """.badge{display:inline-grid;place-items:center;min-width:18px;height:18px;padding:0 5px;border-radius:999px;background:var(--strike);color:#fff;font-size:11px;font-weight:700;margin-left:2px}
.chat{position:fixed;top:0;right:0;bottom:0;width:min(440px,100%);background:var(--surface);border-left:1px solid var(--line);box-shadow:-18px 0 50px rgba(0,0,0,.18);display:flex;flex-direction:column;z-index:45}
.chat-head{padding:16px 16px 10px;border-bottom:1px solid var(--line)}
.chat-head .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.chat-head h3{font-family:"Bricolage Grotesque","Instrument Sans",system-ui,sans-serif;font-size:26px;letter-spacing:-.02em;margin:0}
.chans{display:flex;gap:4px;flex-wrap:wrap}
.chan{background:none;border:1px solid var(--line);border-radius:999px;padding:4px 12px;color:var(--muted);font-size:14px}
.chan[aria-selected=true]{background:var(--ink);border-color:var(--ink);color:var(--surface);font-weight:600}
.chan .badge{margin-left:4px}
.chat-note{font-size:12px;color:var(--muted);margin:8px 0 0}
.msgs{flex:1;overflow-y:auto;padding:14px 16px;display:flex;flex-direction:column;gap:10px;background:var(--paper)}
.msg{display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:end;max-width:88%}
.msg .photo{width:30px;height:30px;border-width:2px}
.msg .initials{font-size:13px}
.bubble{background:var(--surface);border:1px solid var(--line);border-radius:14px 14px 14px 4px;padding:7px 11px;min-width:0}
.bubble .who{display:flex;gap:8px;align-items:baseline;font-size:12px;color:var(--muted);margin-bottom:2px}
.bubble .who b{color:var(--c);font-weight:700}
.bubble p{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font-size:15px;line-height:1.4}
.bubble p a{color:var(--c)}
.bubble .rm{background:none;border:0;color:var(--muted);font-size:12px;padding:0;margin-left:auto;opacity:0}
.msg:hover .rm,.msg:focus-within .rm{opacity:1}
@media (hover:none){.bubble .rm{opacity:1}}
.msg.mine{align-self:flex-end;grid-template-columns:1fr}
.msg.mine .photo{display:none}
.msg.mine .bubble{border-radius:14px 14px 4px 14px;background:var(--c);border-color:var(--c);color:var(--c-ink)}
.msg.mine .bubble .who,.msg.mine .bubble .who b,.msg.mine .bubble p a,.msg.mine .bubble .rm{color:var(--c-ink)}
.day{align-self:center;font-size:12px;color:var(--muted);padding:2px 10px;border-radius:999px;background:var(--surface);border:1px solid var(--line)}
.nomsg{margin:auto;color:var(--muted);text-align:center;padding:30px 10px}
.composer{display:grid;grid-template-columns:1fr auto;gap:8px;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));border-top:1px solid var(--line);background:var(--surface)}
.composer textarea{font:inherit;color:var(--ink);border:1px solid var(--line);background:var(--paper);border-radius:12px;padding:9px 11px;resize:none;min-height:42px;max-height:140px}
.composer textarea:focus{border-color:var(--accent);outline:none}
.composer .primary{--c:var(--accent);align-self:end}
.readonly .composer{display:none}
.mv{background:none;""")

# ---- state: chat store
rep("    if(!Array.isArray(s.people)) s.people = [];",
    "    if(!Array.isArray(s.people)) s.people = [];\n    if(!s.chat || typeof s.chat !== 'object' || Array.isArray(s.chat)) s.chat = {};")

# ---- top bar button + drawer markup
rep("""          '<button class="pill" id="sendBtn" type="button" hidden>Send a task</button>' +""",
"""          '<button class="pill" id="chatBtn" type="button" hidden>Chat<span class="badge" id="chatBadge" hidden></span></button>' +
          '<button class="pill" id="sendBtn" type="button" hidden>Send a task</button>' +""")
rep("""      '</form></div></div>';""", """      '</form></div></div>' +
    '<aside class="chat k0" id="chatPanel" hidden aria-labelledby="chatTitle">' +
      '<div class="chat-head"><div class="top"><h3 id="chatTitle">Team chat</h3><button class="link" type="button" id="chatClose">Close</button></div>' +
        '<div class="chans" id="chans" role="tablist" aria-label="Channels"></div>' +
        '<p class="chat-note" id="chatNote"></p></div>' +
      '<div class="msgs" id="msgs" aria-live="polite"></div>' +
      '<form class="composer" id="composer"><textarea id="chatText" rows="1" placeholder="Write a message" aria-label="Message"></textarea><button class="primary" type="submit">Send</button></form>' +
    '</aside>';""")

# ---- escape closes chat
rep("    else if(sendOpen) closeSend();", "    else if(sendOpen) closeSend();\n    else if(chatOpen) closeChat();")

# ---- render hooks
rep("""    renderTop();
    if(teamOpen) renderTeam();""", """    renderTop();
    if(teamOpen) renderTeam();
    if(chatOpen) renderChat();""")
rep("    $('sendBtn').hidden = mode === 'readonly' || !m || !addablePeople().length;",
"""    $('sendBtn').hidden = mode === 'readonly' || !m || !addablePeople().length;
    $('chatBtn').hidden = !m;
    var unread = m ? channelsFor(m).reduce(function(n, c){ return n + unreadIn(c.id); }, 0) : 0;
    $('chatBadge').hidden = !unread; $('chatBadge').textContent = unread > 99 ? '99+' : unread;""")

# ---- chat logic (before task actions section)
rep("  // ---------- task actions ----------", """  // ---------- team chat ----------
  // Channels follow the same rules as the lists: Everyone for all; each team
  // has its own channel; Management also reads Post; the superuser reads all.
  var CHANNELS = [
    { id: 'all', name: 'Everyone' },
    { id: 'management', name: 'Management' },
    { id: 'post', name: 'Post' },
    { id: 'finance', name: 'Finance' }
  ];
  var chatOpen = ss.get('chat-open') === '1', chatChan = ss.get('chat-chan') || 'all';
  function canSeeChannel(v, ch){
    if(!v) return false;
    if(ch === 'all' || v.role === 'superuser' || v.team === ch) return true;
    return v.team === 'management' && ch === 'post';
  }
  function channelsFor(v){ return CHANNELS.filter(function(c){ return canSeeChannel(v, c.id); }); }
  function msgsIn(ch){ return (state.chat[ch] || []); }
  function seenKey(ch){ return 'chat-seen-' + (ls.get(ME_KEY) || '') + '-' + ch; }
  function unreadIn(ch){
    var seen = +(ls.get(seenKey(ch)) || 0), mine = ls.get(ME_KEY);
    return msgsIn(ch).filter(function(m){ return m.at > seen && m.by !== mine; }).length;
  }
  function markSeen(ch){ var list = msgsIn(ch); if(list.length) ls.set(seenKey(ch), String(list[list.length - 1].at)); }
  function chatTime(ms){
    var d = new Date(ms), t = d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    return dayOf(ms) === todayStr() ? t : d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }) + ', ' + t;
  }
  function linkify(el, text){
    var re = /(https?:\\/\\/[^\\s<]+[^\\s<.,;:!?)\\]'"])/gi, last = 0, m;
    while((m = re.exec(text))){
      if(m.index > last) el.appendChild(document.createTextNode(text.slice(last, m.index)));
      var a = document.createElement('a'); a.href = m[0]; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = m[0];
      el.appendChild(a); last = m.index + m[0].length;
    }
    if(last < text.length) el.appendChild(document.createTextNode(text.slice(last)));
  }
  function openChat(){ if(!me()) return; chatOpen = true; ss.set('chat-open', '1'); $('chatPanel').hidden = false; renderChat(true); renderTop(); }
  function closeChat(){ chatOpen = false; ss.del('chat-open'); $('chatPanel').hidden = true; renderTop(); }
  function renderChat(focus){
    var v = me(); if(!v){ closeChat(); return; }
    var chans = channelsFor(v);
    if(!chans.some(function(c){ return c.id === chatChan; })) chatChan = 'all';
    var box = $('chans'); box.textContent = '';
    chans.forEach(function(c){
      var b = document.createElement('button'); b.type = 'button'; b.className = 'chan'; b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', c.id === chatChan ? 'true' : 'false'); b.textContent = c.name;
      var n = c.id === chatChan ? 0 : unreadIn(c.id);
      if(n){ var bd = document.createElement('span'); bd.className = 'badge'; bd.textContent = n; b.appendChild(bd); }
      b.addEventListener('click', function(){ chatChan = c.id; ss.set('chat-chan', c.id); renderChat(true); renderTop(); });
      box.appendChild(b);
    });
    var who = state.people.filter(function(p){ return canSeeChannel(p, chatChan); }).map(function(p){ return p.name; });
    $('chatNote').textContent = 'Seen by ' + who.join(', ') + '.';
    var list = $('msgs'), atBottom = list.scrollHeight - list.scrollTop - list.clientHeight < 60;
    list.textContent = '';
    var msgs = msgsIn(chatChan);
    if(!msgs.length){ var e = document.createElement('p'); e.className = 'nomsg'; e.textContent = 'No messages yet. Say hello to the team.'; list.appendChild(e); }
    var lastDay = '';
    msgs.forEach(function(m){
      var d = dayOf(m.at);
      if(d !== lastDay){ lastDay = d; var sep = document.createElement('span'); sep.className = 'day';
        sep.textContent = d === todayStr() ? 'Today' : new Date(m.at).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }); list.appendChild(sep); }
      var from = person(m.by), mine = m.by === v.id;
      var row = document.createElement('div'); row.className = 'msg k' + ((from ? from.color : 0) % 7) + (mine ? ' mine' : '');
      row.innerHTML = (from ? avatarHtml(from) : '<div class="photo initials">?</div>') + '<div class="bubble"><div class="who"><b></b><span></span></div><p></p></div>';
      row.querySelector('.who b').textContent = mine ? 'You' : (from ? from.name : 'Former member');
      row.querySelector('.who span').textContent = chatTime(m.at);
      linkify(row.querySelector('p'), m.text);
      if((mine || v.role === 'superuser') && mode !== 'readonly'){
        var rm = document.createElement('button'); rm.type = 'button'; rm.className = 'rm'; rm.textContent = 'Delete';
        rm.setAttribute('aria-label', 'Delete message');
        rm.addEventListener('click', function(){ change({ type: 'mdel', ch: chatChan, id: m.id }); renderChat(); });
        row.querySelector('.who').appendChild(rm);
      }
      list.appendChild(row);
    });
    if(atBottom || focus) list.scrollTop = list.scrollHeight;
    markSeen(chatChan);
    var ta = $('chatText');
    if(focus && mode !== 'readonly'){ try { var dr = ss.get('chat-draft'); if(dr && !ta.value) ta.value = dr; } catch(e){} setTimeout(function(){ ta.focus(); }, 0); }
  }
  function sendChat(){
    var v = me(), ta = $('chatText'), text = ta.value.trim();
    if(!v || !text || mode === 'readonly' || !canSeeChannel(v, chatChan)) return;
    change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: text.slice(0, 4000), at: Date.now() } });
    ta.value = ''; ss.del('chat-draft'); ss.set('chat-refocus', '1');
    renderChat(); $('msgs').scrollTop = $('msgs').scrollHeight; ta.focus(); renderTop();
  }
  $('chatBtn').addEventListener('click', function(){ chatOpen ? closeChat() : openChat(); });
  $('chatClose').addEventListener('click', closeChat);
  $('composer').addEventListener('submit', function(e){ e.preventDefault(); sendChat(); });
  $('chatText').addEventListener('keydown', function(e){ if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); sendChat(); } });
  $('chatText').addEventListener('input', function(){ ss.set('chat-draft', $('chatText').value); var t = $('chatText'); t.style.height = 'auto'; t.style.height = Math.min(140, t.scrollHeight) + 'px'; });

  // ---------- task actions ----------""")

# ---- journal ops for chat
rep("""  function applyOp(st, o){""", """  function applyOp(st, o){
    if(o.type === 'msg'){
      st.chat = st.chat || {}; var cl = st.chat[o.ch] = st.chat[o.ch] || [];
      if(!cl.some(function(m){ return m.id === o.m.id; })){ cl.push(JSON.parse(JSON.stringify(o.m))); cl.sort(function(a, b){ return a.at - b.at; }); }
      if(cl.length > 300) st.chat[o.ch] = cl.slice(cl.length - 300);
      return;
    }
    if(o.type === 'mdel'){
      if(st.chat && st.chat[o.ch]) st.chat[o.ch] = st.chat[o.ch].filter(function(m){ return m.id !== o.id; });
      return;
    }""")
rep("  function content(st){ return JSON.stringify(st.people); }",
    "  function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {} }); }")

# ---- reopen chat after a reload
rep("  render();\n  if(!me()) openWho();", """  render();
  if(!me()) openWho();
  else if(chatOpen){ $('chatPanel').hidden = false; renderChat(true); renderTop(); }""")
open(p,'w').write(s)
print('patched')
