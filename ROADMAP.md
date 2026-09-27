# Roadmap

## Ready, waiting for a go-ahead
- **Team board login** (branch `login-screen`). Each person picks their name and signs in with a simple password; first sign-in creates it.
  Yasser (superuser) and admins can reset a password from the Team panel; there's "Change password" and "Sign out".
  Three-attempt lockout of 30 seconds after 5 wrong tries. Passwords are stored hashed (PBKDF2) in the page.
  - Still to do: run the browser test (`team-board/tests/t_login.js`), then publish.
  - Yasser should set his password first, before anyone else can pick his name.
  - Honest limit: this keeps teammates out of each other's accounts, not a determined attacker who can read the page. Real protection comes from sharing the page only with the team.

## Ideas mentioned, not started
- Instagram DMs in the Command Centre (needs an Instagram Business/Creator account connected via Composio).
- Forward yasser@akamedia.ae (Namecheap Private Email) into Gmail so work mail can be read and drafted without the Mac.
- Spotify player (needs Spotify Premium and a Composio developer key). Apple Music embed is live now.

## Known limits
- Outlook, WhatsApp, Telegram and LinkedIn syncs need Yasser's Mac awake with Claude desktop, the apps and Chrome open.
  If the Mac is away for a while, a task can be suspended ("device absent") and needs switching back on.
- Telegram only shows the part of the chat list that is visible on screen.
- Opening LinkedIn messaging marks the newest conversation read.
