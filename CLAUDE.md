# Instructions for Claude

Owner: Yasser Obeid, CEO of a.k.a. Media (Dubai). He is not a developer: talk in plain words, show results, not code.

## Non-negotiable rules
- Anything client-facing or public (emails, LinkedIn/WhatsApp/Telegram replies, social posts) is triple-checked before he sends it. The Command Centre's `propose_draft` review card runs three checks (facts, details, tone); keep it.
- Nothing is ever sent or posted automatically. Drafts are saved only after he approves.
- Scheduled syncs are read-only. Personal/family chats: names only, never message text.
- Never enter passwords; he signs in himself.

## Team board (`team-board/team.html`)
Artifact: https://claude.ai/artifact/8GwGDwq8AAmCDmQAqEZjif (capabilities: `artifact`, `room` with topic `alert` at `interact`).
The page saves itself: the team's live state (tasks, chat, reads, acks) is embedded in the published HTML, not in this repo.
To publish a change:
1. Edit `team-board/team.html` (the template, contains `__STATE__`).
2. Artifact `read` the URL with `path: "index.html"` to get the live page, then `python3 team-board/build.py <that file>`.
3. `node --check build/team-board.js`; run `team-board/tests/*.js` (they use `python3 team-board/build.py` with the sample fixture, so rebuild with the live file after testing).
4. Publish `build/team-board.html` to the same URL (omit `capabilities` to keep them). If refused because the page saved a newer version, re-read, rebuild, republish.
Never publish a build made from `fixtures/sample-state.json`: it would wipe the team's data.

## Command Centre (`command-centre/src.html`)
Artifact: https://claude.ai/artifact/Qa1bpKvs9DmNekwfiT2TtZ (private to Yasser).
Capabilities: `mcp` (Gmail: search_threads, get_thread, create_draft, label_thread, unlabel_thread; Microsoft 365: outlook_email_search, read_resource, outlook_calendar_search, chat_message_search, outlook_create_draft, outlook_create_reply_draft), `sample`, `db`. Omit `capabilities` on republish to keep them.
Build: `python3 command-centre/build.py` → `build/command-centre.html`; `node --check build/command-centre.js`; run `command-centre/tests/*.js`; publish.
Cards live in the page database (collection `cards`); write them with ArtifactData. Cards that scheduled tasks own must never be removed: outlook-work, linkedin-inbox, todo-mine, team-chat, whatsapp-chats, telegram-chats, posting-rhythm.
Mail: yasser@akamedia.ae is on Namecheap Private Email and is only reachable through the Outlook desktop app on his Mac.

## Working here
- One feature per commit, with a plain-English message. Keep `ROADMAP.md` and `scheduled-tasks/README.md` current.
- Tests need Playwright with Chromium (preinstalled in Claude's cloud workspace).
- Design: a.k.a. red accent, Outfit + Instrument Sans fonts, light and dark themes, works on phones.
