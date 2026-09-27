p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

rep(".chat-acts{display:flex;gap:14px;align-items:center}", """.chat-acts{display:flex;gap:14px;align-items:center}
.callbtn{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:50%;border:1px solid var(--line);color:var(--ink);text-decoration:none;background:var(--surface)}
.callbtn:hover{border-color:var(--accent);color:var(--accent)}
.readonly .callbtn{display:none}
.callcard{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;margin-top:2px}
.callcard .ci{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:var(--accent-ink)}
.callcard b{display:block;font-size:14px}
.callcard small{display:block;font-size:12px;opacity:.8}
.join{grid-column:1/-1;display:inline-flex;justify-content:center;align-items:center;gap:6px;border-radius:10px;padding:7px 12px;background:var(--accent);color:var(--accent-ink);font-weight:700;text-decoration:none;font-size:14px}
.msg.mine .join{background:var(--surface);color:var(--ink)}
.toast.call{cursor:default;animation:toastIn .25s ease-out,ringPulse 1.2s ease-in-out 3}
.toast .join{grid-column:auto;padding:6px 12px;font-size:13px}
.toast .x{background:none;border:0;cursor:pointer}
@keyframes ringPulse{50%{box-shadow:0 0 0 6px color-mix(in srgb,var(--accent) 35%,transparent)}}""")

PHONE = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5l2.6 3.4-1.6 2.3a13 13 0 006.2 6.2l2.3-1.6 3.4 2.6-1.3 3A2 2 0 0116.3 20 16.3 16.3 0 014 7.7a2 2 0 011.6-2.2z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>'
VIDEO = '<svg width="17" height="17" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6.5" width="12.5" height="11" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M15.5 10.5l5-3v9l-5-3z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>'
rep("""<span class="chat-acts"><a class="tfiles\"""",
    """<span class="chat-acts"><a class="callbtn" id="voiceCall" target="_blank" rel="noopener noreferrer" href="#" title="Start a voice call" aria-label="Start a voice call">""" + PHONE.replace("'", "\\'") + """</a><a class="callbtn" id="videoCall" target="_blank" rel="noopener noreferrer" href="#" title="Start a video call" aria-label="Start a video call">""" + VIDEO.replace("'", "\\'") + """</a><a class="tfiles\"""")

