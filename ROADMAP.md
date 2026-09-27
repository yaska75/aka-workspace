# Roadmap

## Shipped
- **Command Centre: pin, hide, remind, and Dubai/local clocks** (27 Sep 2026). Every item can be pinned (star, moves to the
  top), hidden (collapses to a thin line at the bottom, undo with the same button), or given a reminder (pick a quick
  option or a custom time; it rings with sound and flashes on screen until you Stop or Snooze). Reminders and pins/hides
  live in their own place in the database, separate from the cards the scheduled syncs overwrite, so they survive every
  hourly refresh. Honest limit: a reminder only rings while this page is open in a browser tab — it cannot wake your phone
  or fire while the tab is closed. The page footer also shows two big clocks side by side: your browser's local time and
  Dubai time, so you always know both at a glance while travelling.
- **Team board sign-in** (27 Sep 2026). Everyone picks their name and sets a password on first sign-in.
  Passwords are stored in plain text in the page, on purpose: Yasser (superuser) can see and change everyone's
  password from the Team panel, and admins can see and change passwords for members (not for other admins or Yasser).
  Anyone can change their own password ("Change my password"). 5 wrong tries locks that name out for 30 seconds.
  Honest limit: this keeps people from posting as each other by mistake and lets Yasser help with a forgotten
  password directly, not real security against someone determined who can read the page. Real protection is
  sharing the link only with the team. The page is shared as "Anyone with the link" so it can be sent to the team.

## Ideas mentioned, not started
- Instagram DMs in the Command Centre (needs an Instagram Business/Creator account connected via Composio).
- Forward yasser@akamedia.ae (Namecheap Private Email) into Gmail so work mail can be read and drafted without the Mac.
- Spotify player (needs Spotify Premium and a Composio developer key). Apple Music embed is live now.

## Known limits
- Outlook, WhatsApp, Telegram and LinkedIn syncs need Yasser's Mac awake with Claude desktop, the apps and Chrome open.
  If the Mac is away for a while, a task can be suspended ("device absent") and needs switching back on.
- Telegram only shows the part of the chat list that is visible on screen.
- Opening LinkedIn messaging marks the newest conversation read.
