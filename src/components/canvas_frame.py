import tkinter as tk

def create_canvas_frame(root, controller):
    display_width = controller.config["camera_preview_width"]
    display_height = controller.config["camera_preview_height"]

    canvas = tk.Canvas(root, width=display_width, height=display_height, bg="black")
    canvas.pack(side=tk.TOP, pady=5)

    # Show loading screen in the camera preview spot
    loading_label = canvas.create_text(display_width // 2, display_height // 2, text="Loading Camera...", font=("Open Sans Regular", 16), fill="white")

    return canvas, loading_label