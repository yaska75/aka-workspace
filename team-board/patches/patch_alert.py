p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
BELL = '<svg width="17" height="17" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16.5V11a6 6 0 0112 0v5.5l1.5 2H4.5zM10 20.5a2 2 0 004 0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round"/><path d="M3 7.5c.6-1.7 1.6-3.1 3-4M21 7.5c-.6-1.7-1.6-3.1-3-4" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>'
rep(".callcard{display:grid;", """.callbtn.alertbtn{color:var(--accent);border-color:color-mix(in srgb,var(--accent) 45%,var(--line))}
.callpick .note{font:inherit;font-size:14px;color:var(--ink);border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:7px 10px;width:100%}
.alertcard{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center}
.alertcard .ci{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--strike);color:#fff}
.alertcard b{display:block;font-size:14px}
.alertcard small{display:block;font-size:12px;opacity:.85}
.alertcard .note{grid-column:1/-1;margin:0;font-size:14px}
.alarm{position:fixed;inset:0;z-index:80;display:grid;place-items:center;padding:16px;background:color-mix(in srgb,#B0102C 55%,transparent);animation:alarmFlash 1s steps(2,jump-none) infinite}
.alarm .box{background:var(--surface);color:var(--ink);border-radius:22px;padding:26px 24px;max-width:420px;width:100%;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.45);display:flex;flex-direction:column;align-items:center;gap:10px;border:3px solid var(--strike)}
.alarm .box .photo{width:84px;height:84px;border-width:4px;animation:shake .6s ease-in-out infinite}
.alarm h2{margin:0;font-family:"Outfit","Instrument Sans",system-ui,sans-serif;font-size:26px;line-height:1.15;letter-spacing:-.02em}
.alarm p{margin:0;font-size:16px;color:var(--muted)}
.alarm p.msgtxt{color:var(--ink);font-size:18px;font-weight:600}
.alarm .ack{margin-top:6px;border:0;border-radius:12px;padding:12px 26px;background:var(--strike);color:#fff;font-weight:700;font-size:16px}
@keyframes alarmFlash{50%{background:color-mix(in srgb,#B0102C 20%,transparent)}}
@keyframes shake{25%{transform:rotate(-6deg)}75%{transform:rotate(6deg)}}
@media (prefers-reduced-motion:reduce){.alarm{animation:none}.alarm .box .photo{animation:none}}
.callcard{display:grid;""")
rep("""<a class="callbtn" id="voiceCall\"""", """<a class="callbtn alertbtn" id="alertBtn" role="button" href="#" title="Get someone\\u2019s attention" aria-label="Send an attention alert">""" + BELL + """</a><a class="callbtn" id="voiceCall\"""")
rep("    if(!s.reads || typeof s.reads !== 'object' || Array.isArray(s.reads)) s.reads = {};",
    "    if(!s.reads || typeof s.reads !== 'object' || Array.isArray(s.reads)) s.reads = {};\n    if(!s.acks || typeof s.acks !== 'object' || Array.isArray(s.acks)) s.acks = {};")
rep("  function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {}, r: st.reads || {} }); }",
    "  function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {}, r: st.reads || {}, a: st.acks || {} }); }")
rep("    if(o.type === 'read'){", """    if(o.type === 'ack'){
      st.acks = st.acks || {}; var ak = st.acks[o.id] = st.acks[o.id] || {};
      if(!ak[o.pid]) ak[o.pid] = o.t;
      return;
    }
    if(o.type === 'read'){""")

# picker: support alert mode
rep("""  function openPicker(kind){
    var v = me(); if(!v || mode === 'readonly') return;""", """  function openPicker(kind){
    var v = me(); if(!v || mode === 'readonly') return;
    if(kind === 'alert' && pick && pick.kind !== 'alert' && !$('callPick').hidden){ pick.kind = 'alert'; renderPicker(); return; }""")
rep("""    var t = document.createElement('b'); t.textContent = 'Who do you want to call?';""",
    """    var isAlert = pick.kind === 'alert';
    var t = document.createElement('b'); t.textContent = isAlert ? 'Who needs to see this now?' : 'Who do you want to call?';""")
