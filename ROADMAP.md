# Roadmap

## Shipped
- **Fix: "blocked" screen on signing in as Yasser/Pieter** (28 Sep 2026). The sign-in redirect to
  Command Centre was briefly broken — right after entering your password you'd see a blank "This
  content is blocked" page instead of Command Centre. It opens its own tab now (the same way the
  header's "Command Centre ↗" button already did) instead of trying to load Command Centre inside
  the team board's own page, which is what was causing the blocked screen.
- **Team board sign-in now routes you straight to Command Centre (Yasser and Pieter only)** (27 Sep 2026). Signing
  in on the team board is the one login for everyone. Now, for Yasser and Pieter specifically, the moment you enter
  your password you're taken straight to Command Centre instead of landing on the task page and needing an extra
  click. Everyone else signs in and sees the task page exactly as before — nothing changed for them. This only
  fires on the actual sign-in action (typing your password), not every time the team board tab reloads while
  you're still signed in — so the "My to-do list ↗" button in Command Centre still works normally to get back to
  the task page without immediately bouncing you back.
- **Quick switch between the Command Centre and the team board** (27 Sep 2026). The Command Centre header has a
  "My to-do list ↗" button that jumps to the team board, and the team board header shows a matching
  "Command Centre ↗" button — for Yasser and Pieter, since Command Centre is currently only theirs (everyone else
  just uses the task page for now). Both buttons reuse the same browser tab if one is already open, instead of
  opening a new tab every time, and both are now filled in solid brand red so they're easy to spot at a glance.
- **Command Centre: groundwork for Pieter sharing it with Yasser** (27 Sep 2026). Behind the scenes, Command Centre
  now knows there can be more than one person opening it — the team board's "Command Centre" button passes along
  who clicked it. Nothing changes yet for what either of them sees; this is just the plumbing so Pieter's own
  version can be switched on once his email/WhatsApp/Telegram sync is set up (he uses Mac Mail, not Outlook, so
  that'll need its own connection, not the one Yasser uses).
- **Team board: peer reminders with a sound alarm and the task turning red** (27 Sep 2026). On any task that isn't
  your own, a new "⏰ Remind" button lets you set a reminder for whoever owns it — a quick pick (15 min, 1 hour,
  3 hours, tomorrow 9am) or a custom time. Until it's due, the task gets a dashed red edge on that person's board;
  once it's due, the whole card turns solid red and pulses, and the owner gets the same full-screen sound alarm as
  the existing "Attention alert" — with Snooze (10 min) and Done, stop. This is one-way and by design: you can
  remind teammates, and they can remind you, but nobody can set a reminder on their own task — that's what the
  Remind button is deliberately missing when you're looking at your own list.
- **Team board: task cards color-coded by how long they've sat uncleared** (27 Sep 2026). An open task's card now
  gets a colored left edge: light blue under 24 hours old, orange 24–48 hours, red past 48 hours. It's based on when
  the task was created, not its due date (that's the separate "Overdue" label). Done tasks never get a color. This
  is a quiet visual cue on top of the existing overdue marker, not a replacement for it.
- **Command Centre: "Make a Quote" widget** (27 Sep 2026). A new "Make" section: paste a brief (client, scope, crew,
  equipment, add-ons) into "Make a quote" and it builds a Google Sheets budget from your standard quote template
  (under akamediadigital@gmail.com) and posts the link back as a card, usually within the hour. The in-page Claude
  chat can't reach Google Sheets/Slides directly, so this works by queuing the brief and a scheduled task (hourly,
  7am–11pm Dubai) builds it and writes the result back — the same queue-and-return pattern as "To Promotions" for
  Outlook. It fills in what the brief gives it and leaves anything it can't infer (like a rate the template doesn't
  have) blank rather than guessing. "Make a Presentation" (Google Slides) is a disabled placeholder for now — next,
  once this is proven out. Always check the numbers before sending a quote out.
- **Command Centre: "Make a quote" from an attached brief file, not just pasted text** (27 Sep 2026). An "Attach a PDF"
  button next to the brief box uploads a PDF straight from your device — no Drive step, no link to paste — and the
  scheduled task pulls the text out of it and builds the quote from that (plus anything you typed). Direct attach only
  takes PDF (a platform limit on this kind of upload); for PowerPoint or anything else, there's still a "paste a Drive
  link" field below it — upload to Drive once and paste the share link, same as before. If the file can't be read for
  some reason, the job still runs off whatever text you typed and the result card says honestly that the file didn't
  come through.
- **Command Centre: full LinkedIn messages, not just a summary** (27 Sep 2026). The LinkedIn sync now opens your top
  8 conversations and captures the other person's exact message, not just a one-line gloss. Each item with a full
  message gets a "Read full message" button that shows it in place; "Do it with Claude" on that item drafts a reply
  straight from the real words, instead of asking you to paste the message. Honest trade-off: opening a conversation
  to read it marks it read on LinkedIn, so more conversations now show as read after each hourly sync than before.
- **Command Centre: Spotify instead of Apple Music** (27 Sep 2026). The music player (header note button) now embeds a
  Spotify playlist (AVICII - Essentials) instead of Apple Music, with an "Open in Spotify" link and the same
  play/hide/stop controls as before. Full songs need you signed in to Spotify in that browser; otherwise you get
  30-second previews.
- **Command Centre: theme picker (Classic, Sunset, Ocean, Neon)** (27 Sep 2026). A dropdown next to the Gmail and
  Microsoft 365 status pills lets you pick a skin for this device, matching the team board's four themes: Classic
  (the usual a.k.a. red, auto light/dark), Sunset (warm sand and terracotta, serif headings), Ocean (cool
  blue-teal), or Neon (near-black with violet/cyan, futuristic headings). The choice is remembered per device.
