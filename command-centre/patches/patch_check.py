import os,re
os.chdir('/tmp/claude-0/-home-claude/f551496a-6099-53c0-bb40-c24e871c007b/scratchpad')
p='cc/src.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)

# 1. replace the three save-immediately draft tools with one review-gated tool
a0 = s.index("      { name: 'gmail_draft',")
a1 = s.index("      { name: 'pin_card',")
s = s[:a0] + s[a1:]
b0 = s.index("      { name: 'draft_reply',")
b1 = s.index("        } }\n    ];", b0) + len("        } }")
s = s[:b0] + r"""      { name: 'propose_draft', description: 'Prepare a client-facing draft for Yasser to review. It is NOT saved: the page runs three independent checks (facts vs the source, names/dates/numbers/promises, tone/recipient) and Yasser reads it and saves it himself. Use for every email or message you write for him. mailbox: "gmail", "outlook", or "none" (work inbox in the Outlook app, LinkedIn, WhatsApp: he copies it). kind: "reply" or "new". For a Gmail reply pass threadId and replyToMessageId (the thread\'s lastMessageId) and the sender in to. For an Outlook reply pass messageId and uri. basis: REQUIRED, the exact source you relied on: the original message text (quote it) plus anything Yasser told you in this chat. body: plain text, no markdown.',
        inputSchema: { type: 'object', properties: { mailbox: { type: 'string', enum: ['gmail', 'outlook', 'none'] }, kind: { type: 'string', enum: ['reply', 'new'] }, to: { type: 'array', items: { type: 'string' } }, cc: { type: 'array', items: { type: 'string' } }, subject: { type: 'string' }, body: { type: 'string' }, threadId: { type: 'string' }, replyToMessageId: { type: 'string' }, messageId: { type: 'string' }, uri: { type: 'string' }, basis: { type: 'string' }, channel: { type: 'string', description: 'Email, LinkedIn or WhatsApp' } }, required: ['mailbox', 'body', 'basis'] },
        execute: function(input){
          step('Preparing the draft for your checks…');
          proposeDraft(input);
          return { status: 'shown_for_review', note: 'Not saved. The page is running three independent checks and Yasser will review and save it himself. Do not say it was saved or sent. Briefly tell him it is ready for his review below.' };
        } }""" + s[b1:]
rep("'Tools: search_gmail, read_gmail, gmail_draft for Gmail; search_email, read_email, draft_reply, draft_email for Outlook;",
    "'Tools: search_gmail, read_gmail for Gmail; search_email, read_email for Outlook; propose_draft for every email or message you write (client-facing: it is triple checked and Yasser saves it himself, so never claim a draft was saved);")
rep("'Tools: search_gmail", "'Everything Yasser sends is client-facing: be exact. Never state a fact, name, date, price, attachment or promise that is not in the source or in what Yasser told you; leave a [bracket] instead.\\n' + 'Tools: search_gmail")

