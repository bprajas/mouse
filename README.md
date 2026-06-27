# Gesture Base Mouse

Control your mouse using hand gestures and a webcam.

Gesture Base Mouse uses MediaPipe hand tracking, OpenCV, and the Windows Win32 API to convert hand movements into mouse input. The project tracks both hands in real time, allowing cursor movement, left-clicking, right-clicking, and click-and-drag interactions without touching a physical mouse.

## Features

* Real-time hand tracking using MediaPipe
* Cursor movement using index finger position
* Left click via pinch gesture, right click via pinch gesture
* Windows desktop integration through Win32 mouse APIs

## Structure

```text
.
├── README.md
├── pyproject.toml
├── poetry.lock
└── src
    └── gesture_base_mouse
        ├── __init__.py
        ├── hand_landmarker.task
        └── hand_to_mouse.py
```

## Controls

### Cursor Movement

Move your left index finger to control the cursor position.

### Left Click and Drag

Right Hand:

* Thumb + Index Finger pinch → Mouse Down
* Release pinch → Mouse Up

Holding the pinch allows click-and-drag operations.

### Right Click

Left Hand:

* Thumb + Index Finger pinch → Right Click

## Requirements

* Python 3.11+
* Windows
* Webcam

## Installation

### Clone the Repository

```bash
git clone https://github.com/<your-username>/Gesture_Base_Mouse.git
cd Gesture_Base_Mouse
```

### Install Poetry

```bash
pip install poetry
```

Verify installation:

```bash
python -m poetry --version
```

### Install Dependencies

```bash
python -m poetry install
```

This creates a virtual environment and installs all project dependencies defined in `pyproject.toml`.

## Running

Run the application using Poetry:

```bash
python -m poetry run python src/gesture_base_mouse/hand_to_mouse.py
```

Alternatively, activate the Poetry environment first:

```bash
python -m poetry shell
python src/gesture_base_mouse/hand_to_mouse.py
```

Press `q` to quit.

## Known Issues

* Multi-monitor support is not fully reliable
* Cursor accuracy depends on lighting conditions
* Tracking quality depends on webcam quality and positioning
* Rapid hand motion can occasionally cause cursor jumps
* Windows only

## Future Improvements

* Calibration system
* Adjustable sensitivity
* Custom gesture mapping
* Eye tracking integration
* Cross-platform support
* User configuration profiles

## Current Status

Working prototype.

The application is stable under normal lighting conditions and demonstrates reliable cursor control, clicking, and dragging through hand gestures.
