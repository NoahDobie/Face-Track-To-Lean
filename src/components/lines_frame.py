import tkinter as tk
import ttkbootstrap as ttkb

def create_lines_frame(root, controller):
    lines_frame = ttkb.Frame(root)
    lines_frame.pack(side=tk.TOP, pady=5)

    ttkb.Label(lines_frame, text="Left Line Position:", bootstyle="dark", foreground="white").grid(row=0, column=0, padx=(10,0))
    left_line_slider = ttkb.Scale(lines_frame, from_=0, to=controller.config["camera_preview_width"], orient=tk.HORIZONTAL, command=controller.update_left_line_position, bootstyle="success")
    left_line_slider.set(controller.config["left_line_position"])  # Load from config
    left_line_slider.grid(row=0, column=1, padx=5)

    ttkb.Label(lines_frame, text="Right Line Position:", bootstyle="dark", foreground="white").grid(row=0, column=3, padx=(5,0))
    right_line_slider = ttkb.Scale(lines_frame, from_=0, to=controller.config["camera_preview_width"], orient=tk.HORIZONTAL, command=controller.update_right_line_position, bootstyle="danger")
    right_line_slider.set(controller.config["right_line_position"])  # Load from config
    right_line_slider.grid(row=0, column=4, padx=(5,10))

    return lines_frame, left_line_slider, right_line_slider