"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pandas as pd

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
data_list = []
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    h, w, c = frame.shape

    line1 = [int((w / 2)), 0, int((w / 2)), h]
    line2 = [0, int((h / 2)), w, int((h / 2))]
    all_lines = [line1, line2]  # 4 quad

    for line in all_lines:
        cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 0), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is not None and right_pupil is not None:
        # first_quad = [(597, 150), (702, 200)]  # Top-left, Bottom right - 1st quad
        # first_quad = [(0, 150), (600, 200)]  # Top-right, Bottom right - 1st quad

        center_x = int((left_pupil[0] + right_pupil[0]) / 2)
        center_y = int((left_pupil[1] + right_pupil[1]) / 2)

        data = {'left_pupil': [left_pupil], 'right_pupil': [right_pupil], 'center_x': [center_x], 'center_y': [center_y]}

        if 625 < center_x < 650 and 200 < center_y < 210:
            print("Looking at first quad", center_x, center_y)

            data_list.append([left_pupil, right_pupil, "first"])
            cv2.putText(frame, "You are looking on 1st grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        elif 600 < center_x < 625 and 200 < center_y < 210:
            print("Looking at second quad", center_x, center_y)
            cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append([left_pupil, right_pupil, "second"])

        elif 570 < center_x < 670 and 200 < center_y < 210:
            print("Looking at third quad", center_x, center_y)
            cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append([left_pupil, right_pupil, "third"])

        else:
            print("Looking at fourth quad", center_x, center_y)
            cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append([left_pupil, right_pupil, "fourth"])

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)

    cv2.imshow("Demo", frame)
    # df = pd.DataFrame(data)
    # print(df)
    # df.to_csv('data.csv')

    if cv2.waitKey(1) == 27:
        break
df = pd.DataFrame(data_list, columns=['left_pupil','right_pupil','quad'])
df.to_csv("myrecorded_data.csv")