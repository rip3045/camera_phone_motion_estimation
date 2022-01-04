import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)

while(True):
    ret1, frame1 = cap1.read()

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    cv2.imshow('camera', cv2.resize(gray1, (300,300)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()