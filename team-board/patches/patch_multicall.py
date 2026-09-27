p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
rep(""".callcard{display:grid;""", """.callpick{margin-top:10px;border:1px solid var(--accent);border-radius:14px;padding:12px;background:var(--paper);display:flex;flex-direction:column;gap:10px}
.callpick .row1{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.callpick .row1 b{font-size:14px;margin-right:auto}
.callpick .kind{display:flex;gap:2px;background:var(--soft);border-radius:9px;padding:2px}
.callpick .kind button{border:0;background:none;border-radius:7px;padding:4px 10px;font-size:13px;color:var(--muted)}
.callpick .kind button[aria-pressed=true]{background:var(--surface);color:var(--ink);font-weight:600}
.callpick .ppl{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:6px}
.callpick label{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:10px;padding:5px 8px;background:var(--surface);font-size:14px;cursor:pointer}
.callpick label:has(input:checked){border-color:var(--accent)}
.callpick label .photo{width:24px;height:24px;border-width:1.5px}
.callpick label .initials{font-size:11px}
.callpick input{accent-color:var(--accent)}
.callpick .row2{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.callpick .row2 .link{font-size:13px}
.callpick .start{margin-left:auto;display:inline-flex;align-items:center;gap:6px;border-radius:10px;padding:7px 14px;background:var(--accent);color:var(--accent-ink);font-weight:700;text-decoration:none;font-size:14px}
.callpick .start[aria-disabled=true]{opacity:.45;pointer-events:none}
.callcard .with{display:block;font-size:12px;opacity:.8}
.callcard{display:grid;""")
rep("""        '<p class="chat-note" id="chatNote"></p></div>' +""", """        '<p class="chat-note" id="chatNote"></p><div class="callpick" id="callPick" hidden></div></div>' +""")

