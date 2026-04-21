import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import datetime
from move_cursor import create_move_list
import pyautogui
import time

# Global variables
jiggler_thread = None
stop_event = threading.Event()


def run_jiggler(interval, move_count, cursor_move_duration):
    """Run the jiggler in a separate thread"""
    stop_event.clear()

    try:
        while not stop_event.is_set():
            move_list = create_move_list(move_count)
            log(f'\n{str(datetime.datetime.now())}\n{move_list}\n')

            # FORWARD PATHING
            for move_xy in move_list:
                if stop_event.is_set():
                    break
                pyautogui.moveRel(move_xy[0], move_xy[1], cursor_move_duration)

            # BACKWARD PATHING
            for move_xy in move_list:
                if stop_event.is_set():
                    break
                pyautogui.moveRel(-move_xy[0], -move_xy[1], cursor_move_duration)

            # Wait for interval
            for _ in range(int(interval * 10)):
                if stop_event.is_set():
                    break
                time.sleep(0.1)

    except Exception as e:
        log(f'\nError: {str(e)}\n')
    finally:
        # Re-enable Start button when thread ends
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)


def log(message):
    """Append message to the output box (thread-safe)"""
    output_box.config(state=tk.NORMAL)
    output_box.insert(tk.END, message)
    output_box.see(tk.END)
    output_box.config(state=tk.DISABLED)


def on_start():
    global jiggler_thread
    try:
        interval = float(interval_var.get())
        move_count = int(movecount_var.get())
        duration = float(duration_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")
        return

    log("Mouse jiggler started. Press Stop to stop.\n")
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    jiggler_thread = threading.Thread(
        target=run_jiggler,
        args=(interval, move_count, duration),
        daemon=True
    )
    jiggler_thread.start()


def on_stop():
    stop_event.set()
    log("\nStopped by user.\n")
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)


def on_exit():
    if jiggler_thread and jiggler_thread.is_alive():
        stop_event.set()
        jiggler_thread.join()
    root.destroy()


# --- Build the window ---
root = tk.Tk()
root.title("Mouse Wiggler GUI")
root.resizable(False, False)

# Title
tk.Label(root, text="Mouse Wiggler Control Panel", font=("Arial", 16, "bold")).grid(
    row=0, column=0, columnspan=2, pady=(12, 8), padx=16
)

# Interval
tk.Label(root, text="Interval (seconds):", anchor="w").grid(row=1, column=0, sticky="w", padx=16)
interval_var = tk.StringVar(value="60")
tk.Entry(root, textvariable=interval_var, width=15).grid(row=1, column=1, padx=16, pady=2)

# Move Count
tk.Label(root, text="Move Count:", anchor="w").grid(row=2, column=0, sticky="w", padx=16)
movecount_var = tk.StringVar(value="15")
tk.Entry(root, textvariable=movecount_var, width=15).grid(row=2, column=1, padx=16, pady=2)

# Duration
tk.Label(root, text="Cursor Move Duration (sec):", anchor="w").grid(row=3, column=0, sticky="w", padx=16)
duration_var = tk.StringVar(value="0.005")
tk.Entry(root, textvariable=duration_var, width=15).grid(row=3, column=1, padx=16, pady=2)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

start_btn = tk.Button(btn_frame, text="Start", width=10, bg="green", fg="white", command=on_start)
start_btn.pack(side=tk.LEFT, padx=6)

stop_btn = tk.Button(btn_frame, text="Stop", width=10, bg="red", fg="white", command=on_stop, state=tk.DISABLED)
stop_btn.pack(side=tk.LEFT, padx=6)

exit_btn = tk.Button(btn_frame, text="Exit", width=10, command=on_exit)
exit_btn.pack(side=tk.LEFT, padx=6)

# Output box
output_box = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED, wrap=tk.WORD)
output_box.grid(row=5, column=0, columnspan=2, padx=16, pady=(0, 16))

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()