p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

rep(".composer{display:grid;grid-template-columns:1fr auto;gap:8px;",".composer{display:grid;grid-template-columns:auto 1fr auto;gap:8px;")
rep(".composer .primary{--c:var(--accent);align-self:end}", """.composer .primary{--c:var(--accent);align-self:end}
.composer .clip{align-self:end;width:42px;height:42px;display:grid;place-items:center;border:1px solid var(--line);background:var(--paper);color:var(--muted);border-radius:12px;padding:0}
.composer .clip:hover,.composer .clip[aria-expanded=true]{color:var(--accent);border-color:var(--accent)}
.cattach{grid-column:1/-1;display:grid;grid-template-columns:1fr auto;gap:6px;padding:10px;border:1px dashed var(--accent);border-radius:12px;background:var(--paper)}
.cattach input{font:inherit;font-size:14px;color:var(--ink);border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:6px 9px;min-width:0}
.cattach .url{grid-column:1/-1}
.cattach .row{grid-column:1/-1;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.cattach .row a{font-size:13px;color:var(--accent)}
.cattach .row button{margin-left:auto}
.cattach .err{grid-column:1/-1;margin:0;color:var(--strike);font-size:13px}
.cattach .primary{padding:6px 12px}
.pending{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:6px}
.bubble .files{margin-top:6px}
.bubble .file{background:var(--paper);border-color:var(--line)}
.msg.mine .bubble .file,.msg.mine .bubble .file a{background:var(--surface);color:var(--ink)}
.msg.mine .bubble .file svg{color:var(--accent)}""")

rep("""'<form class="composer" id="composer"><textarea id="chatText\"""",
    """'<form class="composer" id="composer"><div class="pending" id="pendingFiles" hidden></div><div class="cattach" id="cAttach" hidden></div><button class="clip" type="button" id="clipBtn" aria-label="Share a file" aria-expanded="false" title="Share a file from Google Drive"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.5l-8.2 8.2a5.3 5.3 0 01-7.5-7.5l8.6-8.6a3.5 3.5 0 015 5l-8.6 8.6a1.8 1.8 0 01-2.5-2.5l7.9-7.9" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg></button><textarea id="chatText\"""")