# helpers + wiring (before sendChat helpers block)
rep("""  function msgPreview(m){""", """  // ---- calls: rooms on Jitsi Meet, opened in a new tab
  var PHONE_SVG = '""" + PHONE.replace("'", "\\'") + """', VIDEO_SVG = '""" + VIDEO.replace("'", "\\'") + """';
  function newRoom(){ var ch = String(chatChan || 'all').replace(/[^a-z0-9]+/gi, '').slice(0, 24); return 'akamedia-' + ch + '-' + uid('r').replace(/[^a-z0-9]/gi, '').slice(-10); }
  function roomUrl(room, kind){
    var v = me(), nm = v ? v.name : 'a.k.a. Media';
    var h = '#userInfo.displayName=%22' + encodeURIComponent(nm) + '%22&config.prejoinConfig.enabled=false';
    if(kind === 'voice') h += '&config.startWithVideoMuted=true';
    return 'https://meet.jit.si/' + room + h;
  }
  var nextRooms = {};
  function armCallButtons(){
    ['voice', 'video'].forEach(function(kind){
      var a = $(kind + 'Call'); if(!a) return;
      if(!nextRooms[kind]) nextRooms[kind] = newRoom();
      a.href = roomUrl(nextRooms[kind], kind);
    });
  }
  ['voice', 'video'].forEach(function(kind){
    var a = $(kind + 'Call'); if(!a) return;
    a.addEventListener('click', function(e){
      var v = me();
      if(!v || mode === 'readonly' || !canSeeChannel(v, chatChan)){ e.preventDefault(); return; }
      var room = nextRooms[kind] || newRoom();
      change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: '', at: Date.now(), call: { kind: kind, room: room } } });
      ls.set(heardKey(), String(Date.now()));
      nextRooms[kind] = null;
      setTimeout(function(){ renderChat(); armCallButtons(); }, 0);
    });
  });
  function callCard(m, mine){
    var c = m.call || {}, box = document.createElement('div'); box.className = 'callcard';
    var ci = document.createElement('span'); ci.className = 'ci'; ci.innerHTML = c.kind === 'voice' ? PHONE_SVG : VIDEO_SVG;
    var t = document.createElement('div'); var b = document.createElement('b'); b.textContent = (c.kind === 'voice' ? 'Voice call' : 'Video call');
    var sm = document.createElement('small'); var mins = Math.round((Date.now() - m.at) / 60000);
    sm.textContent = mins < 2 ? 'Started just now' : mins < 60 ? 'Started ' + mins + ' min ago' : 'Started at ' + chatTime(m.at);
    t.append(b, sm);
    var j = document.createElement('a'); j.className = 'join'; j.target = '_blank'; j.rel = 'noopener noreferrer'; j.href = roomUrl(c.room, c.kind);
    j.textContent = mine ? 'Rejoin call' : 'Join call';
    box.append(ci, t, j); return box;
  }
  function ring(){
    var ac = ctx(); if(!ac) return false; var n = ac.currentTime + 0.02;
    for(var r = 0; r < 3; r++){ var t0 = n + r * 1.4; [0, 0.2].forEach(function(o){ tone(ac, 440, t0 + o, 0.18, 0.14, 'sine'); tone(ac, 480, t0 + o, 0.18, 0.14, 'sine'); }); }
    return ac.state === 'running';
  }
  function playRing(){
    if(!soundOn) return;
    var ok = false; try { ok = ring(); } catch(e){}
    if(!ok){ var go = function(){ document.removeEventListener('pointerdown', go, true); document.removeEventListener('keydown', go, true); try { ring(); } catch(e){} }; document.addEventListener('pointerdown', go, true); document.addEventListener('keydown', go, true); }
  }
  function callToast(f, v){
    var box = $('toasts'); if(!box) return;
    var from = person(f.m.by), c = f.m.call || {}, peer = dmPeer(f.ch, v);
    var t = document.createElement('div'); t.className = 'toast call' + (from ? ' k' + (from.color % 7) : ''); t.setAttribute('role', 'alert');
    t.innerHTML = (from ? avatarHtml(from) : '<span></span>') + '<div><b></b><span></span></div><a class="join" target="_blank" rel="noopener noreferrer"></a><button type="button" class="x" aria-label="Dismiss">\\u00d7</button>';
    t.querySelector('div b').textContent = (from ? from.name : 'Someone') + ' is calling' + (peer ? ' you' : ' ' + chanName(f.ch, v));
    t.querySelector('div span').textContent = c.kind === 'voice' ? 'Voice call' : 'Video call';
    var j = t.querySelector('.join'); j.href = roomUrl(c.room, c.kind); j.textContent = 'Join';
    j.addEventListener('click', function(){ t.remove(); });
    t.querySelector('.x').addEventListener('click', function(){ t.remove(); });
    t.style.gridTemplateColumns = 'auto 1fr auto auto';
    box.appendChild(t);
    setTimeout(function(){ if(t.parentNode) t.remove(); }, 60000);
  }
  function msgPreview(m){ if(m.call) return m.call.kind === 'voice' ? 'Started a voice call' : 'Started a video call';""")

# render call messages
rep("""      if(!m.text) row.querySelector('p').hidden = true;""", """      if(!m.text) row.querySelector('p').hidden = true;
      if(m.call) row.querySelector('.bubble').appendChild(callCard(m, mine));""")
# arm buttons on each chat render
rep("""    markSeen(chatChan); recordRead(chatChan);""", """    markSeen(chatChan); recordRead(chatChan); armCallButtons();""")
# announce: calls ring (within 15 min), others as before
rep("""    var viewing = chatOpen && !document.hidden;
    var shown = fresh.filter(function(f){ return !(viewing && f.ch === chatChan); });""",
"""    var calls = fresh.filter(function(f){ return f.m.call && Date.now() - f.m.at < 15 * 60000; });
    fresh = fresh.filter(function(f){ return !f.m.call; });
    calls.slice(-2).forEach(function(f){ callToast(f, v); });
    if(calls.length) playRing();
    if(!fresh.length) return;
    var viewing = chatOpen && !document.hidden;
    var shown = fresh.filter(function(f){ return !(viewing && f.ch === chatChan); });""")
rep("""    shown.slice(-3).forEach(function(f){
      var from = person(f.m.by), peer = dmPeer(f.ch, v);
      toast({ person: from, title: (from ? from.name : 'Someone') + (peer ? '' : ' in ' + chanName(f.ch, v)), text: msgPreview(f.m), ch: f.ch });
    });
    playChime();""", """    shown.slice(-3).forEach(function(f){
      var from = person(f.m.by), peer = dmPeer(f.ch, v);
      toast({ person: from, title: (from ? from.name : 'Someone') + (peer ? '' : ' in ' + chanName(f.ch, v)), text: msgPreview(f.m), ch: f.ch });
    });
    if(!calls.length) playChime();""")
open(p,'w').write(s); print('ok')
