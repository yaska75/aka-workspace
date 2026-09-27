p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, (s.count(a), a[:80])
    s=s.replace(a,b)

rep(".mv{background:none;", """.files{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}
.file{display:inline-flex;align-items:center;gap:2px;max-width:100%;border:1px solid var(--line);border-radius:999px;background:var(--paper);font-size:13px}
.file a{display:inline-flex;align-items:center;gap:6px;padding:3px 4px 3px 10px;color:var(--ink);text-decoration:none;min-width:0}
.file a span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:220px}
.file a:hover span{text-decoration:underline}
.file svg{flex:none;color:var(--c)}
.file .x{background:none;border:0;color:var(--muted);padding:2px 8px 2px 4px;font-size:15px;line-height:1;border-radius:999px}
.file .x:hover{color:var(--strike)}
.attach{display:grid;grid-template-columns:1fr auto;gap:6px;margin-top:8px;padding:10px;border:1px dashed var(--c);border-radius:12px;background:var(--paper)}
.attach input{font:inherit;font-size:14px;color:var(--ink);border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:6px 9px;min-width:0}
.attach .url{grid-column:1/-1}
.attach .row{grid-column:1/-1;display:flex;gap:8px;align-items:center;justify-content:flex-end;flex-wrap:wrap}
.attach .row a{margin-right:auto;font-size:14px;color:var(--c)}
.attach .err{grid-column:1/-1;color:var(--strike);font-size:13px;margin:0}
.attach .primary{padding:6px 12px}
.readonly .file .x{display:none}
.mv{background:none;""")

# anyEditing covers the attach panel
rep("    return state.people.some(function(p){ var u = ui[p.id]; return u && (u.editingId || u.editingWhere); });",
    "    return state.people.some(function(p){ var u = ui[p.id]; return u && (u.editingId || u.editingWhere || u.attachId); });")

# file chips + attach panel under the task
rep("    body.appendChild(due);", """    body.appendChild(due);
    if(t.files && t.files.length){
      var fl = document.createElement('div'); fl.className = 'files';
      t.files.forEach(function(f){
        var chip = document.createElement('span'); chip.className = 'file';
        var a = document.createElement('a'); a.href = f.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
        a.title = f.url;
        a.innerHTML = isDrive(f.url)
          ? '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.2 3h7.6l6.2 10.7-3.8 6.6H5.8L2 13.7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.2 3l6 10.7H22M15.8 3l-9.9 17.3M2 13.7h12.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg><span></span>'
          : '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 005.7 0l3.5-3.5a4 4 0 00-5.7-5.7L12 6.3M14 10a4 4 0 00-5.7 0l-3.5 3.5a4 4 0 005.7 5.7l1.5-1.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg><span></span>';
        a.querySelector('span').textContent = f.name;
        chip.appendChild(a);
        var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.textContent = '\\u00d7';
        x.setAttribute('aria-label', 'Remove ' + f.name); x.title = 'Remove';
        x.addEventListener('click', function(){ if(mode === 'readonly') return; change({ type: 'fdel', pid: pid, id: t.id, fid: f.id }); renderCol(pid); });
        chip.appendChild(x);
        fl.appendChild(chip);
      });
      body.appendChild(fl);
    }
    if(u.attachId === t.id) body.appendChild(renderAttach(pid, t));""")

# Attach button in actions
rep("    var edit = document.createElement('button'); edit.className = 'icon'; edit.type = 'button';",
"""    var att = document.createElement('button'); att.className = 'icon'; att.type = 'button';
    att.textContent = 'Attach'; att.setAttribute('aria-label', 'Attach a file link to: ' + t.text);
    att.addEventListener('click', function(){ if(mode === 'readonly') return; u.attachId = u.attachId === t.id ? null : t.id; renderCol(pid); });
    actions.appendChild(att);
    var edit = document.createElement('button'); edit.className = 'icon'; edit.type = 'button';""")

