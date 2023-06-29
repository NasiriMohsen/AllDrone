import sys
import traceback
import tellopy
import av
import cv2 as cv
import numpy
import time
import keyboard

class Mohsen_Tello():
    def flightDataHandler(self,event, sender, data):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            print(data)

    def __init__(self):
        self.speed = 65
        self.Mission_mode = False
        self.FPS = 30
        self.Record_video = False
        self.Videoout = None
        retry = 3
        self.frame_skip = 100
        self.frame_container = None
        self.drone = tellopy.Tello()

        try:
            self.drone.connect()
            self.drone.wait_for_connection(60.0)
            self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.flightDataHandler)

            while self.frame_container is None and 0 < retry:
                retry -= 1
                try:
                    self.frame_container = av.open(self.drone.get_video_stream())
                except av.AVError as ave:
                    print(ave)
                    print('Stream Error! retrying... ')

        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)

    def ExitAll(self):
        print("Exiting program... ")
        self.drone.land()
        time.sleep(1)
        self.drone.quit()

    def Cap_Webcam(self):
        for Raw_frame in self.frame_container.decode(video=0):
            if 0 < self.frame_skip:
                self.frame_skip = self.frame_skip - 1
                continue
            
            start_time = time.time()
            #################Image Proccesing goes here#############
            self.frame = cv.cvtColor(numpy.array(Raw_frame.to_image()),cv.COLOR_RGB2BGR)
            

            frame_width = int(len(self.frame))
            frame_height = int(len(self.frame[0]))
            self.frame_size = (frame_width,frame_height)
            if self.Record_video:
                self.Videoout.write(self.frame)
            #################Image Proccesing ends here#############
           #Recalculate the frame-skip-rate
            if Raw_frame.time_base < 1.0/60:
                time_base = 1.0/60
            else:
                time_base = Raw_frame.time_base
            self.frame_skip = int((time.time() - start_time)/time_base)
            return self.frame


    def Opencv_Keyboard_Control(self,Input):
        #Doesnt work Well !!!
        if Input == ord("8"):
            self.speed = self.speed + 10
            if self.speed >= 100:
                self.speed = 100
        elif Input == ord("2"):
            self.speed = self.speed - 10
            if self.speed <= 30:
                self.speed = 30
        elif Input == 27:
            self.drone.land()
            self.ExitAll()
            time.sleep(1)
        elif Input == ord("l") or Input == 8:
            self.drone.land()
            time.sleep(1)
        elif Input == ord("t") or Input == 9:
            self.drone.takeoff()
            time.sleep(1)
        elif Input == ord(" "):
            self.drone.up(self.speed)
            time.sleep(0.01)
        elif Input == 14 or Input == 15:
            self.drone.down(self.speed)
            time.sleep(0.01)
        elif Input == ord("e"):
            self.drone.clockwise(self.speed)
            time.sleep(0.01)
        elif Input == ord("q"):
            self.drone.counter_clockwise(self.speed)
            time.sleep(0.01)
        elif Input == ord("w"):
            self.drone.forward(self.speed)
            time.sleep(0.01)
        elif Input == ord("s"):
            self.drone.backward(self.speed)
            time.sleep(0.01)
        elif Input == ord("d"):
            self.drone.right(self.speed)
            time.sleep(0.01)
        elif Input == ord("a"):
            self.drone.left(self.speed)
            time.sleep(0.01)
        else:
            self.drone.up(0)
            self.drone.down(0)
            self.drone.clockwise(0)
            self.drone.counter_clockwise(0)
            self.drone.forward(0)
            self.drone.backward(0)
            self.drone.right(0)
            self.drone.left(0)

    def Keyboard_Control(self):
        if keyboard.is_pressed("8"):
            self.speed = self.speed + 10
            if self.speed >= 100:
                self.speed = 100
        elif keyboard.is_pressed("2"):
            self.speed = self.speed - 10
            if self.speed <= 30:
                self.speed = 30
        elif keyboard.is_pressed("m"):
            self.Mission_mode = not self.Mission_mode
        elif keyboard.is_pressed("p"):
            cv.imwrite('C:/Users/mohse/Pictures/Tello/P'+ str(time.time()) + '.jpg', self.frame) 
        elif keyboard.is_pressed("r"):
            if self.Record_video:
                self.Record_video = False
                self.Videoout.release()
            else:
                self.Record_video = True
                self.Videoout = cv.VideoWriter('C:/Users/mohse/Pictures/Tello/V'+ str(time.time()) + '.avi',cv.VideoWriter_fourcc(*'MJPG'),self.FPS,self.frame_size)
        elif keyboard.is_pressed("esc"):
            self.drone.land()
            self.ExitAll()
            time.sleep(1)
        elif keyboard.is_pressed("l") or keyboard.is_pressed("backspace"):
            self.drone.land()
            time.sleep(1)
        elif keyboard.is_pressed("t") or keyboard.is_pressed("tab"):
            self.drone.takeoff()
            time.sleep(1)
        elif keyboard.is_pressed("space"):
            self.drone.up(self.speed)
        elif keyboard.is_pressed("shift"):
            self.drone.down(self.speed)
        elif keyboard.is_pressed("e"):
            self.drone.clockwise(self.speed)
        elif keyboard.is_pressed("q"):
            self.drone.counter_clockwise(self.speed)
        elif keyboard.is_pressed("w"):
            self.drone.forward(self.speed)
        elif keyboard.is_pressed("s"):
            self.drone.backward(self.speed)
        elif keyboard.is_pressed("d"):
            self.drone.right(self.speed)
        elif keyboard.is_pressed("a"):
            self.drone.left(self.speed)
        else:
            self.drone.up(0)
            self.drone.down(0)
            self.drone.clockwise(0)
            self.drone.counter_clockwise(0)
            self.drone.forward(0)
            self.drone.backward(0)
            self.drone.right(0)
            self.drone.left(0)

