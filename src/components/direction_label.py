import tkinter as tk
import ttkbootstrap as ttkb

def create_direction_label(root):
    direction_label = ttkb.Label(root, text="Direction", bootstyle="dark", foreground="white", font=("Open Sans", 16))
    direction_label.pack(side=tk.TOP, pady=5)

    return direction_label