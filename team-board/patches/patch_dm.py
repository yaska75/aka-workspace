p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

# ---- CSS
rep(".nomsg{margin:auto;", """.chan-group{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.chan-group + .chan-group{margin-top:8px}
.chan-label{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-right:2px;min-width:52px}
.chan.dm{display:inline-flex;align-items:center;gap:6px;padding:3px 10px 3px 3px}
.chan.dm .photo{width:22px;height:22px;border-width:1.5px;border-radius:50%}
.chan.dm .initials{font-size:11px}
.receipt{align-self:flex-end;display:flex;align-items:center;gap:5px;margin:-4px 2px 0 0;font-size:11.5px;color:var(--muted)}
.receipt svg{color:var(--accent);flex:none}
.receipt.none svg{color:var(--muted)}
.receipt .only{border:1px solid var(--line);border-radius:999px;padding:0 6px;font-size:10px;letter-spacing:.06em;text-transform:uppercase}
.toasts{position:fixed;left:16px;bottom:16px;display:flex;flex-direction:column;gap:8px;z-index:60;max-width:min(360px,calc(100% - 32px))}
.toast{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;background:var(--ink);color:var(--surface);border-radius:14px;padding:9px 10px 9px 9px;box-shadow:0 12px 30px rgba(0,0,0,.25);text-align:left;border:0;font:inherit;cursor:pointer;animation:toastIn .25s ease-out}
.toast .photo{width:32px;height:32px;border-width:2px}
.toast b{display:block;font-size:13px}
.toast span{display:block;font-size:13px;opacity:.85;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:250px}
.toast .x{color:inherit;opacity:.6;font-size:18px;padding:0 4px}
.toast.rr{background:var(--surface);color:var(--ink);border:1px solid var(--accent)}
@keyframes toastIn{from{transform:translateY(12px);opacity:0}to{transform:none;opacity:1}}
.nomsg{margin:auto;""")

# ---- state cleaning
rep("    if(!s.chat || typeof s.chat !== 'object' || Array.isArray(s.chat)) s.chat = {};",
"""    if(!s.chat || typeof s.chat !== 'object' || Array.isArray(s.chat)) s.chat = {};
    if(!s.reads || typeof s.reads !== 'object' || Array.isArray(s.reads)) s.reads = {};""")

# ---- markup: toast container
rep("""    '<aside class="chat k0" id="chatPanel" hidden aria-labelledby="chatTitle">' +""",
"""    '<div class="toasts" id="toasts" aria-live="polite"></div>' +
    '<aside class="chat k0" id="chatPanel" hidden aria-labelledby="chatTitle">' +""")

# ---- channels incl. DMs
rep("""  function canSeeChannel(v, ch){
    if(!v) return false;""", """  function dmId(a, b){ return 'dm:' + [a, b].sort().join('|'); }
  function dmPeer(ch, v){ if(!/^dm:/.test(ch)) return null; var ids = ch.slice(3).split('|'); var o = ids[0] === v.id ? ids[1] : ids[0]; return person(o); }
  function canSeeChannel(v, ch){
    if(!v) return false;
    if(/^dm:/.test(ch)) return ch.slice(3).split('|').indexOf(v.id) >= 0;""")
rep("""  function channelsFor(v){ return CHANNELS.filter(function(c){ return canSeeChannel(v, c.id); }); }""",
"""  function groupsFor(v){ return CHANNELS.filter(function(c){ return canSeeChannel(v, c.id); }); }
  function dmsFor(v){ return state.people.filter(function(p){ return p.id !== v.id; }).map(function(p){ return { id: dmId(v.id, p.id), name: p.name, dm: p }; }); }
  function channelsFor(v){ return groupsFor(v).concat(dmsFor(v)); }
  function chanName(ch, v){ var peer = dmPeer(ch, v); if(peer) return peer.name; for(var i = 0; i < CHANNELS.length; i++){ if(CHANNELS[i].id === ch) return CHANNELS[i].name; } return 'Chat'; }""")