old_start = s.index("  var nextRooms = {};\n  function armCallButtons(){")
old_end = s.index("  function callCard(m, mine){")
s = s[:old_start] + r"""  // Call picker: choose who to call; only they are rung
  var pick = null; // {kind, room, sel: {id: true}}
  function defaultInvitees(){
    var v = me(), peer = dmPeer(chatChan, v), sel = {};
    if(peer) sel[peer.id] = true;
    else state.people.forEach(function(p){ if(p.id !== v.id && canSeeChannel(p, chatChan)) sel[p.id] = true; });
    return sel;
  }
  function openPicker(kind){
    var v = me(); if(!v || mode === 'readonly') return;
    if(pick && pick.kind === kind && !$('callPick').hidden){ closePicker(); return; }
    pick = { kind: kind, room: newRoom(), sel: pick && !$('callPick').hidden ? pick.sel : defaultInvitees() };
    renderPicker();
  }
  function closePicker(){ pick = null; $('callPick').hidden = true; $('callPick').textContent = ''; }
  function renderPicker(){
    var box = $('callPick'), v = me(); if(!pick || !v){ closePicker(); return; }
    box.hidden = false; box.textContent = '';
    var r1 = document.createElement('div'); r1.className = 'row1';
    var t = document.createElement('b'); t.textContent = 'Who do you want to call?';
    var kd = document.createElement('div'); kd.className = 'kind'; kd.setAttribute('role', 'group'); kd.setAttribute('aria-label', 'Call type');
    [['voice', 'Voice'], ['video', 'Video']].forEach(function(k){
      var b = document.createElement('button'); b.type = 'button'; b.textContent = k[1]; b.setAttribute('aria-pressed', pick.kind === k[0] ? 'true' : 'false');
      b.addEventListener('click', function(){ pick.kind = k[0]; renderPicker(); }); kd.appendChild(b);
    });
    r1.append(t, kd); box.appendChild(r1);
    var ppl = document.createElement('div'); ppl.className = 'ppl';
    state.people.forEach(function(p){
      if(p.id === v.id) return;
      var l = document.createElement('label'); l.className = 'k' + (p.color % 7);
      var cb = document.createElement('input'); cb.type = 'checkbox'; cb.checked = !!pick.sel[p.id];
      cb.addEventListener('change', function(){ if(cb.checked) pick.sel[p.id] = true; else delete pick.sel[p.id]; paintStart(); });
      l.appendChild(cb); l.insertAdjacentHTML('beforeend', avatarHtml(p));
      l.appendChild(document.createTextNode(p.name)); ppl.appendChild(l);
    });
    box.appendChild(ppl);
    var r2 = document.createElement('div'); r2.className = 'row2';
    var all = document.createElement('button'); all.type = 'button'; all.className = 'link'; all.textContent = 'Everyone';
    all.addEventListener('click', function(){ state.people.forEach(function(p){ if(p.id !== v.id) pick.sel[p.id] = true; }); renderPicker(); });
    var none = document.createElement('button'); none.type = 'button'; none.className = 'link'; none.textContent = 'Clear';
    none.addEventListener('click', function(){ pick.sel = {}; renderPicker(); });
    var cancel = document.createElement('button'); cancel.type = 'button'; cancel.className = 'link'; cancel.textContent = 'Cancel';
    cancel.addEventListener('click', closePicker);
    var go = document.createElement('a'); go.className = 'start'; go.id = 'startCall'; go.target = '_blank'; go.rel = 'noopener noreferrer';
    go.addEventListener('click', function(e){
      var ids = Object.keys(pick.sel).filter(function(id){ return person(id); });
      if(!ids.length){ e.preventDefault(); return; }
      startCall(pick.kind, pick.room, ids);
    });
    r2.append(all, none, cancel, go); box.appendChild(r2);
    paintStart();
  }
  function paintStart(){
    var go = $('startCall'); if(!go || !pick) return;
    var n = Object.keys(pick.sel).length;
    go.innerHTML = (pick.kind === 'voice' ? PHONE_SVG : VIDEO_SVG) + '<span></span>';
    go.querySelector('span').textContent = n ? 'Call ' + (n === 1 ? person(Object.keys(pick.sel)[0]).name : n + ' people') : 'Pick someone';
    go.setAttribute('aria-disabled', n ? 'false' : 'true');
    go.href = roomUrl(pick.room, pick.kind);
  }
  function startCall(kind, room, ids){
    var v = me(); if(!v) return;
    var call = { kind: kind, room: room, invite: ids.slice() };
    var here = canSeeChannel(v, chatChan) && ids.every(function(id){ var p = person(id); return p && canSeeChannel(p, chatChan); });
    if(here) change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: '', at: Date.now(), call: call } });
    else ids.forEach(function(id, i){ change({ type: 'msg', ch: dmId(v.id, id), m: { id: uid('m'), by: v.id, text: '', at: Date.now() + i, call: call } }); });
    ls.set(heardKey(), String(Date.now() + ids.length));
    setTimeout(function(){ closePicker(); renderChat(); }, 0);
  }
  function armCallButtons(){ if(pick && !$('callPick').hidden) paintStart(); }
  ['voice', 'video'].forEach(function(kind){
    var a = $(kind + 'Call'); if(!a) return;
    a.removeAttribute('target'); a.setAttribute('role', 'button');
    a.addEventListener('click', function(e){ e.preventDefault(); openPicker(kind); });
  });
""" + s[old_end:]

# call card: show who was invited
rep("""    t.append(b, sm);
    var j = document.createElement('a'); j.className = 'join';""", """    t.append(b, sm);
    if(Array.isArray(c.invite) && c.invite.length){
      var w = document.createElement('small'); w.className = 'with';
      var names = c.invite.map(function(id){ var p = person(id); return p ? (me() && p.id === me().id ? 'you' : p.name) : null; }).filter(Boolean);
      w.textContent = 'With ' + names.join(', ');
      t.appendChild(w);
    }
    var j = document.createElement('a'); j.className = 'join';""")
# ring only invitees
rep("""    var calls = fresh.filter(function(f){ return f.m.call && Date.now() - f.m.at < 15 * 60000; });""",
    """    var calls = fresh.filter(function(f){ var c = f.m.call; return c && Date.now() - f.m.at < 15 * 60000 && (!Array.isArray(c.invite) || c.invite.indexOf(v.id) >= 0); });
    var seenRooms = {}; calls = calls.filter(function(f){ if(seenRooms[f.m.call.room]) return false; seenRooms[f.m.call.room] = true; return true; });""")
open(p,'w').write(s); print('ok')
