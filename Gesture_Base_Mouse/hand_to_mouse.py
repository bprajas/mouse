from pathlib import Path as p
import ctypes

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

basepath = p(__file__).resolve().parent
path = basepath / "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

IS_CLICKED = False
IS_CLICKED2 = False
PREV_X=0
PREV_Y=0

def result_callback(result, output_image=None, timestamp_ms=None):
    num_hands=len(result.handedness)
    global PREV_X,prev_y,IS_CLICKED,IS_CLICKED2
    if ctypes.windll.user32.GetSystemMetrics(80)>1:
        constx=ctypes.windll.user32.GetSystemMetrics(78)
        consty=ctypes.windll.user32.GetSystemMetrics(79)
    else:
        constx=ctypes.windll.user32.GetSystemMetrics(0)
        consty=ctypes.windll.user32.GetSystemMetrics(1)
    
    S_C=0.9
    S_P=1- S_C
    MIN_XY, MAX_XY=0.03, 0.97
    
    for i in range(num_hands):
        handedness=result.handedness[i][0].category_name
        landmarks=result.hand_landmarks[i]

        if handedness=="Right" and num_hands==2:
            thumbx=landmarks[4].x
            thumby=landmarks[4].y
            midx=landmarks[12].x
            midy=landmarks[12].y
            dist1=((midx-thumbx)**2 + (midy-thumby)**2)**0.5

            if dist1<0.05 and not IS_CLICKED2:
                ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)
                IS_CLICKED2=True
            elif IS_CLICKED2 and dist1 > 0.05:
                ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)
                IS_CLICKED2=False

            pos_x=landmarks[8].x
            pos_y=landmarks[8].y

            pos_x=max(MIN_XY, min(MAX_XY, pos_x))
            pos_y=max(MIN_XY, min(MAX_XY, pos_y))

            screen_x=(pos_x-MIN_XY)/(MAX_XY-MIN_XY)
            screen_y=(pos_y-MIN_XY)/(MAX_XY-MIN_XY)

            PREV_X=PREV_X*S_P+screen_x*S_C
            PREV_Y=PREV_Y*S_P+screen_y*S_C

            final_x=int(PREV_X*constx)
            final_y=int(PREV_Y*consty)

            ctypes.windll.user32.SetCursorPos(final_x, final_y)

        elif handedness=="Left" and num_hands==2:
            indexx=landmarks[8].x
            indexy=landmarks[8].y
            thumbx=landmarks[4].x
            thumby=landmarks[4].y

            dist=((indexx-thumbx)**2 + (indexy-thumby)**2)**0.5

            if dist<0.05 and not IS_CLICKED:
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                IS_CLICKED=True
            elif IS_CLICKED and dist > 0.05:
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                IS_CLICKED=False

options =vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback, 
    num_hands=2
    )

detector =vision.HandLandmarker.create_from_options(options)

cap =cv2.VideoCapture(0)
timestamp =0

while True:
    ret, frametobeflipped =cap.read()
    frame =cv2.flip(frametobeflipped,1)
    rgb =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image =mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    detector.detect_async(mp_image, timestamp)
    timestamp+=1
    if cv2.waitKey(1) == ord("q"):
        break
