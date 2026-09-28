# aftter v2

Lightweight Discord bot for a Minecraft community.

## Main features
- `/nuke` + `/nuke-confirm`: rebuilds the server into exactly 5 channels
- temporary voice rooms from `🔎・create [+]`
- moderation: warn, warnings, clear, kick, ban, timeout
- warning escalation: 3h / 24h / kick / ban thresholds
- anti-link filter
- clans with `[TAG] Name` nicknames and clan roles
- fun commands
- SQLite with WAL/NORMAL settings
- low-memory Discord intents and no message cache

## The 5 channels
— information —
- 📢・announcements
- 📄・readme

— community —
- 💬・chat

— support —
- 🆘・support

— voice —
- 🔎・create [+]

## Hosting / RAM
Designed for small free hosts. It does not use a web server, Redis, MongoDB, HTTP polling loop, or a message cache.

A real RAM number depends on Discord.py, Python, guild size and host overhead. The bot is intentionally optimized for low idle memory, but no honest implementation can guarantee a fixed RAM limit on every host.

## Install
Python 3.11+
`pip install -r requirements.txt`
Copy `.env.example` to `.env`, add token, then:
`python bot.py`

For faster slash-command updates during testing, set `GUILD_ID` to your server ID.
