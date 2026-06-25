# Gesture Base Mouse

Control your mouse using hand gestures and a webcam.

Built with MediaPipe hand tracking, OpenCV, and Win32 mouse APIs.

## What It Can Do

* Move the cursor using hand tracking
* Click using a pinch gesture
* Hold and drag
* Smooth cursor movement to reduce jitter
* Basic support for a single extended monitor

## Controls

My webcam feed had to be mirrored, so the controls are:

* **Left Hand** → Move cursor / Right Click
* **Right Hand** → Left Click / Drag

### Movement

The tip of the index finger is tracked and mapped to screen coordinates.

### Clicking

Bring the thumb and index finger together on the right hand.

* Pinch → Mouse Down
* Release → Mouse Up

This allows both normal left clicking and click-and-drag operations.

Bring the thumb and middle finger together on the left hand.

* Pinch → Mouse Down
* Release → Mouse Up

This allows normal roght click.

## Running

### Install Dependencies

```bash
pip install opencv-python mediapipe
```

### Run

```bash
python hand_to_mouse.py
```

Press `q` to quit.

## Known Issues

* Multi-monitor support is still a bit cursed.
* Cursor can occasionally teleport on extended displays.
* Tracking quality depends on lighting, camera quality, camera position and distance. It is preferable to keep the webcam slightly above and away from yourself for best mouse smoothing.
* Only tested on Windows.

## Future Ideas

* Better multi-monitor support
* Eye tracking mode
* Facial gesture controls
* Sensitivity settings

## Current Status

Works. Mostly.
