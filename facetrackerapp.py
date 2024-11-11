import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from pynput.keyboard import Controller, Key
import cv2
from facetracker import FaceTracker
from configmanager import ConfigManager

class FaceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lean Tracking by Noah Dobie")

        self.tracking_enabled = False
        self.preview_enabled = True
        self.running = True
        self.current_direction = "Center"
        self.keyboard = Controller()

        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()

        self.setup_ui()
        self.load_config()

        # Initialize camera in a separate thread
        self.init_thread = threading.Thread(target=self.initialize_camera)
        self.init_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(10, self.main_loop)

        # Bind the start/stop key
        self.root.bind(f'<KeyPress-{self.start_stop_key_var.get()}>', self.toggle_tracking)

    def setup_ui(self):
        self.root.minsize(400, 300)  # Set minimum window size
        self.root.resizable(True, True)  # Allow window to be resized

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, pady=5)

        self.toggle_button = tk.Button(self.button_frame, text="Start", command=self.toggle_tracking, height=2, width=20, bg="green", font=("Helvetica", 14))
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Select Camera:").pack(side=tk.TOP, pady=5)
        self.camera_var = tk.StringVar()
        self.camera_dropdown = ttk.Combobox(self.root, textvariable=self.camera_var)
        self.camera_dropdown.pack(side=tk.TOP, pady=5)
        self.camera_dropdown['values'] = self.list_cameras()
        self.camera_dropdown.current(0)

        self.toggle_preview_button = tk.Button(self.root, text="Toggle Preview", command=self.toggle_preview, height=2, width=20)
        self.toggle_preview_button.pack(side=tk.TOP, pady=5)

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack(side=tk.TOP, pady=5)

        # Show loading screen in the camera preview spot
        self.loading_label = self.canvas.create_text(320, 240, text="Loading...", font=("Helvetica", 14), fill="black")

        self.direction_label = tk.Label(self.root, text="Direction: Center", font=("Helvetica", 14))
        self.direction_label.pack(side=tk.TOP, pady=5)

        # Add sliders for defining lines
        self.lines_frame = tk.Frame(self.root)
        self.lines_frame.pack(side=tk.TOP, pady=5)
        tk.Label(self.lines_frame, text="Left Line Position:").grid(row=0, column=0)
        self.left_line_slider = tk.Scale(self.lines_frame, from_=0, to=640, orient=tk.HORIZONTAL)
        self.left_line_slider.set(self.config["left_line_position"])  # Load from config
        self.left_line_slider.grid(row=0, column=1)

        tk.Label(self.lines_frame, text="     ").grid(row=0, column=2)  # Space between sliders

        tk.Label(self.lines_frame, text="Right Line Position:").grid(row=0, column=3)
        self.right_line_slider = tk.Scale(self.lines_frame, from_=0, to=640, orient=tk.HORIZONTAL)
        self.right_line_slider.set(self.config["right_line_position"])  # Load from config
        self.right_line_slider.grid(row=0, column=4)

        self.keybinds_frame = tk.Frame(self.root)
        self.keybinds_frame.pack(side=tk.TOP, pady=5)
        tk.Label(self.keybinds_frame, text="Left lean =").grid(row=0, column=0)
        self.left_key_var = tk.StringVar(value=self.config["left_key"])  # Load from config
        tk.Entry(self.keybinds_frame, textvariable=self.left_key_var, width=5).grid(row=0, column=1)
        tk.Button(self.keybinds_frame, text="Set", command=self.set_left_keybind).grid(row=0, column=2)

        tk.Label(self.keybinds_frame, text="Right lean =").grid(row=1, column=0)
        self.right_key_var = tk.StringVar(value=self.config["right_key"])  # Load from config
        tk.Entry(self.keybinds_frame, textvariable=self.right_key_var, width=5).grid(row=1, column=1)
        tk.Button(self.keybinds_frame, text="Set", command=self.set_right_keybind).grid(row=1, column=2)

        tk.Label(self.keybinds_frame, text="Start/Stop tracking =").grid(row=2, column=0)
        self.start_stop_key_var = tk.StringVar(value=self.config["start_stop_key"])  # Load from config
        tk.Entry(self.keybinds_frame, textvariable=self.start_stop_key_var, width=5).grid(row=2, column=1)
        tk.Button(self.keybinds_frame, text="Set", command=self.set_start_stop_keybind).grid(row=2, column=2)

    def list_cameras(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr

    def initialize_camera(self):
        self.face_tracker = FaceTracker(camera_index=int(self.camera_var.get()))
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        # Remove loading screen
        self.canvas.delete(self.loading_label)

    def toggle_tracking(self, event=None):
        self.tracking_enabled = not self.tracking_enabled
        if self.tracking_enabled:
            self.toggle_button.config(text="Stop", bg="red")
        else:
            self.toggle_button.config(text="Start", bg="green")
            # Ensure keys are released when tracking stops
            self.keyboard.release(self.left_key_var.get())
            self.keyboard.release(self.right_key_var.get())
            self.current_direction = "Center"

    def toggle_preview(self):
        self.preview_enabled = not self.preview_enabled

    def on_closing(self):
        self.running = False
        self.root.quit()
        self.root.destroy()

    def capture_frames(self):
        while self.running:
            self.face_tracker.capture_frame()

    def main_loop(self):
        if not hasattr(self, 'face_tracker') or not self.face_tracker.ret:
            self.root.after(10, self.main_loop)
            return

        results = self.face_tracker.process_frame()

        # Get the positions of the defining lines from the sliders
        left_line_pos = self.left_line_slider.get()
        right_line_pos = self.right_line_slider.get()

        # Ensure minimum distance between lines
        if right_line_pos - left_line_pos < 50:
            right_line_pos = left_line_pos + 50
            self.right_line_slider.set(right_line_pos)

        if self.tracking_enabled and results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                x, y, w, h = (int(bboxC.xmin * self.face_tracker.frame_width), int(bboxC.ymin * self.face_tracker.frame_height),
                              int(bboxC.width * self.face_tracker.frame_width), int(bboxC.height * self.face_tracker.frame_height))

                face_center_x = x + w // 2
                self.face_tracker.smoothed_face_center_x = int(self.face_tracker.smoothing_factor * self.face_tracker.smoothed_face_center_x + (1 - self.face_tracker.smoothing_factor) * face_center_x)

                # Draw bounding box around the face
                cv2.rectangle(self.face_tracker.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if self.face_tracker.smoothed_face_center_x < left_line_pos:
                    if self.current_direction != "Left":
                        self.keyboard.press(self.left_key_var.get())
                        self.keyboard.release(self.right_key_var.get())
                        self.current_direction = "Left"
                    self.direction_label.config(text="Direction: Left")
                    if self.preview_enabled:
                        cv2.putText(self.face_tracker.frame, 'Left', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                elif self.face_tracker.smoothed_face_center_x > right_line_pos:
                    if self.current_direction != "Right":
                        self.keyboard.press(self.right_key_var.get())
                        self.keyboard.release(self.left_key_var.get())
                        self.current_direction = "Right"
                    self.direction_label.config(text="Direction: Right")
                    if self.preview_enabled:
                        cv2.putText(self.face_tracker.frame, 'Right', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                else:
                    if self.current_direction != "Center":
                        self.keyboard.release(self.left_key_var.get())
                        self.keyboard.release(self.right_key_var.get())
                        self.current_direction = "Center"
                    self.direction_label.config(text="Direction: Center")
                    if self.preview_enabled:
                        cv2.putText(self.face_tracker.frame, 'Center', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        else:
            if self.current_direction != "Center":
                self.keyboard.release(self.left_key_var.get())
                self.keyboard.release(self.right_key_var.get())
                self.current_direction = "Center"
            self.direction_label.config(text="Direction: Center")

        if self.preview_enabled:
            cv2.line(self.face_tracker.frame, (left_line_pos, 0), (left_line_pos, self.face_tracker.frame_height), (0, 255, 0), 2)
            cv2.line(self.face_tracker.frame, (right_line_pos, 0), (right_line_pos, self.face_tracker.frame_height), (0, 255, 0), 2)

            img = Image.fromarray(cv2.cvtColor(self.face_tracker.frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk

        self.root.after(10, self.main_loop)

    def set_left_keybind(self):
        key = self.left_key_var.get()
        if len(key) == 1 and key.isalpha():
            self.left_key_var.set(key.lower())
        else:
            self.left_key_var.set('q')  # Reset to default if invalid
        self.config_manager.update_config("left_key", self.left_key_var.get())

    def set_right_keybind(self):
        key = self.right_key_var.get()
        if len(key) == 1 and key.isalpha():
            self.right_key_var.set(key.lower())
        else:
            self.right_key_var.set('e')  # Reset to default if invalid
        self.config_manager.update_config("right_key", self.right_key_var.get())

    def set_start_stop_keybind(self):
        key = self.start_stop_key_var.get()
        if len(key) == 1 and key.isalpha():
            self.start_stop_key_var.set(key.lower())
        else:
            self.start_stop_key_var.set(']')  # Reset to default if invalid
        # Rebind the key
        self.root.bind(f'<KeyPress-{self.start_stop_key_var.get()}>', self.toggle_tracking)
        self.config_manager.update_config("start_stop_key", self.start_stop_key_var.get())

    def load_config(self):
        self.left_line_slider.set(self.config["left_line_position"])
        self.right_line_slider.set(self.config["right_line_position"])
        self.left_key_var.set(self.config["left_key"])
        self.right_key_var.set(self.config["right_key"])
        self.start_stop_key_var.set(self.config["start_stop_key"])