- **Team board: theme picker (Classic, Sunset, Ocean, Neon)** (27 Sep 2026). A new dropdown next to the sound and
  notification buttons lets each person pick a skin for their own device: Classic (the usual a.k.a. red, auto
  light/dark), Sunset (warm sand and terracotta, serif headings), Ocean (cool blue-teal), or Neon (near-black with
  violet/cyan, futuristic headings). The choice is remembered per device, same as the fold and sound settings.
- **Team board: collapsed lists, your current time, and a deposit-folder hint for task results** (27 Sep 2026). On
  the task screen, everyone else's list now starts folded down to just their name and photo — click it (or the
  arrow) to open it up and add or see their tasks. Your own list still opens by default. Each person's fold choice
  is remembered on that device. Your current local time now shows at the top of the page, next to the other
  buttons. Each task's "Deposit result" button (renamed from "Attach") now also suggests the Drive folder to use —
  your name, then the task name — before you paste the resulting share link, so results end up organized instead
  of loose in one folder.
- **Team board: browser notifications, on this device** (27 Sep 2026). Each person can click "Notify me on this
  device" (top bar, once signed in) to turn on browser notifications for new tasks and chat messages, on that
  browser/device only. They arrive 9am–21:00 Dubai time; outside that window they're held back silently unless
  someone uses the existing urgent alert/alarm, which always comes through. Notifications only fire while the tab
  is in the background (so you don't get a duplicate of the in-page pop-up while watching the screen). Honest
  limits: this is a real WhatsApp-style ping, not an actual WhatsApp message — it needs the person to have said
  yes once on that specific device/browser, and like any browser notification it may not reliably wake a phone
  once the browser is fully closed or the phone is locked for a long time. A real WhatsApp message (arriving in
  the WhatsApp app itself) needs a WhatsApp Business API sender — see "Ideas mentioned, not started" below.
- **Command Centre: pin, hide, remind, and Dubai/local clocks** (27 Sep 2026). Every item can be pinned (star, moves to the
  top), hidden (collapses to a thin line at the bottom, undo with the same button), or given a reminder (pick a quick
  option or a custom time; it rings with sound and flashes on screen until you Stop or Snooze). Reminders and pins/hides
  live in their own place in the database, separate from the cards the scheduled syncs overwrite, so they survive every
  hourly refresh. Honest limit: a reminder only rings while this page is open in a browser tab — it cannot wake your phone
  or fire while the tab is closed. The page footer also shows two big clocks side by side: your browser's local time and
  Dubai time, so you always know both at a glance while travelling. You can also set your location manually (pencil/edit
  next to the clock) if the browser guesses it wrong — pick a known city or, for anywhere else, type a name and choose
  its time zone from a list. The choice is remembered on this device.
- **Team board: communications panel, task progress/notes, remove, and Dubai clocks** (27 Sep 2026). On a wide screen the
  team chat now opens as a docked panel on the right by default as soon as you sign in, instead of needing a click —
  close it any time and it stays closed until you reopen it. Each task can carry a progress bar (drag the slider) and a
  short note, visible to everyone who can see that list. Each task's "Remove from list" button takes it off the list for
  good (tap once to arm it, again to confirm). Each person's "Currently in…" location badge now also shows Dubai's
  current time side by side, so it is easy to compare anyone's time to Dubai's — set your own location manually the same
  way as before (click "Currently in…", type a city or pick a time zone).
- **Team board: online/asleep status and urgent chat alerts** (27 Sep 2026). Each person's column shows Online (their
  tab is active) or Asleep (it isn't) to the rest of the team. The chat composer has an urgent (🔔) toggle: send with it
  on and the recipients get the same full-screen, sound-and-flash alarm as the existing Alert button, until they
  acknowledge it.
- **Team board sign-in** (27 Sep 2026). Everyone picks their name and sets a password on first sign-in.
  Passwords are stored in plain text in the page, on purpose: Yasser (superuser) can see and change everyone's
  password from the Team panel, and admins can see and change passwords for members (not for other admins or Yasser).
  Anyone can change their own password ("Change my password"). 5 wrong tries locks that name out for 30 seconds.
  Honest limit: this keeps people from posting as each other by mistake and lets Yasser help with a forgotten
  password directly, not real security against someone determined who can read the page. Real protection is
  sharing the link only with the team. The page is shared as "Anyone with the link" so it can be sent to the team.

## Ideas mentioned, not started
- Real WhatsApp messages for task/chat notifications (not just browser alerts), via a WhatsApp Business API sender
  through Twilio: register a WhatsApp sender in the Twilio Console, test it in Twilio's sandbox, get message
  templates approved (any business-initiated message outside a 24-hour reply window needs an approved template),
  then hand the resulting Account SID / Auth Token / WhatsApp number back to Claude to wire in.
- Instagram DMs in the Command Centre (needs an Instagram Business/Creator account connected via Composio).
- Forward yasser@akamedia.ae (Namecheap Private Email) into Gmail so work mail can be read and drafted without the Mac.

## Known limits
- Outlook, WhatsApp, Telegram and LinkedIn syncs need Yasser's Mac awake with Claude desktop, the apps and Chrome open.
  If the Mac is away for a while, a task can be suspended ("device absent") and needs switching back on.
- Telegram only shows the part of the chat list that is visible on screen.
- The LinkedIn sync now opens each of the top 8 conversations to read the sender's exact message, not just the newest
  one, so it marks each of those as read on LinkedIn (not just the newest, as before).
