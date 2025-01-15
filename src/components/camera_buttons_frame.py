import tkinter as tk
import ttkbootstrap as ttkb

def create_camera_buttons_frame(root, controller):
    camera_buttons_frame = ttkb.Frame(root)
    camera_buttons_frame.pack(side=tk.TOP, pady=5)

    toggle_preview_button = ttkb.Button(camera_buttons_frame, text="Toggle Preview", command=controller.toggle_preview, bootstyle="info", width=20, takefocus=False)
    toggle_preview_button.pack(side=tk.LEFT, padx=5)

    flip_camera_button = ttkb.Button(camera_buttons_frame, text="Flip Camera", command=controller.flip_camera, bootstyle="warning", width=20, takefocus=False)
    flip_camera_button.pack(side=tk.LEFT, padx=5)

    return camera_buttons_frame