rep("""    [['voice', 'Voice'], ['video', 'Video']].forEach(function(k){""", """    [['voice', 'Voice'], ['video', 'Video'], ['alert', 'Alert']].forEach(function(k){""")
rep("""    box.appendChild(ppl);
    var r2 = document.createElement('div'); r2.className = 'row2';""", """    box.appendChild(ppl);
    if(isAlert){
      var nt = document.createElement('input'); nt.type = 'text'; nt.className = 'note'; nt.id = 'alertNote'; nt.maxLength = 140;
      nt.placeholder = 'What is it about? (optional)'; nt.setAttribute('aria-label', 'Alert message'); nt.value = pick.note || '';
      nt.addEventListener('input', function(){ pick.note = nt.value; });
      nt.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); var g = $('startCall'); if(g) g.click(); } });
      box.appendChild(nt);
    }
    var r2 = document.createElement('div'); r2.className = 'row2';""")
rep("""    go.addEventListener('click', function(e){
      var ids = Object.keys(pick.sel).filter(function(id){ return person(id); });
      if(!ids.length){ e.preventDefault(); return; }
      startCall(pick.kind, pick.room, ids);
    });""", """    go.addEventListener('click', function(e){
      var ids = Object.keys(pick.sel).filter(function(id){ return person(id); });
      if(pick.kind === 'alert'){ e.preventDefault(); if(ids.length) sendAlert(ids, pick.note || ''); return; }
      if(!ids.length){ e.preventDefault(); return; }
      startCall(pick.kind, pick.room, ids);
    });""")
rep("""    go.innerHTML = (pick.kind === 'voice' ? PHONE_SVG : VIDEO_SVG) + '<span></span>';
    go.querySelector('span').textContent = n ? 'Call ' + (n === 1 ? person(Object.keys(pick.sel)[0]).name : n + ' people') : 'Pick someone';
    go.setAttribute('aria-disabled', n ? 'false' : 'true');
    go.href = roomUrl(pick.room, pick.kind);""", """    var who1 = n === 1 ? person(Object.keys(pick.sel)[0]).name : n + ' people';
    if(pick.kind === 'alert'){
      go.innerHTML = BELL_SVG + '<span></span>'; go.querySelector('span').textContent = n ? 'Alert ' + who1 : 'Pick someone';
      go.removeAttribute('target'); go.href = '#';
    } else {
      go.innerHTML = (pick.kind === 'voice' ? PHONE_SVG : VIDEO_SVG) + '<span></span>';
      go.querySelector('span').textContent = n ? 'Call ' + who1 : 'Pick someone';
      go.target = '_blank'; go.href = roomUrl(pick.room, pick.kind);
    }
    go.setAttribute('aria-disabled', n ? 'false' : 'true');""")

