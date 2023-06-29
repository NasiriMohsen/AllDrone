import MTello3
import cv2 as cv

Tello = MTello3.Mohsen_Tello()
Tello.Keyboard_Control()

while True:
    Tello.EmergencyStopCheck()
    frame = Tello.Cap_Webcam()

    cv.imshow("Frame",frame)
    Key = cv.waitKey(1)
    if 27 == Key:
        cv.destroyAllWindows()







