# Claude Sessions shell helpers. Loaded from ~/.zshrc by install.sh.
#
#   csessions [--days N]   list closed Claude sessions; type a number to reopen it in a new iTerm2 tab
#   tabname <name>         name this tab; `tabname` alone clears it
#   claude                 tab turns orange while Claude runs, and gets its color and name back on exit

csessions() { python3 -I ~/.config/claude-sessions/claude_sessions.py pick "$@"; }

tabname() {
  if [[ -z "$1" ]]; then unset TAB_NAME; printf "\e]0;\a"
  else export TAB_NAME="$*"; printf "\e]0;%s\a" "$TAB_NAME"; fi
}

claude() {
  local saved_name="$TAB_NAME"
  printf "\e]6;1;bg;red;brightness;125\a\e]6;1;bg;green;brightness;65\a\e]6;1;bg;blue;brightness;20\a"
  command claude "$@"
  local rc=$?
  printf "\e]6;1;bg;*;default\a"
  if [[ -n "$saved_name" ]]; then tabname "$saved_name"; else tabname; fi
  return $rc
}
