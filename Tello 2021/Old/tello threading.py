import MTello2
import cv2 as cv
from threading import Thread

Tello = MTello2.Mohsen_Tello()

Tello.Keyboard_Control()

while True:
    frame = Tello.Cap_Webcam()

    cv.imshow("Frame",frame)
    Key = cv.waitKey(1)
    if 27 == Key:
        Tello.ExitAll()
        cv.destroyAllWindows()







