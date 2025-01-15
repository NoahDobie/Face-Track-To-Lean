import tkinter as tk
import logging
from controller import Controller
import cv2
from PIL import Image, ImageTk

if __name__ == "__main__":
    app = None
    try:
        root = tk.Tk()
        app = Controller(root)
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        if app and app.face_tracker:
            app.face_tracker.release()
        cv2.destroyAllWindows()