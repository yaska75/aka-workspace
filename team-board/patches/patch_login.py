import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'team.html')
s = open(p).read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:70])
    s = s.replace(a, b)

# ---- CSS ----
rep(".overlay[hidden]{display:none}", """.overlay[hidden]{display:none}
.overlay.lock{background:var(--paper);z-index:60}
.overlay.lock .sheet{width:min(560px,100%);box-shadow:0 30px 80px rgba(0,0,0,.18)}
.lg-brand{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.lg-brand .logo{width:96px}
.lg-brand span{font:600 13px/1.2 "Outfit",sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.lg-back{border:0;background:none;color:var(--muted);padding:0;margin:0 0 14px;font:inherit;cursor:pointer}
.lg-back:hover{color:var(--ink)}
.lg-who{display:flex;align-items:center;gap:12px;margin:0 0 16px}
.lg-who .photo{width:52px;height:52px}
.lg-who b{font:600 20px/1.2 "Outfit",sans-serif}
.lg-form{display:grid;gap:10px}
.lg-form label{font-size:13px;color:var(--muted)}
.lg-form input{font:inherit;font-size:16px;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:var(--paper);color:var(--ink);width:100%;box-sizing:border-box}
.lg-form input:focus{outline:2px solid var(--accent,#e0103a);outline-offset:1px}
.lg-show{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted);margin-top:-2px}
.lg-form .go{margin-top:6px;border:0;border-radius:12px;padding:13px 16px;font:600 16px/1 "Outfit",sans-serif;background:var(--ink);color:var(--paper);cursor:pointer}
.lg-form .go:disabled{opacity:.5;cursor:default}
.lg-err{color:#d0103a;font-size:14px;min-height:1.2em;margin:0}
.lg-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.lg-acts button{border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:10px 16px;font:500 15px/1 "Instrument Sans",sans-serif;cursor:pointer}
.lg-acts button.out{border-color:#d0103a;color:#d0103a}
.pwcell{display:flex;align-items:center;gap:6px}
.pwcell input{font-family:ui-monospace,monospace;letter-spacing:.02em}
.pweye{border:1px solid var(--line);background:var(--paper);color:var(--muted);border-radius:8px;width:34px;height:34px;flex:none;cursor:pointer;font-size:15px}""")

# ---- markup: who overlay becomes a generic sign-in sheet ----
rep("""'<h3 id="whoTitle">Who are you?</h3><p class="note">Pick your name so the list knows who added what. It’s remembered on this device.</p>' +
      '<div class="who" id="whoList"></div></div></div>' +""",
"""'<div class="lg-brand"><span class="logo" role="img" aria-label="a.k.a. Media"></span><span>Team board</span></div>' +
      '<div id="whoBody"></div></div></div>' +""")

# ---- state: keys collection ----
rep("    if(!s.acks || typeof s.acks !== 'object' || Array.isArray(s.acks)) s.acks = {};",
    "    if(!s.acks || typeof s.acks !== 'object' || Array.isArray(s.acks)) s.acks = {};\n    if(!s.keys || typeof s.keys !== 'object' || Array.isArray(s.keys)) s.keys = {};")
rep("function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {}, r: st.reads || {}, a: st.acks || {} }); }",
    "function content(st){ return JSON.stringify({ p: st.people, c: st.chat || {}, r: st.reads || {}, a: st.acks || {}, k: st.keys || {} }); }")
rep("    if(o.type === 'mdel'){",
    """    if(o.type === 'pwset'){
      st.keys = st.keys || {};
      var cur = st.keys[o.pid];
      if(!cur || o.at >= cur.at) st.keys[o.pid] = { pw: String(o.pw), at: o.at };
      return;
    }
    if(o.type === 'mdel'){""")

# ---- identity: authed() replaces raw ls lookups ----
rep("  var ME_KEY = 'team-todo-me';", "  var ME_KEY = 'team-todo-me';\n  var AUTH_KEY = 'team-todo-auth';")
rep("  function me(){ return person(ls.get(ME_KEY)); }",
"""  function authed(){
    var a; try { a = JSON.parse(ls.get(AUTH_KEY) || 'null'); } catch(e){ a = null; }
    if(!a || !a.pid) return null;
    var k = state.keys && state.keys[a.pid];
    return (k && k.pw === a.pw) ? a.pid : null;
  }
  function me(){ return person(authed()); }
  function myId(){ var m = me(); return m ? m.id : null; }""")
s = s.replace("ls.get(ME_KEY)", "myId()")

# ---- password visibility permission ----
rep("  function isAdmin(p){ return !!p && (p.role === 'admin' || p.role === 'superuser'); }",
    """  function isAdmin(p){ return !!p && (p.role === 'admin' || p.role === 'superuser'); }
  function canSeePw(target){
    var m = me(); if(!isAdmin(m)) return false;
    if(m.role === 'superuser') return true;
    return target.role === 'member';
  }""")

