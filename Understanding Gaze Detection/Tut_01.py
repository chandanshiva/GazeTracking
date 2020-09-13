import cv2
print("Package imported")
import numpy as np

#img = cv2.imread("Resources/img.jpeg")
#cv2.imshow("output",img)
#cv2.waitKey(0)

#cap = cv2.VideoCapture("Resources/vid.mp4")

#while True:
 #   success, img = cap.read()
  #  cv2.imshow("Video",img)
   # if cv2.waitKey(1) & 0xFF ==ord('q'):
    #    break

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