# ---- render channel tabs in two groups
rep("""    var box = $('chans'); box.textContent = '';
    chans.forEach(function(c){
      var b = document.createElement('button'); b.type = 'button'; b.className = 'chan'; b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', c.id === chatChan ? 'true' : 'false'); b.textContent = c.name;
      var n = c.id === chatChan ? 0 : unreadIn(c.id);
      if(n){ var bd = document.createElement('span'); bd.className = 'badge'; bd.textContent = n; b.appendChild(bd); }
      b.addEventListener('click', function(){ chatChan = c.id; ss.set('chat-chan', c.id); renderChat(true); renderTop(); });
      box.appendChild(b);
    });
    var who = state.people.filter(function(p){ return canSeeChannel(p, chatChan); }).map(function(p){ return p.name; });
    $('chatNote').textContent = 'Seen by ' + who.join(', ') + '.';""",
"""    var box = $('chans'); box.textContent = '';
    function chip(c, grp){
      var b = document.createElement('button'); b.type = 'button'; b.className = 'chan' + (c.dm ? ' dm k' + (c.dm.color % 7) : ''); b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', c.id === chatChan ? 'true' : 'false');
      if(c.dm){ b.innerHTML = avatarHtml(c.dm); b.setAttribute('aria-label', 'Private chat with ' + c.name); }
      b.appendChild(document.createTextNode(c.name));
      var n = c.id === chatChan ? 0 : unreadIn(c.id);
      if(n){ var bd = document.createElement('span'); bd.className = 'badge'; bd.textContent = n; b.appendChild(bd); }
      b.addEventListener('click', function(){ chatChan = c.id; ss.set('chat-chan', c.id); renderChat(true); renderTop(); });
      grp.appendChild(b);
    }
    [['Groups', groupsFor(v)], ['Direct', dmsFor(v)]].forEach(function(g){
      if(!g[1].length) return;
      var grp = document.createElement('div'); grp.className = 'chan-group';
      var lb = document.createElement('span'); lb.className = 'chan-label'; lb.textContent = g[0]; grp.appendChild(lb);
      g[1].forEach(function(c){ chip(c, grp); });
      box.appendChild(grp);
    });
    var peer = dmPeer(chatChan, v);
    $('chatTitle').textContent = peer ? 'Chat with ' + peer.name : 'Team chat';
    if(peer) $('chatNote').textContent = 'Private: only you and ' + peer.name + ' see this chat.';
    else {
      var who = state.people.filter(function(p){ return canSeeChannel(p, chatChan); }).map(function(p){ return p.name; });
      $('chatNote').textContent = 'Seen by ' + who.join(', ') + '.';
    }""")

rep("""    if(!msgs.length){ var e = document.createElement('p'); e.className = 'nomsg'; e.textContent = 'No messages yet. Say hello to the team.'; list.appendChild(e); }""",
"""    if(!msgs.length){ var e = document.createElement('p'); e.className = 'nomsg'; e.textContent = peer ? 'No messages yet. Say hello to ' + peer.name + '.' : 'No messages yet. Say hello to the team.'; list.appendChild(e); }
    var showRR = v.role === 'superuser', rrPrev = null, rrSets = showRR ? msgs.map(function(m){ return readersOf(chatChan, m); }) : [];""")
rep("""    msgs.forEach(function(m){
      var d = dayOf(m.at);""", """    msgs.forEach(function(m, mi){
      var d = dayOf(m.at);""")
rep("""      list.appendChild(row);
    });
    if(atBottom || focus) list.scrollTop = list.scrollHeight;""",
"""      list.appendChild(row);
      if(showRR){
        var rs = rrSets[mi], next = rrSets[mi + 1], key = rs.read.map(function(p){ return p.id; }).join(',');
        var nextKey = next ? next.read.map(function(p){ return p.id; }).join(',') : null;
        if(key !== nextKey) list.appendChild(receiptEl(rs));
      }
    });
    if(atBottom || focus) list.scrollTop = list.scrollHeight;""")

