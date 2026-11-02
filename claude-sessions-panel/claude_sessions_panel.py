#!/usr/bin/env python3
"""iTerm2 toolbelt panel: "Claude Sessions".

Lists Claude Code sessions (via the shared script in ~/.config/claude-sessions/claude_sessions.py)
and refreshes live. Open sessions show a status dot (busy = Claude spinner, waiting = amber,
idle = green); closed ones show a grey dot. Clicking an open session jumps to its tab; clicking a
closed one opens it in a new tab with `claude --resume <id>` in the session's folder.

Show it with View > Toolbelt > Claude Sessions.
"""
import asyncio
import json
import os
import secrets
import shlex
import subprocess
import sys
import time
from urllib.parse import parse_qs, urlparse

import iterm2

sys.path.insert(0, os.path.expanduser("~/.config/claude-sessions"))
import claude_sessions  # noqa: E402  (shared with the `csessions` shell command)

PORT = 58731
DAYS = 30
TOKEN = secrets.token_urlsafe(16)  # only this panel's page knows it, so other pages can't open tabs

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  :root { color-scheme: light dark; --bg:#fafafa; --fg:#1d1d1f; --dim:#6e6e73; --row:#ececec; --line:#d9d9d9;
          --busy:#d97757; --waiting:#e5a50a; --idle:#3fb950; --closed:#8b8b8b; }
  @media (prefers-color-scheme: dark) { :root { --bg:#1e1e1e; --fg:#e8e8e8; --dim:#9a9a9a; --row:#2c2c2c; --line:#333; } }
  body { margin:0; background:var(--bg); color:var(--fg); font:11px Monaco, "SF Mono", Menlo, monospace; }  /* same as the terminal */
  input, select, button { font:inherit; }
  header { position:sticky; top:0; background:var(--bg); padding:6px; border-bottom:1px solid var(--line); display:flex; gap:6px; z-index:1; }
  #dir { padding:2px 7px; border:1px solid var(--line); border-radius:5px; background:transparent; color:var(--fg); cursor:pointer; }
  select { padding:3px 4px; border:1px solid var(--line); border-radius:5px; background:transparent; color:var(--fg); }
  input { flex:1; padding:4px 6px; border:1px solid var(--line); border-radius:5px; background:transparent; color:var(--fg); }
  nav { position:sticky; top:35px; background:var(--bg); display:flex; flex-wrap:wrap; gap:4px; padding:5px 6px; border-bottom:1px solid var(--line); z-index:1; }
  nav button { padding:2px 7px; border:1px solid var(--line); border-radius:10px; background:transparent; color:var(--dim); cursor:pointer; }
  nav button.on { background:var(--fg); color:var(--bg); border-color:var(--fg); }
  nav .c { opacity:.7; margin-left:3px; }
  h2 { margin:0; padding:8px 8px 4px; font-size:10px; letter-spacing:.04em; text-transform:uppercase; color:var(--dim); }
  .s { display:flex; gap:7px; padding:6px 8px; border-bottom:1px solid var(--line); cursor:pointer; }
  .s:hover { background:var(--row); }
  .dot { font-size:12px; width:1.1em; text-align:center; line-height:16px; flex:none; }
  .busy { color:var(--busy); } .idle { color:var(--idle); } .closed { color:var(--closed); opacity:.55; }
  .waiting { color:var(--waiting); animation:pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 50% { opacity:.35; } }
  .t { min-width:0; flex:1; }
  .n { font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .m { color:var(--dim); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:2px; }
  .empty { color:var(--dim); padding:10px 8px; }
</style></head><body>
<header><input id="q" placeholder="Filter…" oninput="render()"><select id="sort" title="Sort by" onchange="changeSort()"><option value="time">Recent</option><option value="name">Name</option><option value="path">Folder</option><option value="status">Status</option></select><button id="dir" onclick="flipOrder()">↓</button></header>
<nav id="chips"></nav>
<div id="list"><div class="empty">Loading…</div></div>
<script>
  const TOKEN = '__TOKEN__';
  const SPIN = ['·','✢','✳','✶','✻','✽','✻','✶','✳','✢'];
  const LABEL = {busy:'working', waiting:'waiting for you', idle:'idle', closed:'closed'};
  let sessions = [], last = '';
  const SORTS = {
    time: (a, b) => b.last_used - a.last_used,
    name: (a, b) => a.name.localeCompare(b.name, undefined, {sensitivity:'base', numeric:true}),
    path: (a, b) => a.path.localeCompare(b.path) || b.last_used - a.last_used,
    status: (a, b) => RANK[a.status] - RANK[b.status] || b.last_used - a.last_used,
  };
  const RANK = {busy:0, waiting:1, idle:2, closed:3};
  const FILTERS = [['all','All', s => true], ['open','Open', s => s.status !== 'closed'], ['busy','Working', s => s.status === 'busy'],
                   ['waiting','Waiting', s => s.status === 'waiting'], ['idle','Idle', s => s.status === 'idle'], ['closed','Closed', s => s.status === 'closed']];
  let filter = 'all';
  try { filter = localStorage.getItem('filter') || 'all'; } catch (e) {}
  function setFilter(f) { filter = f; try { localStorage.setItem('filter', f); } catch (e) {} render(); }
  try { document.getElementById('sort').value = localStorage.getItem('sort') || 'time'; } catch (e) {}
  const DIR_LABEL = {time:['newest first','oldest first'], name:['A → Z','Z → A'], path:['A → Z','Z → A'], status:['working first','closed first']};
  // Not named `dir`: inside onclick="..." that name resolves to the element's own text-direction property
  let sortOrder = 1;  // 1 = normal order, -1 = reversed
  try { sortOrder = Number(localStorage.getItem('dir')) === -1 ? -1 : 1; } catch (e) {}
  function saveSort() { try { localStorage.setItem('sort', document.getElementById('sort').value); localStorage.setItem('dir', sortOrder); } catch (e) {} }
  function flipOrder() { sortOrder = -sortOrder; saveSort(); render(); }
  function changeSort() { sortOrder = 1; saveSort(); render(); }

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const row = s => `<div class="s" data-id="${esc(s.id)}" title="${esc(s.cwd)}">
      <span class="dot ${s.status}" title="${LABEL[s.status] || s.status}">${s.status === 'busy' ? SPIN[0] : '●'}</span>
      <div class="t"><div class="n">${esc(s.name)}</div><div class="m">${esc(s.ago)} · ${esc(s.path)}</div></div></div>`;

  function render() {
    const q = document.getElementById('q').value.toLowerCase();
    const byStatus = (FILTERS.find(f => f[0] === filter) || FILTERS[0])[2];
    document.getElementById('chips').innerHTML = FILTERS.map(([key, label, test]) =>
      `<button class="${key === filter ? 'on' : ''}" onclick="setFilter('${key}')">${label}<span class="c">${sessions.filter(test).length}</span></button>`).join('');
    const key = document.getElementById('sort').value, btn = document.getElementById('dir');
    const unnamedLast = (a, b) => key === 'name' ? (a.name === '(unnamed)') - (b.name === '(unnamed)') : 0;  // in either direction
    const shown = sessions.filter(byStatus).filter(s => !q || (s.name + ' ' + s.path).toLowerCase().includes(q))
                          .sort((a, b) => unnamedLast(a, b) || sortOrder * (SORTS[key] || SORTS.time)(a, b));
    btn.textContent = sortOrder === 1 ? '↓' : '↑';
    btn.title = 'Order: ' + (DIR_LABEL[key] || DIR_LABEL.time)[sortOrder === 1 ? 0 : 1] + ' (click to flip)';
    const open = shown.filter(s => s.status !== 'closed'), closed = shown.filter(s => s.status === 'closed');
    let out = '';
    const groups = [['Open', open], ['Recent', closed]];
    if (key === 'status' && sortOrder === -1) groups.reverse();  // "closed first" puts Recent on top
    for (const [title, list] of groups) if (list.length) out += `<h2>${title}</h2>` + list.map(row).join('');
    document.getElementById('list').innerHTML = out || '<div class="empty">No sessions match.</div>';
  }

  async function refresh() {
    if (document.hidden) return;  // panel not visible: skip the work
    try {
      const text = await (await fetch('/data', {cache:'no-store'})).text();
      if (text !== last) { last = text; sessions = JSON.parse(text); render(); }  // only redraw on change
    } catch (e) {}
  }

  document.getElementById('list').addEventListener('click', async e => {
    const el = e.target.closest('.s'); if (!el) return;
    el.style.opacity = .4;
    await fetch('/open?token=' + TOKEN + '&id=' + encodeURIComponent(el.dataset.id));
    setTimeout(() => { el.style.opacity = ''; refresh(); }, 1200);
  });

  let frame = 0;
  setInterval(() => {  // Claude-style spinner on busy sessions
    frame = (frame + 1) % SPIN.length;
    document.querySelectorAll('.dot.busy').forEach(d => d.textContent = SPIN[frame]);
  }, 120);
  setInterval(refresh, 2000);
  document.addEventListener('visibilitychange', refresh);
  refresh();
</script></body></html>"""


def session_data():
    return json.dumps([
        {"id": s["id"], "name": s["name"], "status": s["status"], "cwd": s["cwd"],
         "path": claude_sessions.short_path(s["cwd"]), "ago": claude_sessions.ago(s["last_used"]),
         "last_used": s["last_used"]}
        for s in claude_sessions.all_sessions(DAYS)
    ])


async def focus_running_session(connection, pid):
    """Bring the tab that runs this Claude process to the front. Returns False if not found."""
    tty = subprocess.run(["ps", "-o", "tty=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    if not tty or tty == "??":
        return False
    app = await iterm2.async_get_app(connection)
    for window in app.terminal_windows:
        for tab in window.tabs:
            for session in tab.sessions:
                if await session.async_get_variable("tty") == f"/dev/{tty}":
                    await session.async_activate(select_tab=True, order_window_front=True)
                    await app.async_activate()
                    return True
    return False


async def open_in_new_tab(connection, session):
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window
    if window is None:
        window = await iterm2.Window.async_create(connection)
        tab = window.current_tab
    else:
        tab = await window.async_create_tab()
    command = f"cd {shlex.quote(session['cwd'])} && claude --resume {shlex.quote(session['id'])}"
    await tab.current_session.async_send_text(command + "\n")
    await app.async_activate()


async def open_or_focus(connection, session_id):
    running = claude_sessions.open_sessions().get(session_id)
    if running:
        return await focus_running_session(connection, running["pid"])
    session = claude_sessions.find_session(session_id)
    if not session:
        return False
    await open_in_new_tab(connection, session)
    return True


def respond(writer, status, body, content_type="text/html; charset=utf-8"):
    data = body.encode()
    writer.write(f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(data)}\r\n"
                 f"Cache-Control: no-store\r\nConnection: close\r\n\r\n".encode() + data)


async def handle(connection, reader, writer):
    try:
        request_line = (await reader.readline()).decode(errors="replace")
        while (await reader.readline()) not in (b"\r\n", b"\n", b""):
            pass  # skip headers
        parts = request_line.split()
        url = urlparse(parts[1] if len(parts) > 1 else "/")
        query = parse_qs(url.query)
        if url.path == "/data":
            respond(writer, "200 OK", session_data(), "application/json")
        elif url.path == "/open":
            session_id = (query.get("id") or [""])[0]
            ok = query.get("token") == [TOKEN] and await open_or_focus(connection, session_id)
            respond(writer, "200 OK" if ok else "403 Forbidden", json.dumps({"ok": bool(ok)}), "application/json")
        else:
            respond(writer, "200 OK", PAGE.replace("__TOKEN__", TOKEN))
        await writer.drain()
    finally:
        writer.close()


async def main(connection):
    server = await asyncio.start_server(lambda r, w: handle(connection, r, w), "127.0.0.1", PORT)
    await iterm2.tool.async_register_web_view_tool(
        connection,
        "Claude Sessions",
        "com.claude-sessions.panel",
        False,
        f"http://127.0.0.1:{PORT}/?t={int(time.time())}",
    )
    async with server:
        await server.serve_forever()


iterm2.run_forever(main)