# ---- who/openWho block: replace name-picker with sign-in screens ----
old_start = s.index("  // ---------- who are you ----------")
old_end = s.index("  $('meBtn').addEventListener('click', openWho);")
new = r"""  // ---------- sign in ----------
  var FAIL_KEY = 'team-todo-fails';
  function lockLeft(){ var f; try { f = JSON.parse(ls.get(FAIL_KEY) || '{}'); } catch(e){ f = {}; } return f.until && f.until > Date.now() ? Math.ceil((f.until - Date.now()) / 1000) : 0; }
  function noteFail(){ var f; try { f = JSON.parse(ls.get(FAIL_KEY) || '{}'); } catch(e){ f = {}; } f.n = (f.n || 0) + 1; if(f.n >= 5){ f.until = Date.now() + 30000; f.n = 0; } ls.set(FAIL_KEY, JSON.stringify(f)); }
  function signIn(pid, pw){ ls.set(AUTH_KEY, JSON.stringify({ pid: pid, pw: pw })); ls.set(ME_KEY, pid); ls.del(FAIL_KEY); }
  function signOut(){ ls.del(AUTH_KEY); ls.del(ME_KEY); openWho(); render(); }
  function whoSheet(html){ var b = $('whoBody'); b.innerHTML = html; return b; }
  function pwToggle(input, btn){ btn.addEventListener('click', function(){ var show = input.type === 'password'; input.type = show ? 'text' : 'password'; btn.textContent = show ? '🙈' : '👁️'; btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password'); }); }
  function openWho(){
    whoOpen = true;
    var m = me(), ov = $('whoOverlay');
    ov.classList.toggle('lock', !m);
    document.body.classList.toggle('signed-out', !m);
    if(m) showAccount(m); else showNames();
    ov.hidden = false;
  }
  function showNames(){
    var b = whoSheet('<h3 id="whoTitle">Sign in</h3><p class="note">Choose your name, then enter your password.</p><div class="who" id="whoList"></div>');
    var list = b.querySelector('#whoList');
    state.people.forEach(function(p){
      var bt = document.createElement('button'); bt.type = 'button'; bt.className = 'k' + (p.color % 7);
      bt.innerHTML = avatarHtml(p) + '<span></span>';
      bt.querySelector('span').textContent = p.name;
      bt.addEventListener('click', function(){ showPassword(p); });
      list.appendChild(bt);
    });
    var first = list.querySelector('button'); if(first) first.focus();
  }
  function showPassword(p){
    var has = !!(state.keys && state.keys[p.id]);
    var b = whoSheet('<button type="button" class="lg-back">← Not you</button>' +
      '<div class="lg-who k' + (p.color % 7) + '">' + avatarHtml(p) + '<div><b></b><p class="note" style="margin:2px 0 0"></p></div></div>' +
      '<h3 id="whoTitle"></h3>' +
      '<form class="lg-form" novalidate>' +
        '<label for="lgPw"></label><div class="pwcell"><input type="password" id="lgPw" autocomplete="' + (has ? 'current-password' : 'new-password') + '" required><button type="button" class="pweye" aria-label="Show password">👁️</button></div>' +
        (has ? '' : '<label for="lgPw2">Type it again</label><input type="password" id="lgPw2" autocomplete="new-password" required>') +
        '<p class="lg-err" id="lgErr" role="alert"></p><button type="submit" class="go"></button></form>');
    b.querySelector('.lg-who b').textContent = p.name;
    b.querySelector('.lg-who .note').textContent = (TEAM_NAMES[p.team] || '') + ' · ' + (p.location || '');
    b.querySelector('#whoTitle').textContent = has ? 'Enter your password' : 'Create your password';
    b.querySelector('label[for="lgPw"]').textContent = has ? 'Password' : 'New password (at least 4 characters)';
    var go = b.querySelector('.go'); go.textContent = has ? 'Sign in' : 'Create and sign in';
    b.querySelector('.lg-back').addEventListener('click', showNames);
    var pw = b.querySelector('#lgPw'), err = b.querySelector('#lgErr'); pw.focus();
    pwToggle(pw, b.querySelector('.pweye'));
    b.querySelector('form').addEventListener('submit', function(e){
      e.preventDefault(); err.textContent = '';
      var v = pw.value;
      if(has){
        var wait = lockLeft(); if(wait){ err.textContent = 'Too many tries. Wait ' + wait + ' seconds.'; return; }
        if(!v){ err.textContent = 'Enter your password.'; return; }
        if(v === state.keys[p.id].pw){ signIn(p.id, v); closeWho(); }
        else { noteFail(); err.textContent = 'That password isn’t right. Ask Yasser if you’ve forgotten it.'; pw.select(); }
      } else {
        var v2 = b.querySelector('#lgPw2').value;
        if(v.length < 4){ err.textContent = 'Use at least 4 characters.'; pw.focus(); return; }
        if(v !== v2){ err.textContent = 'The two passwords don’t match.'; b.querySelector('#lgPw2').select(); return; }
        if(mode === 'readonly'){ err.textContent = 'This copy is read-only, so a password can’t be saved here.'; return; }
        change({ type: 'pwset', pid: p.id, pw: v, at: Date.now() });
        signIn(p.id, v); closeWho();
      }
    });
  }
  function showAccount(m){
    var b = whoSheet('<div class="lg-who k' + (m.color % 7) + '">' + avatarHtml(m) + '<div><b></b><p class="note" style="margin:2px 0 0">Signed in on this device</p></div></div>' +
      '<div class="lg-acts"><button type="button" class="chg">Change my password</button><button type="button" class="out">Sign out</button><button type="button" class="cls">Close</button></div>');
    b.querySelector('.lg-who b').textContent = m.name;
    b.querySelector('.out').addEventListener('click', signOut);
    b.querySelector('.cls').addEventListener('click', closeWho);
    b.querySelector('.chg').addEventListener('click', function(){ showChange(m); });
    b.querySelector('.chg').focus();
  }
  function showChange(m){
    var b = whoSheet('<button type="button" class="lg-back">← Back</button><h3 id="whoTitle">Change my password</h3>' +
      '<form class="lg-form" novalidate><label for="cpNew">New password (at least 4 characters)</label><input type="password" id="cpNew" autocomplete="new-password">' +
      '<label for="cpNew2">Type it again</label><input type="password" id="cpNew2" autocomplete="new-password">' +
      '<p class="lg-err" role="alert"></p><button type="submit" class="go">Save new password</button></form>');
    b.querySelector('.lg-back').addEventListener('click', function(){ showAccount(m); });
    var err = b.querySelector('.lg-err');
    b.querySelector('#cpNew').focus();
    b.querySelector('form').addEventListener('submit', function(e){
      e.preventDefault(); err.textContent = '';
      var n = b.querySelector('#cpNew').value, n2 = b.querySelector('#cpNew2').value;
      if(n.length < 4){ err.textContent = 'Use at least 4 characters.'; return; }
      if(n !== n2){ err.textContent = 'The two don’t match.'; return; }
      change({ type: 'pwset', pid: m.id, pw: n, at: Date.now() });
      signIn(m.id, n); showAccount(m);
      var nt = $('whoBody').querySelector('.lg-who .note'); if(nt) nt.textContent = 'Password changed';
    });
  }
  function closeWho(){
    if(!me()) return;
    whoOpen = false; $('whoOverlay').hidden = true; $('whoOverlay').classList.remove('lock'); document.body.classList.remove('signed-out');
    colSig = ''; render(); if(pendingSave) scheduleSave();
  }
  function guardAuth(){ if(!me() && !whoOpen) openWho(); }
"""
s = s[:old_start] + new + s[old_end:]

