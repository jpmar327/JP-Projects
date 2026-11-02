#!/bin/zsh
# Installs the Claude Sessions panel for iTerm2, plus the csessions / tabname / claude shell helpers.
# Safe to run again: it replaces its own files and never adds the ~/.zshrc line twice.
set -e

HERE="${0:A:h}"
LIB_DIR="$HOME/.config/claude-sessions"
AUTOLAUNCH="$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch"
ZSHRC="$HOME/.zshrc"
SOURCE_LINE='[[ -f ~/.config/claude-sessions/shell.zsh ]] && source ~/.config/claude-sessions/shell.zsh  # Claude Sessions'

[[ "$(uname)" == "Darwin" ]] || { echo "This needs macOS."; exit 1; }
[[ -d /Applications/iTerm.app ]] || { echo "iTerm2 isn't installed (https://iterm2.com)."; exit 1; }
command -v claude >/dev/null || echo "Note: 'claude' isn't on your PATH yet. The panel will be empty until you use Claude Code."

echo "1. Copying files"
mkdir -p "$LIB_DIR" "$AUTOLAUNCH"
cp "$HERE/claude_sessions.py" "$HERE/shell.zsh" "$LIB_DIR/"
cp "$HERE/claude_sessions_panel.py" "$AUTOLAUNCH/"

echo "2. Adding the shell helpers to ~/.zshrc"
if grep -qF "# Claude Sessions" "$ZSHRC" 2>/dev/null; then
  echo "   already there, skipped"
else
  [[ -f "$ZSHRC" ]] && cp "$ZSHRC" "$ZSHRC.bak-$(date +%Y%m%d-%H%M%S)"
  if grep -qE '^\s*(claude|tabname|csessions)\(\)' "$ZSHRC" 2>/dev/null; then
    echo "   WARNING: ~/.zshrc already defines claude(), tabname() or csessions(); the later definition wins."
  fi
  printf '\n%s\n' "$SOURCE_LINE" >> "$ZSHRC"
  echo "   done (backup saved next to ~/.zshrc)"
fi

echo "3. Starting the panel"
if lsof -nP -iTCP:58731 -sTCP:LISTEN >/dev/null 2>&1; then
  pkill -f claude_sessions_panel.py 2>/dev/null || true
  sleep 2
fi
if osascript -e 'tell application "iTerm2" to launch API script named "AutoLaunch/claude_sessions_panel.py"' >/dev/null 2>&1; then
  echo "   started"
else
  echo "   couldn't start it yet; finish the steps below, then pick Scripts > AutoLaunch > claude_sessions_panel.py"
fi

cat <<'EOF'

Almost done. In iTerm2:
  a. Settings > General > Magic: check "Enable Python API"
  b. Scripts > Manage > Install Python Runtime   (first time only)
  c. Scripts > AutoLaunch > claude_sessions_panel.py   (if it didn't start above; allow it when macOS asks)
  d. View > Toolbelt > Show Toolbelt, then View > Toolbelt > Claude Sessions

Open a new tab (or run: source ~/.zshrc) to use csessions, tabname and the orange Claude tab.
EOF
