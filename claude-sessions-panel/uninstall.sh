#!/bin/zsh
# Removes everything install.sh added. Your Claude sessions themselves are not touched.

pkill -f claude_sessions_panel.py 2>/dev/null && echo "Stopped the panel"
rm -f "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch/claude_sessions_panel.py"
rm -rf "$HOME/.config/claude-sessions"
if grep -qF "# Claude Sessions" "$HOME/.zshrc" 2>/dev/null; then
  cp "$HOME/.zshrc" "$HOME/.zshrc.bak-$(date +%Y%m%d-%H%M%S)"
  grep -vF "# Claude Sessions" "$HOME/.zshrc" > "$HOME/.zshrc.tmp" && mv "$HOME/.zshrc.tmp" "$HOME/.zshrc"
  echo "Removed the line from ~/.zshrc (backup saved next to it)"
fi
echo "Uninstalled. Open a new tab, and hide the panel with View > Toolbelt > Claude Sessions."
