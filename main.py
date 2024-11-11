import tkinter as tk
import logging
from facetrackerapp import FaceTrackerApp
import cv2

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FaceTrackerApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    finally:
        app.face_tracker.release()
        cv2.destroyAllWindows()
