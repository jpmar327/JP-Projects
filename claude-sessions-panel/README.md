# Claude Sessions panel for iTerm2

A side panel in iTerm2 that lists your Claude Code sessions, live.

- **Status dots:** Claude's spinner = working, pulsing amber = waiting for you, green = idle, grey = closed
- **Click** an open session to jump to its tab, or a closed one to resume it in a new tab
- **Filter** by All / Open / Working / Waiting / Idle / Closed, or by typing
- **Sort** by Recent, Name, Folder or Status; the ↓/↑ button flips the order
- **Delete** a closed session (hover it): asks first, then moves it to the Trash with a note on how to restore it
- **Finder** (hover a closed session) shows its file; **✕** or Esc clears the search

It also adds three terminal commands:

| Command | What it does |
|---|---|
| `csessions` | Numbered list of closed sessions; type a number to reopen one in a new tab |
| `tabname My Work` | Names the current tab (`tabname` alone clears it) |
| `claude` | Same Claude as before, but the tab turns orange while it runs and goes back afterwards |

## Requirements

macOS, [iTerm2](https://iterm2.com) 3.5 or newer, Claude Code, and zsh (the macOS default shell).

## Install

```
cd claude-sessions-panel
zsh install.sh
```

Then in iTerm2:

1. **Settings → General → Magic** → check **Enable Python API**
2. **Scripts → Manage → Install Python Runtime** (first time only)
3. **Scripts → AutoLaunch → claude_sessions_panel.py** (allow it when macOS asks)
4. **View → Toolbelt → Show Toolbelt**, then **View → Toolbelt → Claude Sessions**

After that the panel starts by itself whenever iTerm2 opens.

## Uninstall

```
zsh uninstall.sh
```

## What gets installed

| File | Purpose |
|---|---|
| `~/.config/claude-sessions/claude_sessions.py` | Finds sessions (shared by the panel and `csessions`) |
| `~/.config/claude-sessions/shell.zsh` | The `csessions`, `tabname` and `claude` commands |
| `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/claude_sessions_panel.py` | The panel |
| one line at the end of `~/.zshrc` | Loads `shell.zsh` (a backup of `~/.zshrc` is made first) |

## Good to know

- **Private:** it only reads your own `~/.claude` folder and only listens on `127.0.0.1` (your Mac), port 58731. Opening a tab needs a secret code that only the panel's page knows.
- **Light on resources:** about 35 MB of memory; after the first load each refresh takes around 0.01 s, and it pauses while the panel is hidden.
- **May need a fix after a Claude Code update:** it reads Claude Code's internal session files, which aren't a documented API.
- **Shows the last 30 days:** change `DAYS` at the top of the panel script, or run `csessions --days 90`.