# 2. checks engine + review card
rep("  // ---- human reply writer", r"""  // ---- triple check for anything client-facing
  var CHECKS = [
    { key: 'facts', name: 'Facts match the source', focus: 'Every factual statement in the DRAFT (what was said, agreed, sent, attached, requested, scheduled) must be supported by the SOURCE. Flag anything not supported, contradicted, or overstated.' },
    { key: 'details', name: 'Names, dates, numbers and promises', focus: 'Check every name (spelling, the right person addressed, first name used correctly), company and title; every date, weekday-vs-date match, time and time zone; every price, quantity and reference number; every attachment mentioned; every commitment or deadline Yasser would be making. Flag anything wrong, unsupported or risky to promise, and any unfilled [bracket].' },
    { key: 'tone', name: 'Tone, language and recipient', focus: 'Check it goes to the right recipient (to/cc match the source), is in the same language as the original, is professional and warm for a client, contains no internal-only information (internal team talk, costs, margins, notes), no AI-sounding phrases, and nothing embarrassing or ambiguous.' }
  ];
  function runChecks(d, source){
    var base = 'You are checking a message Yasser Obeid (CEO, a.k.a. Media, a production company) is about to send to a client or partner. Be strict and concrete. Today is ' + new Date().toLocaleDateString('en-GB', { timeZone: 'Asia/Dubai', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + ' (Dubai).\n\n'
      + 'SOURCE (the original message and what Yasser said):\n---\n' + String(source || '(none given)').slice(0, 20000) + '\n---\n\n'
      + 'DRAFT' + (d.channel ? ' (' + d.channel + ')' : '') + ':\n' + (d.to && d.to.length ? 'To: ' + d.to.join(', ') + '\n' : '') + (d.cc && d.cc.length ? 'Cc: ' + d.cc.join(', ') + '\n' : '') + (d.subject ? 'Subject: ' + d.subject + '\n' : '') + '---\n' + d.body + '\n---\n\n';
    return CHECKS.map(function(ck){
      var prompt = base + 'Your only job in this check: ' + ck.focus + '\nIgnore everything outside that job. Reply with only JSON: {"ok": true or false, "issues": ["short, specific issue quoting the words", ...]}. ok is true only if you found nothing to fix.';
      return sample.json(prompt, { cache: false }).then(function(r){
        var issues = Array.isArray(r && r.issues) ? r.issues.map(String).filter(Boolean).slice(0, 6) : [];
        return { key: ck.key, name: ck.name, ok: !!(r && r.ok) && !issues.length, issues: issues };
      }, function(e){ return { key: ck.key, name: ck.name, ok: false, failed: true, issues: ['This check could not run (' + ((e && e.code) || 'error') + '). Read this part yourself.'] }; });
    });
  }
  function fetchSource(d){
    var parts = [String(d.basis || '')];
    if(d.mailbox === 'gmail' && d.threadId && mcp){
      return mcp.callTool('Gmail', 'get_thread', { threadId: String(d.threadId), messageFormat: 'PLAIN_TEXT' }).then(function(r){
        var ms = (r.payload && r.payload.messages) || [];
        parts.push('ORIGINAL THREAD:\n' + ms.slice(-4).map(function(m){ return 'From: ' + m.sender + '\nTo: ' + (m.toRecipients || []).join(', ') + (m.ccRecipients && m.ccRecipients.length ? '\nCc: ' + m.ccRecipients.join(', ') : '') + '\nDate: ' + m.date + '\nSubject: ' + m.subject + '\n' + String(m.plaintextBody || m.snippet || '').slice(0, 5000); }).join('\n\n'));
        return parts.join('\n\n');
      }, function(){ return parts.join('\n\n'); });
    }
    if(d.mailbox === 'outlook' && d.uri && mcp){
      return mcp.callTool(M365, 'read_resource', { uri: String(d.uri) }).then(function(r){
        var o = resultObjects(r)[0] || {};
        var body = o.body && o.body.contentType === 'html' ? textOf(o.body.content) : String((o.body && o.body.content) || o.bodyPreview || '');
        parts.push('ORIGINAL EMAIL:\nFrom: ' + who(o.sender || o.from) + '\nTo: ' + (o.toRecipients || []).map(who).join(', ') + '\nDate: ' + o.receivedDateTime + '\nSubject: ' + o.subject + '\n' + body.slice(0, 8000));
        return parts.join('\n\n');
      }, function(){ return parts.join('\n\n'); });
    }
    return Promise.resolve(parts.join('\n\n'));
  }
  function checkList(host, d, source, onDone){
    var box = document.createElement('div'); box.className = 'checks';
    var head = document.createElement('div'); head.className = 'chh'; head.textContent = 'Triple check'; box.appendChild(head);
    var rows = CHECKS.map(function(ck){
      var r = document.createElement('div'); r.className = 'ck run'; r.innerHTML = '<span class="ci"></span><div><b></b><ul></ul></div>';
      r.querySelector('b').textContent = ck.name; box.appendChild(r); return r;
    });
    var you = document.createElement('div'); you.className = 'ck you'; you.innerHTML = '<span class="ci"></span><div><b>Your read</b><ul><li>Read it once yourself before saving or sending.</li></ul></div>'; box.appendChild(you);
    host.appendChild(box);
    if(!sample || !sample.json){ rows.forEach(function(r){ r.className = 'ck warn'; r.querySelector('ul').innerHTML = '<li>Checks aren’t available in this view. Read it carefully yourself.</li>'; }); onDone([]); return; }
    var results = runChecks(d, source);
    var all = [];
    results.forEach(function(pr, i){
      pr.then(function(res){
        all[i] = res; var r = rows[i]; r.className = 'ck ' + (res.ok ? 'ok' : 'warn');
        var ul = r.querySelector('ul'); ul.textContent = '';
        if(res.ok){ var li = document.createElement('li'); li.textContent = 'Nothing to fix.'; ul.appendChild(li); }
        res.issues.forEach(function(t){ var li2 = document.createElement('li'); li2.textContent = t; ul.appendChild(li2); });
      });
    });
    Promise.all(results).then(function(res){ onDone(res); });
  }
  function htmlBody(t){ return String(t || '').split(/\n{2,}/).map(function(p2){ return '<p>' + p2.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>') + '</p>'; }).join(''); }
  function saveDraftNow(d){
    if(d.mailbox === 'gmail'){
      var a = { body: d.body }; if(d.to && d.to.length) a.to = d.to; if(d.cc && d.cc.length) a.cc = d.cc; if(d.subject) a.subject = d.subject; if(d.replyToMessageId) a.replyToMessageId = d.replyToMessageId;
      return mcp.callTool('Gmail', 'create_draft', a).then(function(r){ var p3 = r.payload || {}; return p3.viewUrl || 'https://mail.google.com/mail/#drafts'; });
    }
    if(d.mailbox === 'outlook'){
      if(d.kind === 'reply' && d.messageId) return mcp.callTool(M365, 'outlook_create_reply_draft', { messageId: d.messageId, body: htmlBody(d.body), bodyType: 'html' }).then(function(r){ var o = resultObjects(r)[0] || {}; return o.webLink || 'https://outlook.office.com/mail/drafts'; });
      var b = { body: htmlBody(d.body), bodyType: 'html' }; if(d.to && d.to.length) b.to = d.to; if(d.cc && d.cc.length) b.cc = d.cc; if(d.subject) b.subject = d.subject;
      return mcp.callTool(M365, 'outlook_create_draft', b).then(function(r){ var o = resultObjects(r)[0] || {}; return o.webLink || 'https://outlook.office.com/mail/drafts'; });
    }
    return Promise.reject({ message: 'no mailbox' });
  }
  function proposeDraft(input){
    var d = { mailbox: ['gmail', 'outlook'].indexOf(input.mailbox) >= 0 ? input.mailbox : 'none', kind: input.kind === 'new' ? 'new' : 'reply', to: Array.isArray(input.to) ? input.to.map(String) : [], cc: Array.isArray(input.cc) ? input.cc.map(String) : [], subject: input.subject ? String(input.subject) : '', body: String(input.body || '').trim(), threadId: input.threadId ? String(input.threadId) : '', replyToMessageId: input.replyToMessageId ? String(input.replyToMessageId) : '', messageId: input.messageId ? String(input.messageId) : '', uri: input.uri ? String(input.uri) : '', basis: String(input.basis || ''), channel: input.channel ? String(input.channel) : (input.mailbox === 'none' ? '' : 'Email') };
    if(!popOpen()) openPop();
    var th = $('pthread'), card = document.createElement('div'); card.className = 'rev';
    var where = d.mailbox === 'gmail' ? 'Gmail draft' : d.mailbox === 'outlook' ? 'Outlook draft' : (d.channel || 'Message') + ' to copy';
    card.innerHTML = '<div class="revh"><b></b><span></span></div><div class="meta2"></div><textarea class="revtext" rows="8" aria-label="Draft text"></textarea><div class="revacts"></div>';
    card.querySelector('.revh b').textContent = 'Draft for your review'; card.querySelector('.revh span').textContent = where;
    var meta = []; if(d.to.length) meta.push('To: ' + d.to.join(', ')); if(d.cc.length) meta.push('Cc: ' + d.cc.join(', ')); if(d.subject) meta.push('Subject: ' + d.subject);
    card.querySelector('.meta2').textContent = meta.join('  ·  '); if(!meta.length) card.querySelector('.meta2').remove();
    var ta = card.querySelector('.revtext'); ta.value = d.body;
    th.appendChild(card);
    var acts = card.querySelector('.revacts');
    var save = document.createElement('button'); save.type = 'button'; save.className = 'psend'; save.disabled = true;
    save.textContent = d.mailbox === 'none' ? 'Copy' : 'Save as draft'; save.title = 'Available once the three checks finish';
    var fix = document.createElement('button'); fix.type = 'button'; fix.className = 'pbtn'; fix.textContent = 'Fix the issues'; fix.hidden = true;
    var status = document.createElement('small'); status.className = 'revst'; status.textContent = 'Running three checks…';
    acts.append(save, fix, status);
    var lastRes = [];
    var start = function(){
      d.body = ta.value.trim();
      var old = card.querySelector('.checks'); if(old) old.remove();
      save.disabled = true; fix.hidden = true; status.textContent = 'Running three checks…';
      fetchSource(d).then(function(src){
        checkList(card, d, src, function(res){
          lastRes = res;
          var bad = res.filter(function(x){ return !x.ok; });
          save.disabled = false;
          if(bad.length){ fix.hidden = false; status.textContent = bad.length + ' of 3 checks found something. Fix it, or save anyway after reading.'; save.textContent = d.mailbox === 'none' ? 'Copy anyway' : 'Save anyway'; }
          else { status.textContent = 'All three checks passed. Read it once, then save.'; save.textContent = d.mailbox === 'none' ? 'Copy' : 'Save as draft'; }
          card.appendChild(acts);
          $('pthread').scrollTop = $('pthread').scrollHeight;
        });
      });
    };
    var recheck = document.createElement('button'); recheck.type = 'button'; recheck.className = 'pbtn'; recheck.textContent = 'Check again'; recheck.hidden = true;
    acts.insertBefore(recheck, status);
    ta.addEventListener('input', function(){ recheck.hidden = false; save.disabled = true; status.textContent = 'You edited it. Check again before saving.'; });
    recheck.addEventListener('click', function(){ recheck.hidden = true; start(); });
    fix.addEventListener('click', function(){
      var issues = lastRes.filter(function(x){ return !x.ok; }).map(function(x){ return x.name + ': ' + x.issues.join('; '); }).join('\n');
      ask('The checks found issues in the draft. Fix only these, keep everything else, and propose the corrected draft again with propose_draft (same mailbox and details):\n' + issues + '\n\nCurrent draft:\n' + ta.value, false, 'Fix the issues the checks found');
    });
    save.addEventListener('click', function(){
      d.body = ta.value.trim();
      if(d.mailbox === 'none'){
        var t = d.body;
        try { navigator.clipboard.writeText(t).then(function(){ status.textContent = 'Copied. Paste it where you need it.'; }, function(){ ta.select(); status.textContent = 'Selected: press Cmd+C to copy.'; }); } catch(e){ ta.select(); status.textContent = 'Selected: press Cmd+C to copy.'; }
        return;
      }
      save.disabled = true; status.textContent = 'Saving the draft…';
      saveDraftNow(d).then(function(link){
        status.textContent = ''; var a = document.createElement('a'); a.href = link; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = 'Saved as a draft. Open it ↗'; status.appendChild(a);
        save.textContent = 'Saved'; ta.readOnly = true; fix.hidden = true; recheck.hidden = true;
      }, function(e){ save.disabled = false; status.textContent = (e && e.code) ? m365Copy(e).replace(/Microsoft 365/g, d.mailbox === 'gmail' ? 'Gmail' : 'Microsoft 365') : 'Couldn’t save the draft. Try again.'; });
    });
    start();
  }

  // ---- human reply writer""")

