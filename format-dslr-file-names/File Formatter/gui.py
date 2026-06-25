"""
gui.py — Film Formatter
Tkinter GUI. All business logic lives in core.py.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

from core import build_rename_plan, execute_plan, delete_source_folders


# ─────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────

DARK_BG      = "#1a1a1a"
PANEL_BG     = "#242424"
ACCENT       = "#d4a843"
ACCENT_DARK  = "#b8902e"
TEXT_MAIN    = "#e8e8e8"
TEXT_DIM     = "#888888"
TEXT_SUCCESS = "#7abf7a"
TEXT_ERROR   = "#d46b6b"
TEXT_WARN    = "#d4a843"
BORDER       = "#333333"
INPUT_BG     = "#2e2e2e"
BTN_DANGER   = "#8b2e2e"
BTN_DANGER_H = "#a83535"

_mac   = sys.platform == "darwin"
FONT_BODY  = ("SF Pro Text",    10) if _mac else ("Segoe UI", 10)
FONT_LABEL = ("SF Pro Text",     9) if _mac else ("Segoe UI",  9)
FONT_MONO  = ("SF Mono",         9) if _mac else ("Consolas",  9)
FONT_TITLE = ("SF Pro Display", 14, "bold") if _mac else ("Segoe UI", 14, "bold")
FONT_HEAD  = ("SF Pro Text",    11, "bold") if _mac else ("Segoe UI", 11, "bold")


# ─────────────────────────────────────────────
#  CUSTOM WIDGETS
# ─────────────────────────────────────────────

class FlatButton(tk.Label):
    """
    Styled flat button built from a Label so it looks identical on every OS.
    """

    def __init__(self, parent, text, command=None,
                 bg=ACCENT, fg=DARK_BG, hover_bg=ACCENT_DARK,
                 font=FONT_BODY, padx=16, pady=7, **kwargs):
        super().__init__(parent, text=text, bg=bg, fg=fg,
                         font=font, padx=padx, pady=pady,
                         cursor="hand2", **kwargs)
        self._bg       = bg
        self._hover_bg = hover_bg
        self._command  = command
        self.bind("<Enter>",    lambda _: self.config(bg=self._hover_bg))
        self.bind("<Leave>",    lambda _: self.config(bg=self._bg))
        self.bind("<Button-1>", lambda _: self._command() if self._command else None)

    def set_state(self, enabled: bool):
        if enabled:
            self.config(bg=self._bg, fg=DARK_BG, cursor="hand2")
            self.bind("<Button-1>",
                      lambda _: self._command() if self._command else None)
        else:
            self.config(bg="#444444", fg="#777777", cursor="")
            self.unbind("<Button-1>")

    def update_command(self, fn):
        self._command = fn
        self.bind("<Button-1>", lambda _: fn() if fn else None)


class SectionLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text.upper(),
                         bg=PANEL_BG if kwargs.pop("panel", False) else DARK_BG,
                         fg=TEXT_DIM, font=FONT_LABEL, anchor="w", **kwargs)


class Divider(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BORDER, height=1, **kwargs)


def _make_entry(parent, var, font=FONT_BODY) -> tk.Entry:
    return tk.Entry(
        parent, textvariable=var,
        bg=INPUT_BG, fg=TEXT_MAIN,
        insertbackground=TEXT_MAIN,
        relief="flat", font=font,
        bd=0, highlightthickness=1,
        highlightcolor=ACCENT,
        highlightbackground=BORDER,
    )


# ─────────────────────────────────────────────
#  MAIN APPLICATION WINDOW
# ─────────────────────────────────────────────

class FilmFormatterApp(tk.Tk):

    SUBFOLDER = "Formatted"

    # ── initialisation ────────────────────────

    def __init__(self):
        super().__init__()
        self.title("Film Formatter")
        self.configure(bg=DARK_BG)
        self.resizable(False, False)

        self._plan:        list[tuple[str, str]] = []
        self._source_dirs: list[str]             = []
        self._running      = False
        self._delete_bar   = None   # inline confirmation widget, if shown

        self._build_ui()
        self._center(820, 680)

    def _center(self, w: int, h: int):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI construction ───────────────────────

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self, bg=PANEL_BG, pady=14)
        top.pack(fill="x")
        tk.Label(top, text="⬛  Film Formatter",
                 bg=PANEL_BG, fg=TEXT_MAIN,
                 font=FONT_TITLE, padx=20).pack(side="left")
        tk.Label(top, text="DSLR SD Card Organizer",
                 bg=PANEL_BG, fg=TEXT_DIM,
                 font=FONT_LABEL).pack(side="left", pady=3)

        Divider(self).pack(fill="x")

        # Body
        body = tk.Frame(self, bg=DARK_BG)
        body.pack(fill="both", expand=True, padx=24, pady=18)

        left = tk.Frame(body, bg=DARK_BG, width=340)
        left.pack(side="left", fill="y", padx=(0, 18))
        left.pack_propagate(False)
        self._build_inputs(left)

        right = tk.Frame(body, bg=DARK_BG)
        right.pack(side="left", fill="both", expand=True)
        self._build_log(right)

        # Bottom status bar
        Divider(self).pack(fill="x")
        self._build_statusbar()

    def _build_inputs(self, parent):
        # Source folder
        SectionLabel(parent, "Source Folder").pack(anchor="w", pady=(0, 4))
        row = tk.Frame(parent, bg=DARK_BG)
        row.pack(fill="x", pady=(0, 14))

        self._folder_var = tk.StringVar()
        e = _make_entry(row, self._folder_var, font=FONT_MONO)
        e.pack(side="left", fill="x", expand=True, ipady=6, ipadx=6)
        FlatButton(row, "Browse", command=self._browse,
                   padx=10, pady=6).pack(side="left", padx=(6, 0))

        # Prefix
        SectionLabel(parent, "File Prefix").pack(anchor="w", pady=(0, 4))
        self._prefix_var = tk.StringVar(value="JP_Film")
        e2 = _make_entry(parent, self._prefix_var)
        e2.pack(fill="x", ipady=6, ipadx=6, pady=(0, 14))

        # Month / Year
        now = datetime.now()
        date_row = tk.Frame(parent, bg=DARK_BG)
        date_row.pack(fill="x", pady=(0, 14))

        for label, var_default, attr in [
            ("Month", str(now.month), "_month_var"),
            ("Year",  str(now.year),  "_year_var"),
        ]:
            col = tk.Frame(date_row, bg=DARK_BG)
            col.pack(side="left", fill="x", expand=True,
                     padx=(0, 8) if label == "Month" else (0, 0))
            SectionLabel(col, label).pack(anchor="w", pady=(0, 4))
            setattr(self, attr, tk.StringVar(value=var_default))
            e = _make_entry(col, getattr(self, attr))
            e.pack(fill="x", ipady=6, ipadx=6)

        # Delete originals toggle
        Divider(parent).pack(fill="x", pady=(4, 14))
        SectionLabel(parent, "After Formatting").pack(anchor="w", pady=(0, 8))

        self._delete_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            parent,
            text="Offer to delete original source folders",
            variable=self._delete_var,
            bg=DARK_BG, fg=TEXT_MAIN,
            selectcolor=INPUT_BG,
            activebackground=DARK_BG,
            activeforeground=TEXT_MAIN,
            font=FONT_BODY, anchor="w", cursor="hand2",
        ).pack(anchor="w")

        tk.Label(
            parent,
            text="If enabled, you will be asked to confirm\nbefore anything is deleted.",
            bg=DARK_BG, fg=TEXT_DIM, font=FONT_LABEL,
            justify="left", anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        # Spacer + Run button
        tk.Frame(parent, bg=DARK_BG).pack(fill="y", expand=True)
        self._run_btn = FlatButton(
            parent, "▶  Run Formatter",
            command=self._start_format,
            font=FONT_HEAD, padx=0, pady=10,
        )
        self._run_btn.pack(fill="x", pady=(12, 0))

    def _build_log(self, parent):
        SectionLabel(parent, "Activity Log").pack(anchor="w", pady=(0, 6))

        frame = tk.Frame(parent, bg=INPUT_BG,
                         highlightthickness=1,
                         highlightbackground=BORDER)
        frame.pack(fill="both", expand=True)

        self._log = tk.Text(
            frame, bg=INPUT_BG, fg=TEXT_MAIN,
            font=FONT_MONO, relief="flat",
            state="disabled", wrap="none",
            insertbackground=TEXT_MAIN,
            selectbackground=ACCENT,
            selectforeground=DARK_BG,
            bd=0, padx=10, pady=8,
        )
        self._log.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical",
                           command=self._log.yview)
        sb.pack(side="right", fill="y")
        self._log.configure(yscrollcommand=sb.set)

        self._log.tag_config("ok",   foreground=TEXT_SUCCESS)
        self._log.tag_config("err",  foreground=TEXT_ERROR)
        self._log.tag_config("warn", foreground=TEXT_WARN)
        self._log.tag_config("dim",  foreground=TEXT_DIM)
        self._log.tag_config(
            "head",
            foreground=ACCENT,
            font=(*FONT_MONO[:1], FONT_MONO[1], "bold"),
        )

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=PANEL_BG, pady=10)
        bar.pack(fill="x")

        self._status_var = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self._status_var,
                 bg=PANEL_BG, fg=TEXT_DIM,
                 font=FONT_LABEL, padx=20).pack(side="left")

        self._progress = ttk.Progressbar(bar, length=200, mode="determinate")
        self._progress.pack(side="right", padx=20)

    # ── helpers ───────────────────────────────

    def _browse(self):
        path = filedialog.askdirectory(title="Select SD card / source folder")
        if path:
            self._folder_var.set(path)

    def _log_write(self, msg: str, tag: str = ""):
        self._log.configure(state="normal")
        self._log.insert("end", msg + "\n", tag)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _log_clear(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

    def _set_status(self, msg: str):
        self._status_var.set(msg)

    def _set_progress(self, i: int, n: int):
        self._progress["maximum"] = n
        self._progress["value"]   = i

    def _ui(self, fn, *args):
        """Thread-safe: schedule fn(*args) on the main thread."""
        self.after(0, lambda: fn(*args))

    # ── validation ────────────────────────────

    def _validate(self) -> tuple[bool, str]:
        folder = self._folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            return False, "Source folder does not exist or was not selected."
        if not self._prefix_var.get().strip():
            return False, "File prefix cannot be empty."
        month = self._month_var.get().strip()
        if not month.isdigit() or not (1 <= int(month) <= 12):
            return False, "Month must be a number between 1 and 12."
        year = self._year_var.get().strip()
        if not year.isdigit() or len(year) != 4:
            return False, "Year must be a 4-digit number."
        return True, ""

    # ── format flow ───────────────────────────

    def _start_format(self):
        ok, err = self._validate()
        if not ok:
            messagebox.showerror("Input Error", err)
            return

        self._log_clear()
        self._run_btn.set_state(False)
        self._set_progress(0, 1)
        self._running = True
        threading.Thread(target=self._run_format, daemon=True).start()

    def _run_format(self):
        folder = self._folder_var.get().strip()
        prefix = self._prefix_var.get().strip()
        month  = self._month_var.get().strip()
        year   = self._year_var.get().strip()

        try:
            self._ui(self._set_status, "Building file plan…")
            self._ui(self._log_write, "─" * 52, "dim")
            self._ui(self._log_write, f"  Source : {folder}", "dim")
            self._ui(self._log_write,
                     f"  Prefix : {prefix}_{month}_{year}_XXXXX", "dim")
            self._ui(self._log_write,
                     f"  Output : {self.SUBFOLDER}/", "dim")
            self._ui(self._log_write, "─" * 52, "dim")

            plan = build_rename_plan(
                folder, self.SUBFOLDER, prefix, month, year
            )

            if not plan:
                self._ui(self._log_write,
                         "No files found in source subfolders.", "warn")
                self._ui(self._set_status, "Nothing to do.")
                self._ui(self._run_btn.set_state, True)
                return

            self._ui(self._log_write,
                     f"{len(plan)} file(s) to copy:\n", "head")

            source_dirs = execute_plan(
                plan,
                log_fn=lambda m: self._ui(
                    self._log_write, f"  {m}", "ok"),
                progress_fn=lambda i, n: (
                    self._ui(self._set_progress, i, n),
                    self._ui(self._set_status, f"Copying {i} / {n}…"),
                ),
            )
            self._source_dirs = source_dirs

            self._ui(self._log_write, "")
            self._ui(self._log_write,
                     f"✓  Done — {len(plan)} file(s) copied.", "ok")
            self._ui(self._log_write,
                     f"   Output: {os.path.join(folder, self.SUBFOLDER)}",
                     "dim")
            self._ui(self._set_status, "Formatting complete.")

            if self._delete_var.get():
                self._ui(self._offer_delete)
            else:
                self._ui(self._run_btn.set_state, True)

        except Exception as exc:
            self._ui(self._log_write, f"\n✗  Error: {exc}", "err")
            self._ui(self._set_status, "Error — see log.")
            self._ui(self._run_btn.set_state, True)

        finally:
            self._running = False

    # ── deletion confirmation flow ────────────

    def _offer_delete(self):
        """
        Shown on the main thread after formatting completes.
        Renders an inline warning bar with Yes / No buttons.
        """
        self._log_write("", "")
        self._log_write("─" * 52, "dim")
        self._log_write("  PENDING: Delete original source folders?", "warn")
        self._log_write("  The following folders would be removed:", "dim")
        for d in self._source_dirs:
            self._log_write(f"    {d}", "warn")
        self._log_write("─" * 52, "dim")
        self._log_write("", "")
        self._set_status("Waiting — confirm deletion decision below.")

        self._delete_bar = tk.Frame(
            self, bg="#3a1a1a",
            highlightthickness=1,
            highlightbackground=BTN_DANGER,
        )
        self._delete_bar.pack(fill="x", padx=24, pady=(0, 8))

        inner = tk.Frame(self._delete_bar, bg="#3a1a1a")
        inner.pack(padx=14, pady=10)

        tk.Label(
            inner,
            text=(
                f"⚠  Delete {len(self._source_dirs)} source folder(s)?"
                "  This cannot be undone."
            ),
            bg="#3a1a1a", fg=TEXT_WARN, font=FONT_BODY,
        ).pack(side="left", padx=(0, 16))

        FlatButton(
            inner, "Yes, delete folders",
            command=self._on_delete_yes,
            bg=BTN_DANGER, hover_bg=BTN_DANGER_H,
            fg=TEXT_MAIN, padx=12, pady=5,
        ).pack(side="left", padx=(0, 8))

        FlatButton(
            inner, "No, keep originals",
            command=self._on_delete_no,
            bg="#333333", hover_bg="#444444",
            fg=TEXT_MAIN, padx=12, pady=5,
        ).pack(side="left")

    def _dismiss_delete_bar(self):
        if self._delete_bar:
            self._delete_bar.destroy()
            self._delete_bar = None

    def _on_delete_yes(self):
        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete "
            f"{len(self._source_dirs)} source folder(s) "
            f"and all their contents?\n\nThis cannot be undone.",
            icon="warning",
        )
        self._dismiss_delete_bar()

        if confirmed:
            self._log_write("Deleting source folders…", "warn")
            self._set_status("Deleting source folders…")
            try:
                delete_source_folders(
                    self._source_dirs,
                    log_fn=lambda m: self._log_write(f"  {m}", "err"),
                )
                self._log_write(
                    f"\n✓  {len(self._source_dirs)} source folder(s) deleted.",
                    "ok",
                )
                self._set_status("Done — source folders deleted.")
            except Exception as exc:
                self._log_write(f"✗  Deletion error: {exc}", "err")
                self._set_status("Deletion error — see log.")
        else:
            self._log_write("Deletion cancelled — originals kept.", "ok")
            self._set_status("Done — originals kept.")

        self._run_btn.set_state(True)

    def _on_delete_no(self):
        confirmed = messagebox.askyesno(
            "Keep Originals",
            "Keep all original source folders?\n\n"
            "Your formatted files are already safely copied "
            "to the output folder.",
            icon="question",
        )
        self._dismiss_delete_bar()

        if confirmed:
            self._log_write("Originals kept — no files deleted.", "ok")
            self._set_status("Done — originals kept.")
            self._run_btn.set_state(True)
        else:
            # They said "no" to keeping — re-offer the delete prompt
            self._offer_delete()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    app = FilmFormatterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
