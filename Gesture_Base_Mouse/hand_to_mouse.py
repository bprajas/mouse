"""Control mouse using MediaPipe hand gestures."""

from pathlib import Path as p
import ctypes

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

base_path = p(__file__).resolve().parent
model_path = base_path / "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

IS_CLICKED = False
IS_DRAGGING = False

PREV_X = 0.0
PREV_Y = 0.0


def result_callback(result, output_image=None, timestamp_ms=None):
    """Handle hand landmark results and update mouse state."""
    
    global PREV_X, PREV_Y, IS_CLICKED, IS_DRAGGING
    num_hands = len(result.handedness)
    if ctypes.windll.user32.GetSystemMetrics(80) > 1:
        screen_width = ctypes.windll.user32.GetSystemMetrics(78)
        screen_height = ctypes.windll.user32.GetSystemMetrics(79)
    else:
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    smoothing = 0.9
    smoothing_prev = 1 - smoothing

    min_coord = 0.03
    max_coord = 0.97

    for i in range(num_hands):
        handedness = result.handedness[i][0].category_name
        landmarks = result.hand_landmarks[i]

        if handedness == "Right" and num_hands == 2:
            thumb_x = landmarks[4].x
            thumb_y = landmarks[4].y

            middle_x = landmarks[12].x
            middle_y = landmarks[12].y

            drag_distance = (
                (middle_x - thumb_x) ** 2
                + (middle_y - thumb_y) ** 2
            ) ** 0.5

            if drag_distance < 0.05 and not IS_DRAGGING:
                ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)
                IS_DRAGGING = True

            elif IS_DRAGGING and drag_distance > 0.05:
                ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)
                IS_DRAGGING = False

            hand_x = landmarks[8].x
            hand_y = landmarks[8].y

            hand_x = max(min_coord, min(max_coord, hand_x))
            hand_y = max(min_coord, min(max_coord, hand_y))

            screen_x = (hand_x - min_coord) / (max_coord - min_coord)
            screen_y = (hand_y - min_coord) / (max_coord - min_coord)

            PREV_X = PREV_X * smoothing_prev + screen_x * smoothing
            PREV_Y = PREV_Y * smoothing_prev + screen_y * smoothing

            cursor_x = int(PREV_X * screen_width)
            cursor_y = int(PREV_Y * screen_height)

            ctypes.windll.user32.SetCursorPos(cursor_x, cursor_y)

        elif handedness == "Left" and num_hands == 2:
            index_x = landmarks[8].x
            index_y = landmarks[8].y

            thumb_x = landmarks[4].x
            thumb_y = landmarks[4].y
            click_distance = (
                (index_x - thumb_x) ** 2
                + (index_y - thumb_y) ** 2
            ) ** 0.5

            if click_distance < 0.05 and not IS_CLICKED:
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                IS_CLICKED = True

            elif IS_CLICKED and click_distance > 0.05:
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                IS_CLICKED = False


options = vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback,
    num_hands=2,
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
timestamp = 0

while True:
    ret, frame_to_be_flipped = cap.read()

    frame = cv2.flip(frame_to_be_flipped, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb,
    )

    detector.detect_async(mp_image, timestamp)

    timestamp += 1

    if cv2.waitKey(1) == ord("q"):
        break