# render() should re-lock if a device's stored auth stops matching (password changed elsewhere)
rep("""  function render(){
    document.body.classList.toggle('readonly', mode === 'readonly');""",
"""  function render(){
    document.body.classList.toggle('readonly', mode === 'readonly');
    if(typeof guardAuth === 'function') setTimeout(guardAuth, 0);""")

# ---- Team panel: visible, editable password per person (permission-gated) ----
rep("      var row = document.createElement('div'); row.className = 'trow k' + (p.color % 7);\n",
    "      var row = document.createElement('div'); row.className = 'trow k' + (p.color % 7); row.dataset.pid = p.id;\n")
rep("      f.append(name, loc);\n",
"""      f.append(name, loc);
      if(canSeePw(p)){
        var pwWrap = document.createElement('div'); pwWrap.className = 'pwcell';
        var pwIn = document.createElement('input'); pwIn.type = 'password'; pwIn.setAttribute('aria-label', 'Password for ' + p.name);
        pwIn.placeholder = (state.keys && state.keys[p.id]) ? '' : 'Not set yet';
        pwIn.value = (state.keys && state.keys[p.id]) ? state.keys[p.id].pw : '';
        pwIn.addEventListener('change', function(){
          var v = pwIn.value.trim();
          if(!v){ pwIn.value = (state.keys && state.keys[p.id]) ? state.keys[p.id].pw : ''; return; }
          if(v.length < 4){ pwIn.value = (state.keys && state.keys[p.id]) ? state.keys[p.id].pw : ''; return; }
          change({ type: 'pwset', pid: p.id, pw: v, at: Date.now() });
        });
        var eye = document.createElement('button'); eye.type = 'button'; eye.className = 'pweye'; eye.textContent = '👁️'; eye.setAttribute('aria-label', 'Show password');
        pwToggle(pwIn, eye);
        pwWrap.append(pwIn, eye); f.appendChild(pwWrap);
      }
""")

open(p, 'w').write(s)
print('ok')