# 3. reply writer: run the same checks after writing
rep("""      rwLast = r.text.trim().replace(/^"+|"+$/g, ''); $('rwText').textContent = rwLast; $('rwNote').textContent = '';""",
"""      rwLast = r.text.trim().replace(/^"+|"+$/g, ''); $('rwText').textContent = rwLast; $('rwNote').textContent = '';
      var host = $('rwChecks'); host.textContent = ''; $('rwCopy').textContent = 'Checking\\u2026'; $('rwCopy').disabled = true;
      checkList(host, { body: rwLast, channel: rwChannel, to: [], cc: [] }, 'Message received:\\n' + $('rwIn').value + ($('rwWant').value.trim() ? '\\n\\nWhat Yasser wants to say: ' + $('rwWant').value.trim() : ''), function(res){
        var bad = res.filter(function(x){ return !x.ok; }).length;
        $('rwCopy').disabled = false; $('rwCopy').textContent = bad ? 'Copy anyway' : 'Copy';
        $('rwNote').textContent = bad ? bad + ' of 3 checks found something. Use a rewrite or edit before sending.' : 'All three checks passed. Read it once before sending.';
      });""")
rep("""          <div class="rwtext" id="rwText"></div>""", """          <div class="rwtext" id="rwText"></div>
          <div id="rwChecks"></div>""")
