import cv2
import dlib
import numpy as np

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Read Image
# im = cv2.imread("headPose.jpg");
# size = im.shape

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
    _, frame = cap.read()
    size = frame.shape
    # We actually Convert to grayscale conversion
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)  # ; print(faces)

    # Camera internals
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)

    # 2D image points. If you change the image, you need to change vector
    # image_points = np.array([
    #     (435, 250),  # Nose tip
    #     (448, 307),  # Chin
    #     (411, 227),  # Left eye left corner
    #     (489, 215),  # Right eye right corne
    #     (428, 276),  # Left Mouth corner
    #     (473, 268)  # Right mouth corner
    # ], dtype="double")


    for face in faces:
        # The face landmarks code begins from here
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        # Then we can also do cv2.rectangle function (frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        landmarks = predictor(gray, face)

        # We are then accesing the landmark points
        i = [33, 8, 36, 45, 48, 54] #Nose tip, Chin, Left eye corner, Right eye corner, Left mouth corner, right mouth corner
        image_points = []
        for n in i:
            x = landmarks.part(n).x
            y = landmarks.part(n).y;
            # image_points = np.array([(x,y)], dtype="double")
            image_points += [(x,y)]
            cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

        image_points = np.array(image_points, dtype="double")
        # print(image_points)
        print("Camera Matrix :\n {0}".format(cam_matrix))

        dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,
                                                                      cam_matrix,dist_coeffs,
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


        cv2.line(frame, p1, p2, (255, 0, 0), 2)
    #
    # # Display image

    cv2.imshow("Output", frame)
    cv2.waitKey(1);