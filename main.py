"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pandas as pd
import numpy as np

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
data_list = []

K = [6.2500000000000000e+002, 0.0, 3.1250000000000000e+002,
     0.0, 6.2500000000000000e+002, 3.1250000000000000e+002,
     0.0, 0.0, 1.0]

# 3D model points.
model_points = np.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left cornerq
    (225.0, 170.0, -135.0),  # Right eye right corne
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner

])


while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    size = frame.shape

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
    #
    # line1 = [int((w / 2)), 0, int((w / 2)), h]
    # line2 = [0, int((h / 2)), w, int((h / 2))]
    # all_lines = [line1, line2]  # 4 quad


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 0), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is not None and right_pupil is not None:
        # first_quad = [(597, 150), (702, 200)]  # Top-left, Bottom right - 1st quad
        # first_quad = [(0, 150), (600, 200)]  # Top-right, Bottom right - 1st quad

        center_x = int((left_pupil[0] + right_pupil[0]) / 2)
        center_y = int((left_pupil[1] + right_pupil[1]) / 2)

        # if 625 < center_x < 650 and 200 < center_y < 210:
        #     print("Looking at first quad", center_x, center_y)
        #
        #     data_list.append([left_pupil, right_pupil, "first"])
        #     cv2.putText(frame, "You are looking on 1st grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        # elif 600 < center_x < 625 and 200 < center_y < 210:
        #     print("Looking at second quad", center_x, center_y)
        #     cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        #     data_list.append([left_pupil, right_pupil, "second"])
        #
        # elif 570 < center_x < 670 and 200 < center_y < 210:
        #     print("Looking at third quad", center_x, center_y)
        #     cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        #     data_list.append([left_pupil, right_pupil, "third"])
        #
        # else:
        #     print("Looking at fourth quad", center_x, center_y)
        #     cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        #     data_list.append([left_pupil, right_pupil, "fourth"])

        # Camera internals
        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)

        # We are then accesing the landmark points
        i = [33, 8, 36, 45, 48,
             54]  # Nose tip, Chin, Left eye corner, Right eye corner, Left mouth corner, right mouth corner
        image_points = []
        for n in i:
            x = gaze.gaze_landmarks.part(n).x
            y = gaze.gaze_landmarks.part(n).y;
            # image_points = np.array([(x,y)], dtype="double")
            image_points += [(x, y)]
            cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

        image_points = np.array(image_points, dtype="double")
        # print(image_points)
        print("Camera Matrix :\n {0}".format(cam_matrix))

        dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,
                                                                      cam_matrix, dist_coeffs,
                                                                      flags=cv2.SOLVEPNP_ITERATIVE)

        print("Rotation Vector:\n {0}".format(rotation_vector))
        print("Translation Vector:\n {0}".format(translation_vector))

        # Project a 3D point (0, 0, 1000.0) onto the image plane.
        # We use this to draw a line sticking out of the nose

        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector,
                                                         cam_matrix, dist_coeffs)

        for p in image_points:
            cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        center_nose_x = image_points[0][0]
        center_nose_y = image_points[0][1]
        end_nose_x = nose_end_point2D[0][0][0]
        end_nose_y = nose_end_point2D[0][0][1]

        if 0 < end_nose_x < center_nose_x and 0 < end_nose_y < center_nose_y:
            print("Looking at 1st")
            cv2.putText(frame, "You are looking on 1st grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append(['1st', left_pupil, right_pupil, center_x, center_y, p1, p2])

        elif center_nose_x < end_nose_x < (w*10) and 0 < end_nose_y < center_nose_y:
            print("looking at 2nd")
            cv2.putText(frame, "You are looking on 2nd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append(['2nd', left_pupil, right_pupil, center_x, center_y, p1, p2])

        elif 0 < end_nose_x < center_nose_x and center_nose_y < end_nose_y < (h*10):
            print("looking at 4th")
            cv2.putText(frame, "You are looking on 4th grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append(['4th', left_pupil, right_pupil, center_x, center_y, p1, p2])

        else:
            print("looking at 3rd")
            cv2.putText(frame, "You are looking on 3rd grid", (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
            data_list.append(['3rd', left_pupil, right_pupil, center_x, center_y, p1, p2])


        cv2.line(frame, (0, int(center_nose_y)), (w, int(center_nose_y)), (0, 255, 0), 2)
        cv2.line(frame, (int(center_nose_x), 0), (int(center_nose_x), h), (0, 255, 0), 2)
        cv2.line(frame, p1, p2, (255, 0, 0), 2)
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 1)

        cv2.imshow("Demo", frame)


        if cv2.waitKey(1) == 27:
            break

df = pd.DataFrame(data_list, columns=['quadrant','left_pupil','right_pupil','gaze_center_x', 'gaze_center_y', 'nose_end_points',
                                      'gaze_end_points'])
df.to_csv("myrecorded_data.csv")