rep("""    $('rwNote').textContent = 'Writing…'; $('rwOut').hidden = false; $('rwText').textContent = '';""",
    """    $('rwNote').textContent = 'Writing…'; $('rwOut').hidden = false; $('rwText').textContent = ''; $('rwChecks').textContent = '';""")
rep("  function doWithClaude(label, prompt){", "  function doWithClaude(label, prompt){ prompt += ' When you write anything for me to send, use propose_draft so it gets checked.';")

# CSS
rep(".sempty{margin:0;", """.rev{align-self:stretch;border:1px solid var(--line);border-left:3px solid var(--red);border-radius:14px;background:var(--panel);padding:12px;display:flex;flex-direction:column;gap:8px}
.revh{display:flex;align-items:baseline;gap:8px}
.revh b{font:600 14px/1.2 "Outfit",sans-serif}
.revh span{font-size:12px;color:var(--muted)}
.meta2{font-size:12.5px;color:var(--muted);overflow-wrap:anywhere}
.revtext{font:inherit;font-size:14.5px;line-height:1.5;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:9px 11px;resize:vertical;width:100%}
.revacts{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.revacts .psend{height:36px}
.revacts .psend[disabled]{opacity:.45;cursor:default}
.revst{font-size:12.5px;color:var(--muted)}
.revst a{color:var(--red);font-weight:600}
.checks{display:flex;flex-direction:column;gap:6px;border-top:1px dashed var(--line);padding-top:8px}
.chh{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.ck{display:grid;grid-template-columns:18px 1fr;gap:8px;align-items:start;font-size:13px}
.ck b{font-weight:600;font-size:13px}
.ck ul{margin:2px 0 0;padding-left:16px;color:var(--muted)}
.ck.warn ul{color:var(--ink)}
.ck .ci{width:16px;height:16px;border-radius:50%;margin-top:1px;border:2px solid var(--line)}
.ck.run .ci{border-color:var(--line);border-top-color:var(--red);animation:spin 1s linear infinite}
.ck.ok .ci{border-color:var(--ok);background:var(--ok)}
.ck.warn .ci{border-color:#E0A526;background:#E0A526}
.ck.you .ci{border-color:var(--ink)}
@keyframes spin{to{transform:rotate(360deg)}}
.sempty{margin:0;""")
open(p,'w').write(s)
s=s.replace('LOGO_L',open('logo_light.txt').read()).replace('LOGO_D',open('logo_dark.txt').read())
open('cc/command-centre.html','w').write(s)
open('cc/a.js','w').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
print('ok')
