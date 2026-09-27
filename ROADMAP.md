# Roadmap

## Shipped
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
- Spotify player (needs Spotify Premium and a Composio developer key). Apple Music embed is live now.

## Known limits
- Outlook, WhatsApp, Telegram and LinkedIn syncs need Yasser's Mac awake with Claude desktop, the apps and Chrome open.
  If the Mac is away for a while, a task can be suspended ("device absent") and needs switching back on.
- Telegram only shows the part of the chat list that is visible on screen.
- Opening LinkedIn messaging marks the newest conversation read.
