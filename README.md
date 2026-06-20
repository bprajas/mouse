Gesture Base Mouse

Control your mouse using hand gestures and a webcam.

Built with MediaPipe hand tracking, OpenCV, and Win32 mouse APIs.

What it can do

Move the cursor using hand tracking
Click using a pinch gesture
Hold and drag
Smooth cursor movement to reduce jitter
Basic support for a single extended monitor
Controls

My webcam feed had to be mirrored, so the controls are:

Left hand → Move cursor
Right hand → Click / drag
Movement

The tip of the index finger is tracked and mapped to screen coordinates.

Clicking

Bring the thumb and index finger together on the right hand.

Pinch → Mouse down
Release → Mouse up
This allows normal clicking as well as click-and-drag operations.

#Running

Install dependencies:
'''bash
pip install opencv-python mediapipe
'''
Run:
'''bash
python hand_to_mouse.py
'''
Press q to quit.

Known Issues

Multi-monitor support is still a bit cursed.
Cursor can occasionally teleport on extended displays.
Tracking quality depends on lighting and camera quality.
Only tested on Windows.
Future Ideas

Better multi-monitor support
Eye tracking mode
Facial gesture controls
Calibration system
Sensitivity settings
Current Status

Works. Mostly.