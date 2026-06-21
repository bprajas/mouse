import ctypes
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision


path = "C:\\Users\\praja_mfg91s7\\OneDrive\\Desktop\\Workspace\\Gesture_Base_Mouse\\hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

is_Clicked = False
is_Clicked2 = False
prev_x=0
prev_y=0


def result_callback(result, output_image=None, timestamp_ms=None):
    num_hands=len(result.handedness)
    global prev_x,prev_y,is_Clicked,is_Clicked2
    if ctypes.windll.user32.GetSystemMetrics(80)>1:
        constx,consty=ctypes.windll.user32.GetSystemMetrics(78),ctypes.windll.user32.GetSystemMetrics(79)
    else:
        constx, consty=ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    sc=0.9
    sp=1- sc
    min_xy, max_xy=0.03, 0.97
    
    for i in range(num_hands):
        handedness=result.handedness[i][0].category_name
        landmarks=result.hand_landmarks[i]

        if handedness=="Right" and num_hands==2:
            thumbx=landmarks[4].x
            thumby=landmarks[4].y
            midx=landmarks[12].x
            midy=landmarks[12].y
            dist1=((midx-thumbx)**2 + (midy-thumby)**2)**0.5

            if dist1<0.05 and not is_Clicked2:
                ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)
                is_Clicked2=True
            elif is_Clicked2 and dist1 > 0.05:
                ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)
                is_Clicked2=False

            pos_x=landmarks[8].x
            pos_y=landmarks[8].y

            pos_x=max(min_xy, min(max_xy, pos_x))
            pos_y=max(min_xy, min(max_xy, pos_y))

            screen_x=(pos_x-min_xy)/(max_xy-min_xy)
            screen_y=(pos_y-min_xy)/(max_xy-min_xy)

            prev_x=prev_x*sp+screen_x*sc
            prev_y=prev_y*sp+screen_y*sc

            final_x=int(prev_x*constx)
            final_y=int(prev_y*consty)

            ctypes.windll.user32.SetCursorPos(final_x, final_y)

        elif handedness=="Left" and num_hands==2:
            indexx=landmarks[8].x
            indexy=landmarks[8].y
            thumbx=landmarks[4].x
            thumby=landmarks[4].y

            dist=((indexx-thumbx)**2 + (indexy-thumby)**2)**0.5

            if dist<0.05 and not is_Clicked:
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                is_Clicked=True
            elif is_Clicked and dist > 0.05:
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                is_Clicked=False


options =vision.HandLandmarkerOptions(base_options=BaseOptions(model_asset_path=path),running_mode=VisionRunningMode.LIVE_STREAM,result_callback=result_callback, num_hands=2)
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
