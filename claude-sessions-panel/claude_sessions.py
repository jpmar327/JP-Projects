#!/usr/bin/env python3
"""List Claude Code sessions that are not currently open, and reopen one in a new iTerm2 tab.

Used by the `csessions` shell command and the iTerm2 "Claude Sessions" toolbelt panel.

  claude_sessions.py list [--days N] [--json]   show closed sessions
  claude_sessions.py pick [--days N]            numbered list, type a number to open it
  claude_sessions.py open <session-id>          open that session in a new iTerm2 tab

Reads Claude Code's own bookkeeping files (not a documented API, so a Claude update may
change them):
  ~/.claude/projects/<folder>/<session-id>.jsonl   one file per conversation
  ~/.claude/sessions/<pid>.json                    one file per running Claude
"""
import argparse
import glob
import json
import os
import shlex
import shutil
import subprocess
import sys
import time

CLAUDE_DIR = os.path.expanduser("~/.claude")
DEFAULT_DAYS = 30


def open_sessions():
    """Running Claude sessions, keyed by session ID: pid, status (busy/waiting/idle), name, cwd."""
    running = {}
    for path in glob.glob(os.path.join(CLAUDE_DIR, "sessions", "*.json")):
        try:
            with open(path) as f:
                info = json.load(f)
            os.kill(int(info["pid"]), 0)  # raises if the process is gone
            running[info["sessionId"]] = {
                "pid": int(info["pid"]),
                "status": info.get("status") or "idle",
                "name": info.get("name"),
                "cwd": info.get("cwd"),
            }
        except (OSError, ValueError, KeyError):
            continue
    return running


def open_session_ids():
    """Session IDs of Claude processes that are still running."""
    return set(open_sessions())


_read_cache = {}  # path -> (mtime, result); lets a long-running caller (the panel) skip unchanged files


def read_session_cached(path, mtime):
    cached = _read_cache.get(path)
    if cached and cached[0] == mtime:
        return cached[1]
    result = read_session(path)
    _read_cache[path] = (mtime, result)
    return result


def read_session(path):
    """Pull the name, folder and first prompt out of one conversation file."""
    custom_title = ai_title = cwd = first_prompt = entrypoint = None
    with open(path, errors="replace") as f:
        for line in f:
            # Cheap string checks first so we only parse the lines we care about
            if '"custom-title"' in line or '"ai-title"' in line or (cwd is None and '"cwd"' in line) \
                    or (entrypoint is None and '"entrypoint"' in line) \
                    or (first_prompt is None and '"type":"user"' in line):
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                kind = entry.get("type")
                if kind == "custom-title":
                    custom_title = entry.get("customTitle") or custom_title
                elif kind == "ai-title":
                    ai_title = entry.get("aiTitle") or ai_title
                if entrypoint is None and entry.get("entrypoint"):
                    entrypoint = entry["entrypoint"]
                if cwd is None and entry.get("cwd"):
                    cwd = entry["cwd"]
                if first_prompt is None and kind == "user" and not entry.get("isMeta"):
                    content = (entry.get("message") or {}).get("content")
                    if isinstance(content, str) and not content.startswith("<"):
                        first_prompt = content.strip().splitlines()[0][:80] if content.strip() else None
    return custom_title or ai_title or first_prompt, cwd, entrypoint


def closed_sessions(days=DEFAULT_DAYS):
    """Closed sessions used in the last `days` days, newest first."""
    cutoff = time.time() - days * 86400
    running = open_session_ids()
    sessions = []
    for path in glob.glob(os.path.join(CLAUDE_DIR, "projects", "*", "*.jsonl")):
        mtime = os.path.getmtime(path)
        session_id = os.path.basename(path)[:-len(".jsonl")]
        if mtime < cutoff or session_id in running:
            continue
        name, cwd, entrypoint = read_session_cached(path, mtime)
        if not cwd or entrypoint == "sdk-cli":  # empty, or a one-off `claude -p` run
            continue
        sessions.append({"id": session_id, "name": name or "(unnamed)", "cwd": cwd, "last_used": mtime})
    sessions.sort(key=lambda s: s["last_used"], reverse=True)
    return sessions


def all_sessions(days=DEFAULT_DAYS):
    """Open sessions (with their status) followed by closed ones, for the panel.

    Each entry has a "status": busy, waiting or idle for open sessions, "closed" otherwise.
    """
    running = open_sessions()
    opened = []
    for session_id, info in running.items():
        matches = glob.glob(os.path.join(CLAUDE_DIR, "projects", "*", f"{session_id}.jsonl"))
        mtime = os.path.getmtime(matches[0]) if matches else time.time()
        title, cwd, _ = read_session_cached(matches[0], mtime) if matches else (None, None, None)
        opened.append({"id": session_id, "name": info["name"] or title or "(unnamed)",
                       "cwd": info["cwd"] or cwd or "", "last_used": mtime,
                       "status": info["status"], "pid": info["pid"]})
    order = {"busy": 0, "waiting": 1, "idle": 2}
    opened.sort(key=lambda s: (order.get(s["status"], 3), -s["last_used"]))
    closed = [dict(s, status="closed") for s in closed_sessions(days)]
    return opened + closed


