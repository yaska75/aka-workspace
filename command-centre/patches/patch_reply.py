p='cc/src.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep("""    <div class="reply" id="reply" hidden aria-live="polite">""", """    <details class="rw" id="rw">
      <summary>Write a reply for me</summary>
      <div class="rwb">
        <div class="rwrow">
          <div class="seg" role="group" aria-label="Where the reply goes" id="rwCh">
            <button type="button" data-ch="Email" aria-pressed="true">Email</button>
            <button type="button" data-ch="LinkedIn" aria-pressed="false">LinkedIn</button>
            <button type="button" data-ch="WhatsApp" aria-pressed="false">WhatsApp</button>
          </div>
        </div>
        <textarea id="rwIn" rows="5" placeholder="Paste the message you received" aria-label="Message you received"></textarea>
        <input type="text" id="rwWant" placeholder="What do you want to say? (optional) e.g. yes to Tuesday, send the quote Monday" aria-label="What you want to say">
        <div class="rwrow"><button type="button" class="go small" id="rwGo">Write reply</button><span class="steps" id="rwNote"></span></div>
        <div class="rwout" id="rwOut" hidden>
          <div class="rwtext" id="rwText"></div>
          <div class="rwrow">
            <button type="button" class="chip" id="rwCopy">Copy</button>
            <button type="button" class="chip" data-tweak="Make it shorter.">Shorter</button>
            <button type="button" class="chip" data-tweak="Make it warmer and more personal.">Warmer</button>
            <button type="button" class="chip" data-tweak="Make it more formal.">More formal</button>
            <button type="button" class="chip" data-tweak="Write a different version.">Try again</button>
          </div>
        </div>
      </div>
    </details>
    <div class="reply" id="reply" hidden aria-live="polite">""")
rep(".sempty{margin:0;", """.rw{border:1px solid var(--line);border-radius:14px;background:var(--bg)}
.rw summary{cursor:pointer;padding:10px 14px;font-weight:600;font-size:14px;list-style:none;display:flex;align-items:center;gap:8px}
.rw summary::-webkit-details-marker{display:none}
.rw summary::before{content:"+";display:inline-grid;place-items:center;width:20px;height:20px;border-radius:6px;background:var(--red);color:var(--red-ink);font-weight:700}
.rw[open] summary::before{content:"\\2212"}
.rwb{display:flex;flex-direction:column;gap:10px;padding:0 14px 14px}
.rwb textarea,.rwb input{font:inherit;font-size:14.5px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:9px 11px;width:100%;resize:vertical}
.rwb textarea:focus,.rwb input:focus{outline:none;border-color:var(--red)}
.rwrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.seg{display:flex;gap:2px;background:var(--soft);border-radius:10px;padding:3px}
.seg button{border:0;background:none;padding:5px 12px;border-radius:8px;font-size:13px;color:var(--muted)}
.seg button[aria-pressed=true]{background:var(--panel);color:var(--ink);font-weight:600}
.go.small{height:38px;padding:0 16px;border:0;border-radius:10px;background:var(--red);color:var(--red-ink);font-weight:600}
.rwout{display:flex;flex-direction:column;gap:10px}
.rwtext{white-space:pre-wrap;background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--red);border-radius:10px;padding:12px 14px;font-size:15px;line-height:1.55}
.sempty{margin:0;""")

# JS: reply writer
rep("""  var BRIEF = 'Brief me.""", r"""  // ---- human reply writer (email, LinkedIn, WhatsApp)
  var rwChannel = 'Email', rwLast = '', rwBusy = null;
  Array.prototype.forEach.call(document.querySelectorAll('#rwCh button'), function(b){ b.addEventListener('click', function(){ rwChannel = b.dataset.ch; Array.prototype.forEach.call(document.querySelectorAll('#rwCh button'), function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); }); });
  var VOICE = 'You write replies as Yasser Obeid, founder and CEO of a.k.a. Media, a production company in Dubai (also Abu Dhabi, Riyadh, Cape Town). He is warm, direct and busy.\n'
    + 'Write like a real person typing quickly, not like an assistant:\n'
    + '- Short. Get to the point in the first line. No throat-clearing ("I hope this email finds you well", "Thank you for reaching out", "I wanted to").\n'
    + '- Plain words, contractions, varied sentence length. No corporate filler (leverage, synergy, delighted, seamless, circle back, touch base, valuable insights).\n'
    + '- No em dashes, no semicolons, no bullet lists unless the message truly needs one, no headings, no bold, no emojis unless the other person used them.\n'
    + '- Do not repeat their message back to them. Do not over-thank. One question at most.\n'
    + '- Never invent facts, prices, dates or commitments. If something is needed that you do not know, leave a short [bracket] for Yasser to fill.\n'
    + '- Reply in the same language as the message (Arabic stays Arabic, Russian stays Russian).\n';
  function rwPrompt(extra){
    var ch = rwChannel, msg = $('rwIn').value.trim().slice(0, 12000), want = $('rwWant').value.trim();
    var fmt = ch === 'Email' ? 'This is an email reply: greeting with their first name ("Hi Sam,"), 2 to 5 short lines, then sign off "Best,\nYasser" (or just "Yasser" if the thread is casual). No subject line.'
      : ch === 'LinkedIn' ? 'This is a LinkedIn message: 1 to 4 short sentences, friendly and professional, first name greeting, no sign-off block, no hashtags.'
      : 'This is a WhatsApp message: 1 to 3 short lines, casual, no greeting formula, no sign-off.';
    return VOICE + fmt + '\n\nThe message he received:\n---\n' + msg + '\n---\n' + (want ? '\nWhat Yasser wants to say: ' + want + '\n' : '\nIf the right answer is unclear, write a short, natural holding reply.\n')
      + (extra && rwLast ? '\nYour previous draft:\n---\n' + rwLast + '\n---\n' + extra + '\n' : '')
      + '\nReturn only the reply text, nothing before or after it.';
  }
  function rwRun(extra){
    if(!sample){ $('rwNote').textContent = 'Claude isn’t available in this view.'; return; }
    if(!$('rwIn').value.trim()){ $('rwNote').textContent = 'Paste the message first.'; $('rwIn').focus(); return; }
    if(rwBusy) rwBusy.abort();
    rwBusy = new AbortController();
    $('rwNote').textContent = 'Writing…'; $('rwOut').hidden = false; $('rwText').textContent = '';
    sample(rwPrompt(extra), { signal: rwBusy.signal, cache: false, onText: function(u){ $('rwText').textContent = u.text.trim(); } }).then(function(r){
      rwLast = r.text.trim().replace(/^"+|"+$/g, ''); $('rwText').textContent = rwLast; $('rwNote').textContent = '';
    }, function(e){
      if(e && e.code === 'cancelled') return;
      if(e && e.text){ rwLast = e.text.trim(); $('rwText').textContent = rwLast; }
      $('rwNote').textContent = copyFor(e && e.code);
    }).then(function(){ rwBusy = null; });
  }
  $('rwGo').addEventListener('click', function(){ rwRun(''); });
  Array.prototype.forEach.call(document.querySelectorAll('[data-tweak]'), function(b){ b.addEventListener('click', function(){ rwRun(b.dataset.tweak); }); });
  $('rwCopy').addEventListener('click', function(){
    var t = $('rwText').textContent, b = $('rwCopy');
    function done(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy'; }, 1500); }
    try { navigator.clipboard.writeText(t).then(done, function(){ selectReply(); }); } catch(e){ selectReply(); }
  });
  function selectReply(){ var r = document.createRange(); r.selectNodeContents($('rwText')); var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); $('rwNote').textContent = 'Selected: press Cmd+C to copy.'; }
  function openWriter(context, channel){
    openSec('claude'); $('rw').open = true;
    if(channel){ var b = document.querySelector('#rwCh button[data-ch="' + channel + '"]'); if(b) b.click(); }
    $('rwIn').value = context; $('rwOut').hidden = true; $('rwNote').textContent = 'Paste the full email text here for the best reply, then press Write reply.';
    setTimeout(function(){ $('rw').scrollIntoView({ behavior: 'smooth', block: 'start' }); $('rwIn').focus(); }, 60);
  }

  var BRIEF = 'Brief me.""")
# card items: Write reply for email items without a mailbox connection (e.g. Outlook desktop)
rep("""          if(acts.children.length) li.appendChild(acts);""", """          if(secOf(c) === 'email' && !it.messageId && !it.threadId){
            var wr = document.createElement('button'); wr.type = 'button'; wr.className = 'mini'; wr.textContent = 'Write reply';
            wr.addEventListener('click', function(){ openWriter('Email: ' + (it.title || '') + (it.subtitle ? '\\n' + it.subtitle : '') + '\\n\\n', 'Email'); });
            acts.appendChild(wr);
          }
          if(acts.children.length) li.appendChild(acts);""")
open(p,'w').write(s); print('ok')
