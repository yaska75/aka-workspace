p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, (s.count(a), a[:80])
    s=s.replace(a,b)

rep(".del.arm{color:var(--strike);font-weight:600;opacity:1}",
""".del.arm{color:var(--strike);font-weight:600;opacity:1}
.mv{background:none;border:0;color:var(--muted);font-size:15px;line-height:1;padding:4px 6px;border-radius:6px}
.mv:hover{color:var(--ink);background:var(--soft)}
.mv:disabled{opacity:.25;cursor:default;background:none}
.item[draggable=true]{cursor:grab}
.item.dragging{opacity:.4}
.item.drop-before{box-shadow:inset 0 3px 0 var(--c)}
.item.drop-after{box-shadow:inset 0 -3px 0 var(--c)}""")

# sorting: manual order when the person has reordered their list
rep("""    open.sort(function(a,b){
      if(a.due !== b.due) return a.due < b.due ? -1 : 1;
      return (a.createdAt || 0) - (b.createdAt || 0);
    });""", """    var manual = person(pid) && person(pid).manual;
    open.sort(function(a,b){
      if(manual){
        var ao = typeof a.order === 'number' ? a.order : 1e15 + (a.createdAt || 0);
        var bo = typeof b.order === 'number' ? b.order : 1e15 + (b.createdAt || 0);
        if(ao !== bo) return ao - bo;
      }
      if(a.due !== b.due) return a.due < b.due ? -1 : 1;
      return (a.createdAt || 0) - (b.createdAt || 0);
    });""")

# 'Sort by date' link
rep("""          '<button class="link clear" type="button">Clear done tasks</button>' +""",
"""          '<span><button class="link bydate" type="button" hidden title="Go back to ordering by to do date">Sort by date</button> ' +
          '<button class="link clear" type="button">Clear done tasks</button></span>' +""")
rep("""    col.querySelector('.clear').addEventListener('click', function(){""",
"""    col.querySelector('.bydate').addEventListener('click', function(){
      if(mode === 'readonly') return;
      change({ type: 'bydate', pid: pid }); renderCol(pid);
    });
    col.querySelector('.clear').addEventListener('click', function(){""")
rep("    col.querySelector('.clear').hidden = done === 0;",
    "    col.querySelector('.clear').hidden = done === 0;\n    col.querySelector('.bydate').hidden = !p.manual || open < 2;")

# up/down buttons + drag and drop on open tasks
rep("    actions.append(edit, del);", """    if(!t.done && mode !== 'readonly'){
      var openList = sorted(pid).filter(function(x){ return !x.done; });
      var idx = -1; for(var k = 0; k < openList.length; k++){ if(openList[k].id === t.id){ idx = k; break; } }
      if(openList.length > 1){
        var up = document.createElement('button'); up.type = 'button'; up.className = 'mv mv-up'; up.textContent = '\\u2191';
        up.setAttribute('aria-label', 'Move up: ' + t.text); up.title = 'Move up'; up.disabled = idx <= 0;
        up.addEventListener('click', function(){ moveTask(pid, t.id, idx - 1, 'mv-up'); });
        var dn = document.createElement('button'); dn.type = 'button'; dn.className = 'mv mv-down'; dn.textContent = '\\u2193';
        dn.setAttribute('aria-label', 'Move down: ' + t.text); dn.title = 'Move down'; dn.disabled = idx >= openList.length - 1;
        dn.addEventListener('click', function(){ moveTask(pid, t.id, idx + 1, 'mv-down'); });
        actions.append(up, dn);
        li.draggable = true; li.title = 'Drag to change the order';
        li.addEventListener('dragstart', function(e){
          dragging = { pid: pid, id: t.id };
          try { e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', t.id); } catch(err){}
          li.classList.add('dragging');
        });
        li.addEventListener('dragend', function(){ dragging = null; li.classList.remove('dragging'); clearDropMarks(); });
        li.addEventListener('dragover', function(e){
          if(!dragging || dragging.pid !== pid || dragging.id === t.id) return;
          e.preventDefault();
          var r = li.getBoundingClientRect(), after = e.clientY > r.top + r.height / 2;
          clearDropMarks(); li.classList.add(after ? 'drop-after' : 'drop-before');
        });
        li.addEventListener('drop', function(e){
          if(!dragging || dragging.pid !== pid) return;
          e.preventDefault();
          var r = li.getBoundingClientRect(), after = e.clientY > r.top + r.height / 2;
          var from = -1; for(var j = 0; j < openList.length; j++){ if(openList[j].id === dragging.id){ from = j; break; } }
          var to = idx + (after ? 1 : 0); if(from < to) to--;
          var id = dragging.id; dragging = null; clearDropMarks();
          if(from >= 0) moveTask(pid, id, to);
        });
      }
    }
    actions.append(edit, del);""")

# move helpers (placed before task actions)
rep("  // ---------- task actions ----------", """  // ---------- reordering ----------
  var dragging = null;
  function clearDropMarks(){
    Array.prototype.forEach.call(document.querySelectorAll('.drop-before,.drop-after'), function(el){ el.classList.remove('drop-before', 'drop-after'); });
  }
  function moveTask(pid, id, to, refocus){
    if(mode === 'readonly') return;
    var open = sorted(pid).filter(function(t){ return !t.done; });
    var from = -1; for(var i = 0; i < open.length; i++){ if(open[i].id === id){ from = i; break; } }
    if(from < 0) return;
    to = Math.max(0, Math.min(open.length - 1, to));
    if(to === from) return;
    var item = open.splice(from, 1)[0]; open.splice(to, 0, item);
    var orders = {}; open.forEach(function(t, n){ orders[t.id] = n + 1; });
    change({ type: 'reorder', pid: pid, orders: orders });
    renderCol(pid);
    if(refocus){
      var b = ui[pid].list.querySelector('[data-key="' + id + '"] .' + refocus);
      if(b && !b.disabled) b.focus(); else { var o = ui[pid].list.querySelector('[data-key="' + id + '"] .mv:not(:disabled)'); if(o) o.focus(); }
    }
  }

  // ---------- task actions ----------""")

# journal ops
rep("""    if(o.type === 'add'){
      if(!list.some(function(t){ return t.id === o.task.id; })) list.push(JSON.parse(JSON.stringify(o.task)));""",
"""    if(o.type === 'reorder'){
      p.manual = true;
      list.forEach(function(t){ if(o.orders[t.id] !== undefined) t.order = o.orders[t.id]; });
      return;
    }
    if(o.type === 'bydate'){ p.manual = false; list.forEach(function(t){ delete t.order; }); return; }
    if(o.type === 'add'){
      if(!list.some(function(t){ return t.id === o.task.id; })){
        var nt = JSON.parse(JSON.stringify(o.task));
        if(p.manual && typeof nt.order !== 'number'){
          var mx = 0; list.forEach(function(t){ if(typeof t.order === 'number' && t.order > mx) mx = t.order; });
          nt.order = mx + 1;
        }
        list.push(nt);
      }""")
open(p,'w').write(s)
print('patched')