def ago(ts):
    mins = int((time.time() - ts) / 60)
    if mins < 60:
        return f"{mins}m ago"
    if mins < 1440:
        return f"{mins // 60}h ago"
    return f"{mins // 1440}d ago"


def short_path(path):
    home = os.path.expanduser("~")
    return "~" + path[len(home):] if path.startswith(home) else path


def session_files(session_id):
    """The conversation file and its same-named folder (helper-agent work), if present."""
    matches = glob.glob(os.path.join(CLAUDE_DIR, "projects", "*", f"{session_id}.jsonl"))
    if not matches:
        return []
    folder = matches[0][:-len(".jsonl")]
    return [matches[0]] + ([folder] if os.path.isdir(folder) else [])


def reveal_session(session_id):
    """Show the session's file selected in Finder."""
    files = session_files(session_id)
    if not files:
        return False
    subprocess.run(["open", "-R", files[0]], check=False)
    return True


def trash_session(session_id):
    """Move a closed session's files into one folder in the Trash, with a note on where they came from.

    Refuses open sessions. Returns the Trash folder path, or None.
    """
    if session_id in open_session_ids():
        return None
    files = session_files(session_id)
    if not files:
        return None
    name, _, _ = read_session(files[0])
    safe = "".join(c if c.isalnum() or c in " -_." else "_" for c in (name or "unnamed"))[:60].strip()
    dest = os.path.expanduser(f"~/.Trash/Claude session - {safe} - {session_id[:8]}")
    if os.path.exists(dest):
        dest += time.strftime(" %Y%m%d-%H%M%S")
    os.makedirs(dest)
    original_dir = os.path.dirname(files[0])
    for path in files:
        shutil.move(path, dest)
        _read_cache.pop(path, None)
    with open(os.path.join(dest, "RESTORE.txt"), "w") as f:
        f.write(f"Claude Code session: {name}\nSession ID: {session_id}\n\n"
                f"To restore it, move the other items in this folder back to:\n{original_dir}\n\n"
                f"Then reopen it with:  claude --resume {session_id}\n")
    return dest


def find_session(session_id):
    for s in closed_sessions(days=36500):
        if s["id"] == session_id:
            return s
    return None


def open_in_new_tab(session):
    """Open a new iTerm2 tab in the session's folder and resume it."""
    command = f"cd {shlex.quote(session['cwd'])} && claude --resume {shlex.quote(session['id'])}"
    escaped = command.replace("\\", "\\\\").replace('"', '\\"')
    script = f'''
tell application "iTerm2"
  activate
  if (count of windows) = 0 then
    set w to (create window with default profile)
  else
    set w to current window
    tell w to create tab with default profile
  end if
  tell current session of w to write text "{escaped}"
end tell'''
    subprocess.run(["osascript", "-e", script], check=True, capture_output=True)


def print_list(sessions):
    if not sessions:
        print("No closed Claude sessions in that time range.")
        return
    for i, s in enumerate(sessions, 1):
        print(f"{i:>3}. {s['name'][:50]:<50}  {ago(s['last_used']):>8}  {short_path(s['cwd'])}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("list", "pick"):
        p = sub.add_parser(name)
        p.add_argument("--days", type=int, default=DEFAULT_DAYS)
        if name == "list":
            p.add_argument("--json", action="store_true")
    sub.add_parser("open").add_argument("session_id")
    args = parser.parse_args()

    if args.cmd == "list":
        sessions = closed_sessions(args.days)
        print(json.dumps(sessions) if args.json else "", end="" if args.json else "")
        if not args.json:
            print_list(sessions)
    elif args.cmd == "pick":
        sessions = closed_sessions(args.days)
        print_list(sessions)
        if not sessions:
            return
        choice = input("\nOpen which number? (Enter to cancel) ").strip()
        if not choice:
            return
        if not choice.isdigit() or not 1 <= int(choice) <= len(sessions):
            sys.exit(f"Not a number from the list: {choice}")
        open_in_new_tab(sessions[int(choice) - 1])
    elif args.cmd == "open":
        session = find_session(args.session_id)
        if not session:
            sys.exit(f"No closed session with id {args.session_id}")
        open_in_new_tab(session)


if __name__ == "__main__":
    main()
