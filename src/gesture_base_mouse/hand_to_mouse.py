"""Control mouse using MediaPipe hand gestures."""
from pathlib import Path as p
import ctypes

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

base_path=p(__file__).resolve().parent
model_path=base_path / "hand_landmarker.task"

BaseOptions=mp.tasks.BaseOptions
VisionRunningMode=mp.tasks.vision.RunningMode

class HandMouse:
    """Converts hand gestures into mouse movements and clicks."""
    def __init__(self):
        """Set constants and states."""
        self.is_clicked=False
        self.is_rclicked=False
        self.prev_x=0
        self.prev_y=0
    def result_callback(self, result, output_image=None, timestamp_ms=None):
        """Handle hand landmark results and update mouse state."""
        if ctypes.windll.user32.GetSystemMetrics(80) > 1:
            screen_width = ctypes.windll.user32.GetSystemMetrics(78)
            screen_height = ctypes.windll.user32.GetSystemMetrics(79)
        else:
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        smoothing = 0.9
        min_coord = 0.03
        max_coord = 0.97
        for i, handedness in enumerate(result.handedness):
            if handedness[0].category_name=="Right" and len(result.handedness)==2:
                middle_thumb_dist = (
                    (result.hand_landmarks[i][12].x-
                    result.hand_landmarks[i][4].x)**2
                    +(result.hand_landmarks[i][12].y-
                    result.hand_landmarks[i][4].y)**2
                )**0.5
                if middle_thumb_dist < 0.05 and not self.is_rclicked:
                    ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)
                    self.is_rclicked = True
                elif self.is_rclicked and middle_thumb_dist > 0.05:
                    ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)
                    self.is_rclicked = False
                hand_x=max(min_coord,min(max_coord,result.hand_landmarks[i][8].x))
                hand_y=max(min_coord,min(max_coord,result.hand_landmarks[i][8].y))
                self.prev_x = (
                    self.prev_x *
                    (1-smoothing) +
                    (hand_x - min_coord) / (max_coord - min_coord)*
                    smoothing
                )
                self.prev_y = (
                    self.prev_y*
                    (1-smoothing)+
                    (hand_y-min_coord) / (max_coord - min_coord)*
                    smoothing
                )
                ctypes.windll.user32.SetCursorPos(
                    int(self.prev_x * screen_width),
                    int(self.prev_y * screen_height),
                )
            elif handedness[0].category_name=="Left" and len(result.handedness)==2:
                index_thumb_dist = (
                    (result.hand_landmarks[i][8].x -
                    result.hand_landmarks[i][4].x) ** 2
                    + (result.hand_landmarks[i][8].y -
                    result.hand_landmarks[i][4].y) ** 2
                ) ** 0.5
                if index_thumb_dist < 0.05 and not self.is_clicked:
                    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                    self.is_clicked = True
                elif self.is_clicked and index_thumb_dist > 0.05:
                    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                    self.is_clicked = False

    def run(self):
        """Start webcam capture and gesture processing and mouse movement."""
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=str(model_path)),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.result_callback,
            num_hands=2)
        
        detector = vision.HandLandmarker.create_from_options(options)
        cap = cv2.VideoCapture(0)
        timestamp = 0
        while True:
            ret, frame_to_be_flipped = cap.read()

            if not ret:
                continue

            frame = cv2.flip(frame_to_be_flipped, 1)
            
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb)

            detector.detect_async(
                mp_image,
                timestamp)

            timestamp += 1

            if cv2.waitKey(1) == ord("q"):
                break

control = HandMouse()
control.run()
