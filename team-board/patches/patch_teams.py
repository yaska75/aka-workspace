p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    if s.count(a)!=1:
        a=a.replace('\\u2019','\u2019')
    assert s.count(a)==1, (s.count(a), a[:80])
    s=s.replace(a,b)

# ---- CSS additions
rep("#fx{position:fixed;", """.team-tag{display:inline-block;margin-top:6px;font-size:12px;color:var(--muted)}
.rules{margin:0 0 16px;padding:12px 14px;border-radius:12px;background:var(--paper);border:1px solid var(--line);font-size:14px;color:var(--muted)}
.rules b{color:var(--ink)}
.send{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.send label{display:grid;gap:4px;font-size:14px;color:var(--muted)}
.send .wide{grid-column:1/-1}
.send input,.send select{font:inherit;color:var(--ink);border:1px solid var(--line);background:var(--paper);border-radius:9px;padding:9px 10px;min-width:0}
.send .foot{grid-column:1/-1;display:flex;justify-content:flex-end;gap:8px;align-items:center;margin-top:4px}
.sent{color:var(--accent);font-weight:600;margin-right:auto}
.nocols{padding:40px 0;text-align:center;color:var(--muted)}
#fx{position:fixed;""")
rep(".fields{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;align-items:center}",
    ".fields{display:grid;grid-template-columns:1fr 1fr auto auto;gap:8px;align-items:center}")
rep(".addp{margin-top:18px;padding-top:18px;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr auto auto;gap:8px;align-items:center}",
    ".addp{margin-top:18px;padding-top:18px;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr auto auto auto;gap:8px;align-items:center}")
rep(".readonly .add,.readonly .actions,.readonly .clear,.readonly #teamBtn{display:none}",
    ".readonly .add,.readonly .actions,.readonly .clear,.readonly #teamBtn,.readonly #sendBtn{display:none}")

# ---- constants + clean
rep("  var ROLE_NAMES = { superuser: 'Superuser', admin: 'Admin', member: 'Member' };",
"""  var ROLE_NAMES = { superuser: 'Superuser', admin: 'Admin', member: 'Member' };
  var TEAM_NAMES = { management: 'Management', post: 'Post', finance: 'Finance' };""")
rep("      if(ROLE_NAMES[p.role] === undefined) p.role = 'member';",
"""      if(ROLE_NAMES[p.role] === undefined) p.role = 'member';
      if(TEAM_NAMES[p.team] === undefined) p.team = p.role === 'member' ? 'post' : 'management';""")

# ---- visibility rules
rep("  function avatarHtml(p){",
"""  // Who sees what (on screen only; see the note in the Team panel):
  // - the superuser sees every list and every task
  // - Management sees every list
  // - everyone sees their own list and their own team's lists
  // - Finance can send tasks to Management without seeing their lists
  // - tasks Finance sends to the superuser are visible only to the superuser
  function canSee(viewer, owner){
    if(!viewer || !owner) return false;
    if(viewer.id === owner.id || viewer.role === 'superuser') return true;
    if(viewer.team === 'management') return true;
    return viewer.team === owner.team;
  }
  function canAddTo(viewer, owner){
    if(canSee(viewer, owner)) return true;
    return !!viewer && !!owner && viewer.team === 'finance' && owner.team === 'management';
  }
  function taskVisible(viewer, owner, t){
    if(!viewer) return false;
    if(viewer.id === owner.id || viewer.role === 'superuser') return true;
    if(owner.role === 'superuser'){
      var from = t.addedBy ? person(t.addedBy) : null;
      if(from && from.team === 'finance') return false;
    }
    return true;
  }
  function visibleTasks(pid){
    var o = person(pid), v = me(); if(!o) return [];
    return o.tasks.filter(function(t){ return taskVisible(v, o, t); });
  }
  function visiblePeople(){
    var v = me(); if(!v) return [];
    var list = state.people.filter(function(p){ return canSee(v, p); });
    list.sort(function(a, b){ return (a.id === v.id ? -1 : 0) - (b.id === v.id ? -1 : 0); });
    return list;
  }
  function addablePeople(){
    var v = me(); if(!v) return [];
    return state.people.filter(function(p){ return canAddTo(v, p); });
  }
  function avatarHtml(p){""")

