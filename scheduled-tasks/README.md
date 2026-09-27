# Scheduled tasks

All times Dubai. Each task's full instructions live in the task itself (Claude: `list_triggers` shows them).
Every sync is read-only and never sends, replies, posts or deletes. The one exception is Outlook's "Move to Other", which only happens when Yasser queues it with the "To Promotions" button.

| Task | ID | When | Runs on | Writes card |
|---|---|---|---|---|
| Outlook to Command Centre | trig_01QCvEV4bEcBQCvGSBeF1WFJ | :48, 7am–10pm | Yasser's Mac (Outlook app) | `outlook-work`, processes `actions` queue |
| LinkedIn to Command Centre | trig_01PBqQ8prsstrhbHk9TpmbqV | :18, 8am–10pm | Chrome on the Mac | `linkedin-inbox` (top 8 items get the sender's exact message, in `body`; opening each one to read it does mark it read on LinkedIn) |
| WhatsApp and Telegram to Command Centre | trig_017noWFvq6o5Ggv5Bs6ECmSg | :33, 8am–10pm | Mac (both apps) | `whatsapp-chats`, `telegram-chats` |
| Team board to-do sync | trig_0116P6TkHNDnue1XJ5SDmJc9 | :05, 7am–11pm | Cloud | `todo-mine`, `team-chat` |
| Posting reminder (LinkedIn + Instagram) | trig_01B3PQiYTp6DKu4NM7XKTNe4 | 9:51am daily, phone notification | Chrome on the Mac | `posting-rhythm` |
| Make a Quote — build from queued brief | trig_01QGydvjFpMPDn6xv1kPeaEw | :12, 7am–11pm | Cloud (Composio, akamediadigital@gmail.com) | processes `actions` queue (`type: make-quote`, brief text and/or a Drive `fileLink` to a PDF/PPT), writes `make-quote-<job id>` |

This one isn't read-only by the table above's rule: it creates a new Google Sheet (a copy of the quote master template)
and writes into it, but only ever under akamediadigital@gmail.com, never Yasser's own Google account, and never
shares or sends anything — Yasser still opens the link and checks the numbers himself.

## Card format (Command Centre database, collection `cards`)
`{ key, title, source, summary, items: [{ title, subtitle, when, priority: high|med|low, url, linkLabel, body?, ... }], text, wide, pulledAt, request, order }`
`source` picks the section: todo → To do; gmail/outlook → Email; calendar; team → Team; social → Social; anything else → Claude.
`body` (LinkedIn only, so far) is the sender's exact message text: the page shows a "Read full message" toggle for it, and "Do it with Claude" uses it to draft a reply straight away instead of asking Yasser to paste the message.