# alert logic
rep("""  function callCard(m, mine){""", r"""  // ---- attention alerts
  var BELL_SVG = '""" + BELL.replace("'", "\\'") + r"""';
  var roomNs = null, alarmOn = null, alarmTimer = null, titleTimer = null, BASE_TITLE = 'a.k.a. Media team board';
  $('alertBtn').addEventListener('click', function(e){ e.preventDefault(); openPicker('alert'); setTimeout(function(){ var n = $('alertNote'); if(n) n.focus(); }, 0); });
  function sendAlert(ids, note){
    var v = me(); if(!v) return;
    var alert = { id: uid('al'), to: ids.slice(), note: String(note || '').slice(0, 140) };
    var here = canSeeChannel(v, chatChan) && ids.every(function(id){ var p = person(id); return p && canSeeChannel(p, chatChan); });
    var now = Date.now(), chans = [];
    if(here){ chans.push(chatChan); change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: '', at: now, alert: alert } }); }
    else ids.forEach(function(id, i){ var ch = dmId(v.id, id); chans.push(ch); change({ type: 'msg', ch: ch, m: { id: uid('m'), by: v.id, text: '', at: now + i, alert: alert } }); });
    ls.set(heardKey(), String(now + ids.length));
    if(roomNs){ try { roomNs.emit('alert', { alert: alert, by: v.id, at: now, ch: chans[0] }).catch(function(){}); } catch(e){} }
    try { whoosh(); } catch(e){}
    closePicker(); renderChat();
  }
  function ackedBy(id, pid){ return !!(state.acks && state.acks[id] && state.acks[id][pid]); }
  function alertCard(m, mine){
    var a = m.alert || {}, box = document.createElement('div'); box.className = 'alertcard';
    var ci = document.createElement('span'); ci.className = 'ci'; ci.innerHTML = BELL_SVG;
    var t = document.createElement('div'); var b = document.createElement('b'); b.textContent = 'Attention alert';
    var names = (a.to || []).map(function(id){ var p = person(id); return p ? (me() && p.id === me().id ? 'you' : p.name) : null; }).filter(Boolean);
    var sm = document.createElement('small'); sm.textContent = 'To ' + names.join(', ');
    t.append(b, sm);
    var v = me();
    if(v && (mine || v.role === 'superuser')){
      var seen = (a.to || []).filter(function(id){ return ackedBy(a.id, id); }).map(function(id){ var p = person(id); return p ? p.name : '?'; });
      var waiting = (a.to || []).filter(function(id){ return !ackedBy(a.id, id); }).map(function(id){ var p = person(id); return p ? p.name : '?'; });
      var st = document.createElement('small');
      st.textContent = (seen.length ? 'Seen by ' + seen.join(', ') : '') + (seen.length && waiting.length ? ' · ' : '') + (waiting.length ? 'Waiting for ' + waiting.join(', ') : '');
      t.appendChild(st);
    }
    box.append(ci, t);
    if(a.note){ var n = document.createElement('p'); n.className = 'note'; n.textContent = a.note; box.appendChild(n); }
    return box;
  }
  function alarmTone(){
    var ac = ctx(); if(!ac) return false; var n = ac.currentTime + 0.02;
    [0, 0.18, 0.36].forEach(function(o){ tone(ac, 1046.5, n + o, 0.12, 0.2, 'square'); tone(ac, 1318.5, n + o + 0.06, 0.1, 0.12, 'square'); });
    return ac.state === 'running';
  }
  function soundLoop(){
    clearInterval(alarmTimer);
    var play = function(){ if(!alarmOn || !soundOn) return; try { alarmTone(); } catch(e){} };
    play(); alarmTimer = setInterval(play, 1300);
    // if the browser blocked sound, it starts on the first touch
    var unlock = function(){ document.removeEventListener('pointerdown', unlock, true); document.removeEventListener('keydown', unlock, true); play(); };
    document.addEventListener('pointerdown', unlock, true); document.addEventListener('keydown', unlock, true);
  }
  function stopSound(){ clearInterval(alarmTimer); alarmTimer = null; }
  function flashTitle(from){
    clearInterval(titleTimer); var on = false;
    titleTimer = setInterval(function(){ on = !on; document.title = on ? '!! ALERT from ' + from + ' !!' : '❗ ' + from + ' needs you'; }, 800);
  }
  function stopTitle(){ clearInterval(titleTimer); titleTimer = null; document.title = BASE_TITLE; renderTop(); }
  function raiseAlarm(a, byId, ch){
    var v = me(); if(!v || !a || (a.to || []).indexOf(v.id) < 0) return;
    if(ackedBy(a.id, v.id) || ls.get('alert-ack-' + a.id)) return;
    if(alarmOn && alarmOn.id === a.id) return;
    alarmOn = { id: a.id, ch: ch };
    var from = person(byId), nm = from ? from.name : 'Someone';
    var ov = $('alarmBox'); if(ov) ov.remove();
    ov = document.createElement('div'); ov.className = 'alarm'; ov.id = 'alarmBox'; ov.setAttribute('role', 'alertdialog'); ov.setAttribute('aria-modal', 'true');
    ov.innerHTML = '<div class="box ' + (from ? 'k' + (from.color % 7) : '') + '">' + (from ? avatarHtml(from) : '') + '<h2></h2><p class="msgtxt"></p><p class="sub"></p><button type="button" class="ack">I’m here</button></div>';
    ov.querySelector('h2').textContent = nm + ' needs your attention';
    var mt = ov.querySelector('.msgtxt'); if(a.note) mt.textContent = '“' + a.note + '”'; else mt.remove();
    ov.querySelector('.sub').textContent = 'Sent ' + chatTime(Date.now());
    ov.querySelector('.ack').addEventListener('click', function(){ ackAlarm(a.id, ch); });
    document.body.appendChild(ov);
    setTimeout(function(){ var b = ov.querySelector('.ack'); if(b) b.focus(); }, 50);
    soundLoop(); flashTitle(nm);
    if(!document.hidden && document.hasFocus()){ /* already looking: the sound keeps going until they answer */ }
  }
  function ackAlarm(id, ch){
    var v = me();
    ls.set('alert-ack-' + id, String(Date.now()));
    stopSound(); stopTitle(); alarmOn = null;
    var ov = $('alarmBox'); if(ov) ov.remove();
    if(v && mode !== 'readonly') change({ type: 'ack', id: id, pid: v.id, t: Date.now() });
    if(roomNs && v){ try { roomNs.emit('alert', { ack: id, by: v.id }).catch(function(){}); } catch(e){} }
    if(ch && canSeeChannel(v, ch)){ chatChan = ch; ss.set('chat-chan', ch); openChat(); }
  }
  // "until the tab is activated": coming back to the tab silences it; the card stays until answered
  var wasHidden = document.hidden;
  document.addEventListener('visibilitychange', function(){
    if(document.hidden){ wasHidden = true; return; }
    if(alarmOn && wasHidden){ stopSound(); stopTitle(); }
    wasHidden = false;
  });
  window.addEventListener('focus', function(){ if(alarmOn && wasHidden){ stopSound(); stopTitle(); } });
  function checkStoredAlerts(){
    var v = me(); if(!v) return;
    var best = null;
    channelsFor(v).forEach(function(c){ msgsIn(c.id).forEach(function(m){
      if(m.alert && m.by !== v.id && Date.now() - m.at < 30 * 60000 && (m.alert.to || []).indexOf(v.id) >= 0 && !ackedBy(m.alert.id, v.id) && !ls.get('alert-ack-' + m.alert.id)){
        if(!best || m.at > best.m.at) best = { m: m, ch: c.id };
      }
    }); });
    if(best) raiseAlarm(best.m.alert, best.m.by, best.ch);
  }
  if(window.claude && typeof window.claude.use === 'function'){
    window.claude.use('room').then(function(r){
      if(!r) return; roomNs = r;
      r.on('alert', function(msg){
        var d = msg && msg.data; if(!d || msg.sameTab) return;
        if(d.ack){ return; }
        if(d.alert && d.by) raiseAlarm(d.alert, String(d.by), d.ch ? String(d.ch) : null);
      }, function(){ roomNs = null; });
    }, function(){});
  }
  function callCard(m, mine){""")
