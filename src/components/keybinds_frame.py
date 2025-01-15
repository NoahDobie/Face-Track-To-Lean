import tkinter as tk
import ttkbootstrap as ttkb

def create_keybind_field(frame, row, label_text, key_var, set_command, pady):
    ttkb.Label(frame, text=label_text, bootstyle="dark", foreground="white", anchor="e").grid(row=row, column=0, sticky="e", padx=(0, 5))
    ttkb.Entry(frame, textvariable=key_var, width=5, bootstyle="dark", justify="center").grid(row=row, column=1)
    ttkb.Button(frame, text="Set", command=set_command, bootstyle="primary", takefocus=False).grid(row=row, column=2, pady=(0, pady), padx=(5, 0))

def create_keybinds_frame(root, controller):
    keybinds_frame = ttkb.Frame(root, borderwidth=1, relief="solid", padding=8)
    keybinds_frame.pack(side=tk.TOP, pady=10)

    left_key_var = tk.StringVar(value=controller.config["left_key"])  # Load from config
    right_key_var = tk.StringVar(value=controller.config["right_key"])  # Load from config
    start_stop_key_var = tk.StringVar(value=controller.config["start_stop_key"])  # Load from config

    create_keybind_field(keybinds_frame, 0, "Left Lean", left_key_var, controller.set_left_keybind, 2)
    create_keybind_field(keybinds_frame, 1, "Right Lean", right_key_var, controller.set_right_keybind, 2)
    create_keybind_field(keybinds_frame, 2, "Start/Stop Toggle", start_stop_key_var, controller.set_start_stop_keybind, 0)

    return keybinds_frame, left_key_var, right_key_var, start_stop_key_var