# ---- skeleton
rep("""          '<button class="pill" id="teamBtn" type="button" hidden>Manage team</button>' +""",
"""          '<button class="pill" id="sendBtn" type="button" hidden>Send a task</button>' +
          '<button class="pill" id="teamBtn" type="button" hidden>Manage team</button>' +""")
rep("""      '<h3 id="teamTitle">Team</h3><p class="note">Add people, set who is an admin, and update names, offices and photos. Everyone can add tasks to anyone\\u2019s list.</p>' +""",
"""      '<h3 id="teamTitle">Team</h3><p class="note">Add people, set their team and role, and update names, offices and photos.</p>' +
      '<div class="rules"><b>Who sees what.</b> Management sees every list. Everyone else sees their own list and their team\\u2019s lists. Finance can send tasks to Management, and tasks Finance sends to the superuser are only visible to the superuser. <b>This is hidden on screen only</b>, so keep sensitive details out of task text until the team moves to one Claude Team plan.</div>' +""")
rep("""        '<select id="apRole" aria-label="Role"><option value="member">Member</option><option value="admin">Admin</option></select>' +""",
"""        '<select id="apTeam" aria-label="Team"><option value="post">Post</option><option value="finance">Finance</option><option value="management">Management</option></select>' +
        '<select id="apRole" aria-label="Role"><option value="member">Member</option><option value="admin">Admin</option></select>' +""")
rep("""      '<div class="foot"><button class="primary" id="teamDone" type="button">Done</button></div>' +
    '</div></div>';""",
"""      '<div class="foot"><button class="primary" id="teamDone" type="button">Done</button></div>' +
    '</div></div>' +
    '<div class="overlay" id="sendOverlay" hidden><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="sendTitle">' +
      '<h3 id="sendTitle">Send a task</h3><p class="note">It goes straight onto their list, marked as from you.</p>' +
      '<form class="send" id="sendForm">' +
        '<label>To<select id="sendTo" required></select></label>' +
        '<label>To do date<input type="date" id="sendDue" required></label>' +
        '<label class="wide">Task<input type="text" id="sendText" required autocomplete="off" placeholder="What needs doing?"></label>' +
        '<div class="foot"><span class="sent" id="sentNote" role="status" aria-live="polite"></span><button class="link" type="button" id="sendCancel">Close</button><button class="primary" type="submit">Send task</button></div>' +
      '</form></div></div>';""")

rep("    if(teamOpen || whoOpen) return true;", "    if(teamOpen || whoOpen || sendOpen) return true;")
rep("  var teamOpen = false, whoOpen = false, colSig = '';", "  var teamOpen = false, whoOpen = false, sendOpen = false, colSig = '';")

rep("""  function sorted(pid){
    var all = tasksOf(pid);""", """  function sorted(pid){
    var all = visibleTasks(pid);""")

rep("  function signature(){ return state.people.map(function(p){ return [p.id, p.name, p.role, p.color, (p.photo || '').length].join('|'); }).join('/') + '#' + (ls.get(ME_KEY) || ''); }",
    "  function signature(){ return visiblePeople().map(function(p){ return [p.id, p.name, p.role, p.team, p.color, (p.photo || '').length].join('|'); }).join('/') + '#' + (ls.get(ME_KEY) || ''); }")
rep("""    var mine = ls.get(ME_KEY);
    state.people.forEach(function(p){""", """    var mine = ls.get(ME_KEY);
    var shown = visiblePeople();
    if(!shown.length && me()){ cols.innerHTML = '<p class="nocols">No lists to show.</p>'; }
    shown.forEach(function(p){""")
rep("""          '<div class="hero-text"><h2></h2><div class="whereBox"></div></div></div>' +""",
    """          '<div class="hero-text"><h2></h2><div class="whereBox"></div><span class="team-tag"></span></div></div>' +""")
rep("      sec.querySelector('.tabs').setAttribute('aria-label', 'Show ' + p.name + '\\u2019s tasks');",
    "      sec.querySelector('.tabs').setAttribute('aria-label', 'Show ' + p.name + '\\u2019s tasks');\n      sec.querySelector('.team-tag').textContent = TEAM_NAMES[p.team] + ' team';")
rep("""      var ids = tasksOf(pid).filter(function(t){ return t.done; }).map(function(t){ return t.id; });""",
    """      var ids = visibleTasks(pid).filter(function(t){ return t.done; }).map(function(t){ return t.id; });""")

rep("""    buildColumns();
    state.people.forEach(function(p){ renderCol(p.id); });
    renderTop();""", """    buildColumns();
    visiblePeople().forEach(function(p){ renderCol(p.id); });
    renderTop();""")