# ---- helpers: readers, receipts, sounds, toasts, read tracking
rep("""  function openChat(){""", r"""  function readAt(ch, pid){ var r = state.reads[ch] && state.reads[ch][pid]; return r ? (typeof r === 'number' ? r : r.at || 0) : 0; }
  function readWhen(ch, pid){ var r = state.reads[ch] && state.reads[ch][pid]; return r && typeof r === 'object' ? r.t : null; }
  function readersOf(ch, m){
    var aud = state.people.filter(function(p){ return p.id !== m.by && canSeeChannel(p, ch); });
    return { read: aud.filter(function(p){ return readAt(ch, p.id) >= m.at; }), all: aud, ch: ch };
  }
  var TICKS = '<svg width="16" height="11" viewBox="0 0 16 11" aria-hidden="true"><path d="M1 6l3 3L10 2M6 8.5l.8.8L14 2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function receiptEl(rs){
    var el = document.createElement('div'); el.className = 'receipt' + (rs.read.length ? '' : ' none');
    var txt = !rs.all.length ? 'No one else in this chat' : !rs.read.length ? 'Not read yet'
      : rs.read.length === rs.all.length ? (rs.all.length === 1 ? 'Read by ' + rs.read[0].name : 'Read by everyone')
      : 'Read by ' + rs.read.map(function(p){ return p.name; }).join(', ');
    el.innerHTML = TICKS + '<span></span><span class="only">Only you</span>';
    el.querySelector('span').textContent = txt;
    el.title = rs.read.map(function(p){ var t = readWhen(rs.ch, p.id); return p.name + (t ? ' read it ' + chatTime(t) : ''); }).join('\n') || 'Read receipts are only shown to the superuser';
    return el;
  }
  // record that I've read up to the latest message someone else posted here
  function recordRead(ch){
    var v = me(); if(!v || mode === 'readonly' || document.hidden) return;
    var list = msgsIn(ch), latest = 0;
    for(var i = list.length - 1; i >= 0; i--){ if(list[i].by !== v.id){ latest = list[i].at; break; } }
    if(latest && latest > readAt(ch, v.id)) change({ type: 'read', ch: ch, pid: v.id, at: latest, t: Date.now() });
  }
  // --- message sounds
  function chime(){
    var ac = ctx(); if(!ac) return false; var n = ac.currentTime + 0.01;
    bell(ac, 880, n, 0.22, 0.16); bell(ac, 1318.5, n + 0.11, 0.45, 0.16);
    return ac.state === 'running';
  }
  function whoosh(){
    var ac = ctx(); if(!ac) return; var n = ac.currentTime + 0.01;
    var o = ac.createOscillator(), g = ac.createGain(); o.type = 'sine';
    o.frequency.setValueAtTime(420, n); o.frequency.exponentialRampToValueAtTime(980, n + 0.14);
    g.gain.setValueAtTime(0.0001, n); g.gain.exponentialRampToValueAtTime(0.09, n + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, n + 0.18);
    o.connect(g); g.connect(ac.destination); o.start(n); o.stop(n + 0.22);
  }
  var pendingChime = false;
  function playChime(){
    if(!soundOn) return;
    var ok = false; try { ok = chime(); } catch(e){}
    if(!ok && !pendingChime){
      // browsers block sound until the page is touched; play it on the first tap or key
      pendingChime = true;
      var go = function(){ pendingChime = false; document.removeEventListener('pointerdown', go, true); document.removeEventListener('keydown', go, true); try { chime(); } catch(e){} };
      document.addEventListener('pointerdown', go, true); document.addEventListener('keydown', go, true);
    }
  }
  function toast(opts){
    var box = $('toasts'); if(!box) return;
    var t = document.createElement('button'); t.type = 'button'; t.className = 'toast' + (opts.rr ? ' rr' : '') + (opts.person ? ' k' + (opts.person.color % 7) : '');
    t.innerHTML = (opts.person ? avatarHtml(opts.person) : '<span></span>') + '<div><b></b><span></span></div><span class="x" aria-hidden="true">×</span>';
    t.querySelector('div b').textContent = opts.title; t.querySelector('div span').textContent = opts.text || '';
    t.addEventListener('click', function(e){ t.remove(); if(!e.target.classList.contains('x') && opts.ch){ chatChan = opts.ch; ss.set('chat-chan', opts.ch); openChat(); } });
    box.appendChild(t); while(box.children.length > 4) box.removeChild(box.firstChild);
    setTimeout(function(){ if(t.parentNode) t.remove(); }, opts.rr ? 12000 : 9000);
  }
  function heardKey(){ return 'chat-heard-' + (ls.get(ME_KEY) || ''); }
  // on load: chime + pop-up for anything new from others since this browser last checked
  function announceNew(){
    var v = me(); if(!v) return;
    var heard = +(ls.get(heardKey()) || 0), fresh = [], newest = heard;
    channelsFor(v).forEach(function(c){ msgsIn(c.id).forEach(function(m){
      if(m.at > newest) newest = m.at;
      if(heard && m.at > heard && m.by !== v.id) fresh.push({ m: m, ch: c.id });
    }); });
    ls.set(heardKey(), String(Math.max(newest, heard || Date.now())));
    if(!fresh.length) return;
    fresh.sort(function(a, b){ return a.m.at - b.m.at; });
    var viewing = chatOpen && !document.hidden;
    var shown = fresh.filter(function(f){ return !(viewing && f.ch === chatChan); });
    shown.slice(-3).forEach(function(f){
      var from = person(f.m.by), peer = dmPeer(f.ch, v);
      toast({ person: from, title: (from ? from.name : 'Someone') + (peer ? '' : ' in ' + chanName(f.ch, v)), text: f.m.text, ch: f.ch });
    });
    playChime();
  }
  // superuser only: pop-up when someone reads one of your messages
  function announceReads(){
    var v = me(); if(!v || v.role !== 'superuser') return;
    var key = 'rr-known-' + v.id, known = {}, first = ls.get(key) === null;
    try { known = JSON.parse(ls.get(key) || '{}') || {}; } catch(e){}
    var news = [];
    channelsFor(v).forEach(function(c){
      var mineMsgs = msgsIn(c.id).filter(function(m){ return m.by === v.id; }); if(!mineMsgs.length) return;
      state.people.forEach(function(p){
        if(p.id === v.id || !canSeeChannel(p, c.id)) return;
        var at = readAt(c.id, p.id), k = c.id + '|' + p.id;
        if(at > (known[k] || 0)){
          var last = null; mineMsgs.forEach(function(m){ if(m.at <= at && m.at > (known[k] || 0)) last = m; });
          if(last) news.push({ p: p, ch: c.id, m: last });
          known[k] = at;
        }
      });
    });
    ls.set(key, JSON.stringify(known));
    if(first) return;
    news.slice(-3).forEach(function(n){
      var peer = dmPeer(n.ch, v);
      toast({ rr: true, person: n.p, title: n.p.name + ' read your message' + (peer ? '' : ' in ' + chanName(n.ch, v)), text: n.m.text, ch: n.ch });
    });
  }
  function openChat(){""")

