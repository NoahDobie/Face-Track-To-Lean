import os
import sys
import tkinter as tk
import logging
from controller import Controller
import cv2
from PIL import Image, ImageTk

logging.basicConfig(level=logging.DEBUG)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

CONFIG_PATH = resource_path(os.path.join('config', 'config.properties'))
logging.debug(f"Config path: {CONFIG_PATH}")

if __name__ == "__main__":
    app = None
    try:
        root = tk.Tk()
        app = Controller(root, config_path=CONFIG_PATH)
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        if app and app.face_tracker:
            app.face_tracker.release()
        cv2.destroyAllWindows()