rep("    $('teamBtn').hidden = !canManageTeam();",
    "    $('teamBtn').hidden = !canManageTeam();\n    $('sendBtn').hidden = mode === 'readonly' || !m || !addablePeople().length;")
rep("""    var col = u.col, all = p.tasks;
    renderWhere(pid);""", """    var col = u.col, all = visibleTasks(pid);
    renderWhere(pid);""")
rep("""    var all = tasksOf(pid);
    var allDone = t.done && all.every(function(x){ return x.done; });""",
"""    var all = visibleTasks(pid);
    var allDone = t.done && all.every(function(x){ return x.done; });""")

rep("""      f.append(name, loc);
      if(canChangeRole(p)){""", """      f.append(name, loc);
      if(canManageTeam() && (p.role !== 'superuser' || (me() && me().role === 'superuser'))){
        var tsel = document.createElement('select'); tsel.setAttribute('aria-label', 'Team for ' + p.name);
        tsel.innerHTML = '<option value="management">Management</option><option value="post">Post</option><option value="finance">Finance</option>';
        tsel.value = p.team;
        tsel.addEventListener('change', function(){ change({ type: 'pset', pid: p.id, fields: { team: tsel.value } }); renderTeam(); });
        f.appendChild(tsel);
      } else {
        var tf = document.createElement('span'); tf.className = 'fixed'; tf.textContent = TEAM_NAMES[p.team]; f.appendChild(tf);
      }
      if(canChangeRole(p)){""")
rep("change({ type: 'padd', person: { id: uid('p'), name: n, role: $('apRole').value, location: $('apLoc').value.trim() || 'Dubai', color: color, photo: '', tasks: [] } });",
    "change({ type: 'padd', person: { id: uid('p'), name: n, role: $('apRole').value, team: $('apTeam').value, location: $('apLoc').value.trim() || 'Dubai', color: color, photo: '', tasks: [] } });")
rep("    $('apName').value = ''; $('apLoc').value = ''; $('apRole').value = 'member';",
    "    $('apName').value = ''; $('apLoc').value = ''; $('apRole').value = 'member'; $('apTeam').value = 'post';")

rep("  // ---------- sound ----------", """  // ---------- send a task ----------
  function openSend(){
    var v = me(); if(!v || mode === 'readonly') return;
    var sel = $('sendTo'); sel.textContent = '';
    addablePeople().forEach(function(p){
      var o = document.createElement('option'); o.value = p.id; o.textContent = p.id === v.id ? p.name + ' (me)' : p.name; sel.appendChild(o);
    });
    var firstOther = addablePeople().filter(function(p){ return p.id !== v.id; })[0];
    if(firstOther) sel.value = firstOther.id;
    $('sendDue').value = todayStr(); $('sentNote').textContent = '';
    sendOpen = true; $('sendOverlay').hidden = false; $('sendText').focus();
  }
  function closeSend(){ sendOpen = false; $('sendOverlay').hidden = true; render(); if(pendingSave) scheduleSave(); }
  $('sendBtn').addEventListener('click', openSend);
  $('sendCancel').addEventListener('click', closeSend);
  $('sendForm').addEventListener('submit', function(e){
    e.preventDefault();
    var v = me(), to = person($('sendTo').value), text = $('sendText').value.trim();
    if(!v || !to || !text || !canAddTo(v, to)){ $('sendText').focus(); return; }
    change({ type: 'add', pid: to.id, task: { id: uid('t'), text: text, due: $('sendDue').value || todayStr(), done: false, createdAt: Date.now(), doneAt: null, addedBy: v.id } });
    $('sendText').value = ''; $('sentNote').textContent = 'Sent to ' + to.name;
    $('sendText').focus();
  });

  // ---------- sound ----------""")
rep("""    if(teamOpen) closeTeam();
    else if(whoOpen && me()) closeWho();""", """    if(teamOpen) closeTeam();
    else if(sendOpen) closeSend();
    else if(whoOpen && me()) closeWho();""")
rep("        if(teamOpen){ teamOpen = false; $('teamOverlay').hidden = true; }",
    "        if(teamOpen){ teamOpen = false; $('teamOverlay').hidden = true; }\n        if(sendOpen){ sendOpen = false; $('sendOverlay').hidden = true; }")
open(p,'w').write(s)
print('patched')