rep("""      if(m.call) row.querySelector('.bubble').appendChild(callCard(m, mine));""",
    """      if(m.call) row.querySelector('.bubble').appendChild(callCard(m, mine));
      if(m.alert) row.querySelector('.bubble').appendChild(alertCard(m, mine));""")
rep("""  function msgPreview(m){ if(m.call)""", """  function msgPreview(m){ if(m.alert) return 'Attention alert' + (m.alert.note ? ': ' + m.alert.note : ''); if(m.call)""")
# alerts are handled by the alarm, not the normal toast/chime
rep("""    var calls = fresh.filter(function(f){ var c = f.m.call;""", """    fresh = fresh.filter(function(f){ return !f.m.alert; });
    if(!fresh.length) return;
    var calls = fresh.filter(function(f){ var c = f.m.call;""")
rep("""  setTimeout(function(){ announceNew(); announceReads(); }, 400);""", """  setTimeout(function(){ announceNew(); announceReads(); checkStoredAlerts(); }, 400);""")
# don't let title update overwrite flashing
rep("""    document.title = (unread ? '(' + unread + ') ' : '') + 'a.k.a. Media team board';""",
    """    if(!titleTimer) document.title = (unread ? '(' + unread + ') ' : '') + 'a.k.a. Media team board';""")
open(p,'w').write(s); print('ok')
