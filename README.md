# a.k.a. Media workspace

The source for the two pages a.k.a. Media runs inside Claude:

| Page | Who uses it | Link |
|---|---|---|
| **Team board** | Everyone: to-do lists, team chat, DMs, files, calls, alerts | https://claude.ai/artifact/8GwGDwq8AAmCDmQAqEZjif |
| **Command Centre** | Yasser only: email, calendar, LinkedIn, WhatsApp, Telegram, to-do, team chat, Claude chat, music, posting reminders | https://claude.ai/artifact/Qa1bpKvs9DmNekwfiT2TtZ |

## How to improve it

Open a Claude chat with this repository attached and say what you want, for example
"add a notes section to the Command Centre" or "let Finance see the Production list".
Claude reads `CLAUDE.md`, makes the change here, tests it, publishes the page and commits.
Every change is a commit, so any version can be brought back.

Ideas and unfinished work are in `ROADMAP.md`.

## What's in here

- `team-board/team.html`: the team board (the team's tasks and chat are *not* stored here; they live in the published page)
- `command-centre/src.html`: the Command Centre (its cards live in the page's own database)
- `scheduled-tasks/`: the hourly and daily jobs that fill the Command Centre
- `assets/`: a.k.a. logos (light and dark) used by both pages
- `*/tests/`: browser tests that run before every publish
- `*/patches/`: history of how each feature was added