rep("""  function sendChat(){
    var v = me(), ta = $('chatText'), text = ta.value.trim();
    if(!v || !text || mode === 'readonly' || !canSeeChannel(v, chatChan)) return;
    change({ type: 'msg', ch: chatChan, m: { id: uid('m'), by: v.id, text: text.slice(0, 4000), at: Date.now() } });""",
r"""  // ---- files in chat (stored in Google Drive, shared as links)
  var DRIVE_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.2 3h7.6l6.2 10.7-3.8 6.6H5.8L2 13.7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.2 3l6 10.7H22M15.8 3l-9.9 17.3M2 13.7h12.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
  var LINK_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 005.7 0l3.5-3.5a4 4 0 00-5.7-5.7L12 6.3M14 10a4 4 0 00-5.7 0l-3.5 3.5a4 4 0 005.7 5.7l1.5-1.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>';
  function fileChip(f, onRemove){
    var chip = document.createElement('span'); chip.className = 'file';
    var a = document.createElement('a'); a.href = f.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.title = f.url;
    a.innerHTML = (isDrive(f.url) ? DRIVE_SVG : LINK_SVG) + '<span></span>'; a.querySelector('span').textContent = f.name;
    chip.appendChild(a);
    if(onRemove){
      var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.textContent = '×';
      x.setAttribute('aria-label', 'Remove ' + f.name); x.addEventListener('click', onRemove); chip.appendChild(x);
    }
    return chip;
  }
  var pendingFiles = [];
  try { pendingFiles = JSON.parse(ss.get('chat-files') || '[]') || []; } catch(e){ pendingFiles = []; }
  function savePending(){ if(pendingFiles.length) ss.set('chat-files', JSON.stringify(pendingFiles)); else ss.del('chat-files'); }
  function renderPending(){
    var box = $('pendingFiles'); box.textContent = '';
    pendingFiles.forEach(function(f, i){ box.appendChild(fileChip(f, function(){ pendingFiles.splice(i, 1); savePending(); renderPending(); })); });
    box.hidden = !pendingFiles.length;
  }
  function closeCAttach(){ $('cAttach').hidden = true; $('cAttach').textContent = ''; $('clipBtn').setAttribute('aria-expanded', 'false'); }
  function openCAttach(){
    var box = $('cAttach'); box.textContent = ''; box.hidden = false; $('clipBtn').setAttribute('aria-expanded', 'true');
    var url = document.createElement('input'); url.type = 'text'; url.inputMode = 'url'; url.className = 'url'; url.placeholder = 'Paste a Google Drive link'; url.setAttribute('aria-label', 'File link');
    var name = document.createElement('input'); name.type = 'text'; name.placeholder = 'Name (optional)'; name.setAttribute('aria-label', 'File name');
    var add = document.createElement('button'); add.type = 'button'; add.className = 'primary'; add.textContent = 'Attach';
    var err = document.createElement('p'); err.className = 'err'; err.hidden = true;
    var row = document.createElement('div'); row.className = 'row';
    var drive = document.createElement('a'); drive.href = 'https://drive.google.com/drive/my-drive'; drive.target = '_blank'; drive.rel = 'noopener noreferrer'; drive.textContent = 'Open Google Drive to upload';
    var cancel = document.createElement('button'); cancel.type = 'button'; cancel.className = 'link'; cancel.textContent = 'Close';
    cancel.addEventListener('click', function(){ closeCAttach(); $('chatText').focus(); });
    row.append(drive, cancel);
    function commit(){
      var v = cleanUrl(url.value);
      if(!v){ err.textContent = 'Paste a full link. In Google Drive use Share, then Copy link.'; err.hidden = false; url.focus(); return; }
      if(pendingFiles.length >= 6){ err.textContent = 'Up to 6 files per message.'; err.hidden = false; return; }
      pendingFiles.push(makeFile(v, name.value)); savePending(); renderPending();
      closeCAttach(); $('chatText').focus();
    }
    add.addEventListener('click', commit);
    [url, name].forEach(function(el){ el.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){ e.preventDefault(); commit(); }
      if(e.key === 'Escape'){ e.preventDefault(); closeCAttach(); $('chatText').focus(); }
    }); });
    box.append(url, name, add, err, row);
    setTimeout(function(){ url.focus(); }, 0);
  }
  $('clipBtn').addEventListener('click', function(){ if(mode === 'readonly') return; $('cAttach').hidden ? openCAttach() : closeCAttach(); });
  renderPending();
  function msgPreview(m){ return m.text || (m.files && m.files.length ? 'Shared ' + (m.files.length === 1 ? 'a file: ' + m.files[0].name : m.files.length + ' files') : ''); }

  function sendChat(){
    var v = me(), ta = $('chatText'), text = ta.value.trim();
    if(!v || (!text && !pendingFiles.length) || mode === 'readonly' || !canSeeChannel(v, chatChan)) return;
    var msg = { id: uid('m'), by: v.id, text: text.slice(0, 4000), at: Date.now() };
    if(pendingFiles.length) msg.files = pendingFiles.slice(0, 6);
    change({ type: 'msg', ch: chatChan, m: msg });
    pendingFiles = []; savePending(); renderPending(); closeCAttach();""")

rep("""      linkify(row.querySelector('p'), m.text);""", """      linkify(row.querySelector('p'), m.text || '');
      if(!m.text) row.querySelector('p').hidden = true;
      if(m.files && m.files.length){
        var fl = document.createElement('div'); fl.className = 'files';
        m.files.forEach(function(f){ fl.appendChild(fileChip(f)); });
        row.querySelector('.bubble').appendChild(fl);
      }""")
# toasts use preview
rep("""title: (from ? from.name : 'Someone') + (peer ? '' : ' in ' + chanName(f.ch, v)), text: f.m.text, ch: f.ch });""",
    """title: (from ? from.name : 'Someone') + (peer ? '' : ' in ' + chanName(f.ch, v)), text: msgPreview(f.m), ch: f.ch });""")
rep("""read your message' + (peer ? '' : ' in ' + chanName(n.ch, v)), text: n.m.text, ch: n.ch });""",
    """read your message' + (peer ? '' : ' in ' + chanName(n.ch, v)), text: msgPreview(n.m), ch: n.ch });""")
open(p,'w').write(s); print('ok')
