import cv2
import mediapipe as mp
import logging

logging.basicConfig(level=logging.INFO)

class FaceTracker:
    def __init__(self, camera_index, smoothing_factor=0.5, frame_width=640, frame_height=480):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            logging.error(f"Error: Could not open webcam with index {camera_index}.")
            exit()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_center_x = self.frame_width // 2
        self.smoothing_factor = smoothing_factor
        self.smoothed_face_center_x = self.frame_center_x
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)
        self.frame = None
        self.ret = False

    def capture_frame(self):
        self.ret, self.frame = self.cap.read()
        return self.ret, self.frame

    def process_frame(self):
        small_frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
        gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        enhanced_frame = cv2.equalizeHist(gray_frame)
        rgb_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_GRAY2RGB)
        results = self.face_detection.process(rgb_frame)
        return results

    def release(self):
        self.cap.release()