import os,re
os.chdir('/tmp/claude-0/-home-claude/f551496a-6099-53c0-bb40-c24e871c007b/scratchpad')
p='cc/src.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
TODO_IC='<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 12.5l2.6 2.6L16 9.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rep('  <nav class="dock" id="dock" aria-label="Sections">\n', '  <nav class="dock" id="dock" aria-label="Sections">\n    <button type="button" class="dk" data-sec="todo" aria-pressed="false"><span class="ic">'+TODO_IC+'</span><b>To do</b><span class="n" hidden></span></button>\n')
rep('.dock{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}','.dock{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}')
rep('  <div class="blank" id="blank"><p>Choose a section to open.</p></div>\n', '''  <div class="blank" id="blank"><p>Choose a section to open.</p></div>
  <section class="sec" data-sec="todo" hidden aria-label="To do">
    <div class="sh"><h2>To do</h2><a class="sr" href="https://claude.ai/artifact/8GwGDwq8AAmCDmQAqEZjif" target="_blank" rel="noopener noreferrer" style="text-decoration:none;color:inherit">Open team board ↗</a><button type="button" class="sc" aria-label="Close To do">×</button></div>
    <div class="canvas" id="cv-todo"></div>
    <p class="sempty" id="se-todo" hidden></p>
  </section>
''')
rep("  var SECS = ['email', 'calendar', 'team', 'social', 'claude'];", "  var SECS = ['todo', 'email', 'calendar', 'team', 'social', 'claude'];")
rep("  function secOf(c){ var s0 = String(c.source || '').toLowerCase(); if(", "  function secOf(c){ var s0 = String(c.source || '').toLowerCase(); if(s0 === 'todo') return 'todo'; if(")
rep("  var SEC_EMPTY = { email:", "  var SEC_EMPTY = { todo: 'Your tasks from the team board appear here within the hour.', email:")
rep(".badge.gmail{", ".badge.todo{color:var(--ink)}\n.badge.gmail{")
rep("bd.className = 'badge ' + (['outlook','gmail','calendar','teams','claude'].indexOf(src) >= 0 ? src : 'claude');",
    "bd.className = 'badge ' + (['outlook','gmail','calendar','teams','claude','todo','social'].indexOf(src) >= 0 ? src : 'claude'); if(src === 'todo') bd.textContent = 'team board';")
# promos buttons
rep("""          if(acts.children.length) li.appendChild(acts);""", """          if(secOf(c) === 'email' && !it.queued){
            var pm = document.createElement('button'); pm.type = 'button'; pm.className = 'mini';
            var gm = it.mailbox === 'gmail' || (!!it.threadId && !it.uri);
            pm.textContent = 'To Promotions'; pm.title = gm ? 'Move this Gmail thread to the Promotions tab' : 'Move this email to Other in Outlook at the next hourly sync';
            pm.addEventListener('click', function(){ toPromos(c, it, gm, pm); });
            acts.appendChild(pm);
          }
          if(it.queued){ var qn = document.createElement('small'); qn.className = 'qn'; qn.textContent = it.queued === 'failed' ? 'Couldn\\u2019t move to Other. Try again or move it in Outlook.' : 'Moving to Other in Outlook at the next sync'; acts.appendChild(qn); }
          if(acts.children.length) li.appendChild(acts);""")
rep(".sempty{margin:0;", ".qn{font-size:12px;color:var(--muted);align-self:center}\n.sempty{margin:0;")
rep("""  // ---- human reply writer""", r"""  // ---- send an email to Promotions (Gmail now, Outlook work inbox at the next desktop sync)
  function dropItem(c, it, patch){
    var items = (c.items || []).map(function(x){ return x === it ? (patch ? Object.assign({}, x, patch) : null) : x; }).filter(Boolean);
    var nc = Object.assign({}, c, { items: items }); return saveCard(nc);
  }
  function toPromos(c, it, gmail, btn){
    btn.disabled = true; btn.textContent = 'Moving…';
    if(gmail){
      if(!mcp || !it.threadId){ btn.textContent = 'Not available here'; return; }
      mcp.callTool('Gmail', 'label_thread', { threadId: String(it.threadId), labelIds: ['CATEGORY_PROMOTIONS'] }).then(function(){
        return mcp.callTool('Gmail', 'unlabel_thread', { threadId: String(it.threadId), labelIds: ['CATEGORY_PERSONAL'] }).catch(function(){});
      }).then(function(){ markPill('gPill', true); dropItem(c, it); }, function(e){ btn.disabled = false; btn.textContent = 'To Promotions'; var n = document.createElement('small'); n.className = 'qn'; n.textContent = m365Copy(e).replace(/Microsoft 365/g, 'Gmail'); btn.parentNode.appendChild(n); });
      return;
    }
    var job = { type: 'outlook-move-other', mailbox: 'yasser@akamedia.ae', title: it.title || '', subtitle: it.subtitle || '', when: it.when || '', status: 'pending', at: new Date().toISOString() };
    var done = function(){ dropItem(c, it, { queued: 'pending' }); };
    if(db && !memOnly){ db.collection('actions').add(job).then(done, function(){ btn.disabled = false; btn.textContent = 'To Promotions'; }); }
    else { btn.textContent = 'Needs the saved workspace'; }
  }

  // ---- human reply writer""")
open(p,'w').write(s)
s=s.replace('LOGO_L',open('logo_light.txt').read()).replace('LOGO_D',open('logo_dark.txt').read())
open('cc/command-centre.html','w').write(s)
open('cc/a.js','w').write(re.search(r'<script>(.*)</script>',s,re.S).group(1))
print('ok')
