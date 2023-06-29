import MTello
import cv2 as cv

Tello = MTello.Mohsen_Tello()

while True:
    frame = Tello.Cap_Webcam()

    cv.imshow("Frame",frame)
    Key = cv.waitKey(1)
    if 27 == Key:
        Tello.ExitAll()
        cv.destroyAllWindows()