# helpers for links (before task actions)
rep("  // ---------- reordering ----------", """  // ---------- file links (files live in Google Drive) ----------
  function isDrive(url){ return /^https:\\/\\/(drive|docs)\\.google\\.com\\//i.test(url); }
  function cleanUrl(v){
    v = (v || '').trim(); if(!v) return null;
    if(!/^https?:\\/\\//i.test(v)) v = 'https://' + v;
    try { var x = new URL(v); if(x.protocol !== 'https:' && x.protocol !== 'http:') return null; return x.href; } catch(e){ return null; }
  }
  function nameFor(url){
    if(isDrive(url)){
      if(/docs\\.google\\.com\\/document/i.test(url)) return 'Google Doc';
      if(/docs\\.google\\.com\\/spreadsheets/i.test(url)) return 'Google Sheet';
      if(/docs\\.google\\.com\\/presentation/i.test(url)) return 'Google Slides';
      if(/\\/folders\\//i.test(url)) return 'Drive folder';
      return 'Drive file';
    }
    try { return new URL(url).hostname.replace(/^www\\./, ''); } catch(e){ return 'Link'; }
  }
  function makeFile(url, name){ return { id: uid('f'), url: url, name: (name || '').trim() || nameFor(url), addedAt: Date.now(), addedBy: me() ? me().id : null }; }
  function renderAttach(pid, t){
    var u = ui[pid];
    var box = document.createElement('div'); box.className = 'attach';
    var url = document.createElement('input'); url.type = 'url'; url.className = 'url'; url.placeholder = 'Paste a Google Drive link'; url.setAttribute('aria-label', 'File link');
    var name = document.createElement('input'); name.type = 'text'; name.placeholder = 'Name (optional)'; name.setAttribute('aria-label', 'File name');
    var add = document.createElement('button'); add.type = 'button'; add.className = 'primary'; add.textContent = 'Add link';
    var err = document.createElement('p'); err.className = 'err'; err.hidden = true;
    var row = document.createElement('div'); row.className = 'row';
    var drive = document.createElement('a'); drive.href = 'https://drive.google.com/drive/my-drive'; drive.target = '_blank'; drive.rel = 'noopener noreferrer'; drive.textContent = 'Open Google Drive to upload';
    var cancel = document.createElement('button'); cancel.type = 'button'; cancel.className = 'link'; cancel.textContent = 'Close';
    row.append(drive, cancel);
    function commit(){
      var v = cleanUrl(url.value);
      if(!v){ err.textContent = 'Paste a full link, for example from Share, Copy link in Google Drive.'; err.hidden = false; url.focus(); return; }
      change({ type: 'fadd', pid: pid, id: t.id, file: makeFile(v, name.value) });
      u.attachId = null; renderCol(pid);
    }
    add.addEventListener('click', commit);
    cancel.addEventListener('click', function(){ u.attachId = null; renderCol(pid); if(pendingSave) scheduleSave(); });
    [url, name].forEach(function(el){ el.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){ e.preventDefault(); commit(); }
      if(e.key === 'Escape'){ e.preventDefault(); u.attachId = null; renderCol(pid); }
    }); });
    box.append(url, name, add, err, row);
    setTimeout(function(){ url.focus(); }, 0);
    return box;
  }

  // ---------- reordering ----------""")

# journal ops for files
rep("    if(o.type === 'reorder'){", """    if(o.type === 'fadd'){
      list.forEach(function(t){ if(t.id === o.id){ t.files = t.files || []; if(!t.files.some(function(f){ return f.id === o.file.id; })) t.files.push(JSON.parse(JSON.stringify(o.file))); } });
      return;
    }
    if(o.type === 'fdel'){
      list.forEach(function(t){ if(t.id === o.id && t.files) t.files = t.files.filter(function(f){ return f.id !== o.fid; }); });
      return;
    }
    if(o.type === 'reorder'){""")

# Send a task: optional link
rep("""        '<label class="wide">Task<input type="text" id="sendText" required autocomplete="off" placeholder="What needs doing?"></label>' +""",
"""        '<label class="wide">Task<input type="text" id="sendText" required autocomplete="off" placeholder="What needs doing?"></label>' +
        '<label class="wide">File link (optional)<input type="url" id="sendLink" autocomplete="off" placeholder="Paste a Google Drive link"></label>' +""")
rep("    change({ type: 'add', pid: to.id, task: { id: uid('t'), text: text, due: $('sendDue').value || todayStr(), done: false, createdAt: Date.now(), doneAt: null, addedBy: v.id } });",
"""    var link = $('sendLink').value.trim(), lk = link ? cleanUrl(link) : null;
    if(link && !lk){ $('sentNote').textContent = 'That link doesn\\u2019t look right. Paste the full Google Drive link.'; $('sendLink').focus(); return; }
    change({ type: 'add', pid: to.id, task: { id: uid('t'), text: text, due: $('sendDue').value || todayStr(), done: false, createdAt: Date.now(), doneAt: null, addedBy: v.id, files: lk ? [makeFile(lk, '')] : [] } });
    $('sendLink').value = '';""")
open(p,'w').write(s)
print('patched')
