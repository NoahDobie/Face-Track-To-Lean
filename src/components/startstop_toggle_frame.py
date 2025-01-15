import tkinter as tk
import ttkbootstrap as ttkb

def create_startstop_toggle_frame(root, controller):
    frame = ttkb.Frame(root)
    frame.pack(side=tk.TOP, pady=5)

    toggle_button = ttkb.Button(frame, text="Start", command=controller.toggle_tracking, bootstyle="success", width=30, takefocus=False)
    toggle_button.pack(side=tk.TOP, pady=10, padx=5, ipady=5)

    return frame, toggle_button