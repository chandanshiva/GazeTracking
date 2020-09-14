# Gaze Tracking with Head Pose Estimation

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

The base API was built by antoinelame is a Python (2 and 3) library that provides a **webcam-based eye tracking system**. It gives you the exact position of the pupils and the gaze direction, in real time. It is integrated with head pose estimation, it gives Gaze data with gaze direction data.

 
 Please follow the steps to setup

## Installation

Clone this project:

```
git clone https://gitlab.comp.dkit.ie/D00225825/dissertationgazetracking
```

Install these dependencies (NumPy, OpenCV, Dlib,..):

```
pip install -r requirements.txt
```

> The Dlib library has four primary prerequisites: Boost, Boost.Python, CMake and X11/XQuartx. If you doesn't have them, you can [read this article](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/) to know how to easily install them.

Run the demo:

```
python main.py
```

## Simple Demo

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break
```

## Documentation

In the following examples, `gaze` refers to an instance of the `GazeTracking` class.

### Refresh the frame

```python
gaze.refresh(frame)
```

Pass the frame to analyze (numpy.ndarray). If you want to work with a video stream, you need to put this instruction in a loop, like the example above.

### Position of the left pupil

```python
gaze.pupil_left_coords()
```

Returns the coordinates (x,y) of the left pupil.

### Position of the right pupil

```python
gaze.pupil_right_coords()
```

Returns the coordinates (x,y) of the right pupil.

### Looking to the left

```python
gaze.is_left()
```

Returns `True` if the user is looking to the left.

### Looking to the right

```python
gaze.is_right()
```

Returns `True` if the user is looking to the right.

### Looking at the center

```python
gaze.is_center()
```

Returns `True` if the user is looking at the center.

### Horizontal direction of the gaze

```python
ratio = gaze.horizontal_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the horizontal direction of the gaze. The extreme right is 0.0, the center is 0.5 and the extreme left is 1.0.

### Vertical direction of the gaze

```python
ratio = gaze.vertical_ratio()
```

Returns a number between 0.0 and 1.0 that indicates the vertical direction of the gaze. The extreme top is 0.0, the center is 0.5 and the extreme bottom is 1.0.

### Blinking

```python
gaze.is_blinking()
```

Returns `True` if the user's eyes are closed.

### Webcam frame

```python
frame = gaze.annotated_frame()
```

Returns the main frame with pupils highlighted.

## Head Pose Estimation

```python
(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,
                                                                      cam_matrix, dist_coeffs,
                                                                      flags=cv2.SOLVEPNP_ITERATIVE)
```

Returns 3D object point's position with respect to the Camera position using 2D facial landmark points from Dlib

```python
(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector,
                                                         cam_matrix, dist_coeffs)
```

Projects a Jacobian matrix points with respect to rotation and transition direction to draw a line of direction
 
## Data Aggregation

```python
df = pd.DataFrame(data_list, columns=['quadrant','left_pupil','right_pupil','gaze_center_x', 'gaze_center_y', 'nose_end_points',
                                      'gaze_end_points'])
df.to_csv("myrecorded_data.csv")
```

Selecting the data to record for analysis


## You want to help?

Your feedback and suggestions are welcome and appreciated.
