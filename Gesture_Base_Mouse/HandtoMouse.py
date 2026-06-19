import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
import ctypes

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
path = "C:\\Users\\praja_mfg91s7\\OneDrive\\Desktop\\Workspace\\Gesture_Base_Mouse\\hand_landmarker.task"
isClicked = False
prev_x = 0
prev_y = 0
def result_callback(result, output_image, timestamp_ms, scalecoeff = 1.7):
    num_hands = len(result.handedness)
    global prev_x
    global prev_y
    global isClicked
    result_callback.call_count += 1
    for i in range(len(result.handedness)):
        lr = result.handedness[i][0]
        constx, consty = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        if num_hands ==1:
            if lr.category_name =="Right":
                if ctypes.windll.user32.GetSystemMetrics(80)>1:
                    constx += ctypes.windll.user32.GetSystemMetrics(78)
                    consty = ctypes.windll.user32.GetSystemMetrics(79)
                    ctypes.windll.user32.SetCursorPos(int((0.6*result.hand_landmarks[i][8].x+0.4*prev_x)*constx*scalecoeff), int(((0.6*result.hand_landmarks[i][8].y+0.4*prev_y)*consty*scalecoeff)))
                    prev_x = result.hand_landmarks[i][8].x
                    prev_y = result.hand_landmarks[i][8].y
                else:
                    ctypes.windll.user32.SetCursorPos(int((0.6*result.hand_landmarks[i][8].x+0.4*prev_x)*constx*scalecoeff), int(((0.6*result.hand_landmarks[i][8].y+0.4*prev_y)*consty*scalecoeff)))
                    prev_x = result.hand_landmarks[i][8].x
                    prev_y = result.hand_landmarks[i][8].y

        elif num_hands == 2:
            if lr.category_name=="Right":
                if ctypes.windll.user32.GetSystemMetrics(80)>1:
                    constx += ctypes.windll.user32.GetSystemMetrics(78)
                    consty = ctypes.windll.user32.GetSystemMetrics(79)
                    ctypes.windll.user32.SetCursorPos(int((0.6*result.hand_landmarks[i][8].x+0.4*prev_x)*constx), int(((0.6*result.hand_landmarks[i][8].y+0.4*prev_y)*consty)))
                    prev_x = result.hand_landmarks[i][8].x
                    prev_y = result.hand_landmarks[i][8].y
                else:
                    ctypes.windll.user32.SetCursorPos(int((0.6*result.hand_landmarks[i][8].x+0.4*prev_x)*constx*scalecoeff), int(((0.6*result.hand_landmarks[i][8].y+0.4*prev_y)*consty*scalecoeff)))
                    prev_x = result.hand_landmarks[i][8].x
                    prev_y = result.hand_landmarks[i][8].y

            elif lr.category_name =="Left":
                indexx =result.hand_landmarks[i][8].x
                indexy =result.hand_landmarks[i][8].y
                thumbx =result.hand_landmarks[i][4].x
                thumby =result.hand_landmarks[i][4].y
                dist =((indexx-thumbx)**2+(indexy-thumby)**2)**0.5
                if dist< 0.05 and isClicked==False:
                    ctypes.windll.user32.mouse_event(2,0,0,0,0)
                    isClicked = True
                if isClicked==True and dist>0.05:
                    ctypes.windll.user32.mouse_event(4,0,0,0,0)
                    isClicked = False

result_callback.call_count = 0              
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