# markSeen -> also record read
rep("""    markSeen(chatChan);
    var ta = $('chatText');""", """    markSeen(chatChan); recordRead(chatChan);
    var ta = $('chatText');""")
# send sound
rep("""    change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: text.slice(0, 4000), at: Date.now() } });""",
"""    change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: text.slice(0, 4000), at: Date.now() } });
    try { whoosh(); } catch(e){}
    ls.set(heardKey(), String(Date.now()));""")
# ops
rep("""    if(o.type === 'mdel'){""", """    if(o.type === 'read'){
      st.reads = st.reads || {}; var rc = st.reads[o.ch] = st.reads[o.ch] || {};
      var cur = rc[o.pid], curAt = cur ? (typeof cur === 'number' ? cur : cur.at) : 0;
      if(o.at > curAt) rc[o.pid] = { at: o.at, t: o.t };
      return;
    }
    if(o.type === 'mdel'){""")
rep("""  function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {} }); }""",
    """  function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {}, r: st.reads || {} }); }""")
# tab title count
rep("""    $('chatBadge').hidden = !unread; $('chatBadge').textContent = unread > 99 ? '99+' : unread;""",
"""    $('chatBadge').hidden = !unread; $('chatBadge').textContent = unread > 99 ? '99+' : unread;
    document.title = (unread ? '(' + unread + ') ' : '') + 'a.k.a. Media team board';""")
# startup
rep("""  else if(chatOpen){ $('chatPanel').hidden = false; document.body.classList.add('chat-on'); renderChat(true); renderTop(); }""",
"""  else if(chatOpen){ $('chatPanel').hidden = false; document.body.classList.add('chat-on'); renderChat(true); renderTop(); }
  setTimeout(function(){ announceNew(); announceReads(); }, 400);
  document.addEventListener('visibilitychange', function(){ if(!document.hidden && chatOpen) recordRead(chatChan); });""")
open(p,'w').write(s); print('ok')
