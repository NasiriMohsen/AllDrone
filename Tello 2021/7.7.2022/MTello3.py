import sys
import traceback
import tellopy
import av
import cv2 as cv
import numpy
import time
import keyboard
from threading import Thread

class Mohsen_Tello():
    def EmergencyStopCheck(self):
        if keyboard.is_pressed("esc"):
            print("Emergency Stop! ")
            self.drone.up(0)
            self.drone.down(0)
            self.drone.clockwise(0)
            self.drone.counter_clockwise(0)
            self.drone.forward(0)
            self.drone.backward(0)
            self.drone.right(0)
            self.drone.left(0)
            self.drone.land()
            print("Exiting program... ")
            self.drone.quit()

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
        self.frame = []
        self.frame_skip = 100
        self.frame_container = None
        self.drone = tellopy.Tello()
        self.AltitudeLimit = 0
        self.AttitudeLimit = 0
        self.LowBatteryThreshold = 0
        self.Exposure = 0
        self.VideoMode = False

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
            
            #self.drone.set_alt_limit(2)
            #self.drone.set_low_bat_threshold(25)
            self.drone.fast_mode = True
            self.drone.set_exposure(self.Exposure)
            self.drone.set_video_mode(self.VideoMode)
            #self.drone.set_video_encoder_rate()
            

        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)

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

    def Keyboard_Control(self):

        def SpeedIncrease():
            self.speed = self.speed + 10
            if self.speed >= 100:
                self.speed = 100
            print(" Keyboard Event: "+" 8 "+" | Speed Increase! "+" Speed = "+str(self.speed))
        def SpeedDecrease():
            self.speed = self.speed - 10
            if self.speed <= 30:
                self.speed = 30
            print(" Keyboard Event: "+" 2 "+" | Speed Decrease! "+" Speed = "+str(self.speed))

        def ExposureMode():
            self.Exposure = self.Exposure + 1
            if self.Exposure == 3:
                self.Exposure = 0
            self.drone.set_exposure(self.Exposure)
            print(" Keyboard Event: "+" 0 "+" | Changing Exposure Mode "+" Exposure = "+str(self.Exposure))        
        def CameraMode():
            self.VideoMode = not self.VideoMode
            self.drone.set_video_mode(self.VideoMode)
            print(" Keyboard Event: "+" 9 "+" | Changing Camera Mode "+" Mode = "+str(int(self.VideoMode)))

        def MissionMode():
            time.sleep(0.5)
            self.Mission_mode = not self.Mission_mode
            print(" Keyboard Event: "+" m "+" | Mission mode Activated! "+" Mission = "+str(self.Mission_mode))
        
        def TakePic():
            cv.imwrite('C:/Users/mohse/Pictures/Tello/P'+ str(time.time()) + '.jpg', self.frame) 
            print(" Keyboard Event: "+" p "+" | Taking a Picture! "+" C:/Users/mohse/Pictures/Tello/P ")
        def RecordVid():
            time.sleep(0.5)
            if self.Record_video:
                self.Record_video = False
                self.Videoout.release()
                print(" Keyboard Event: "+" r "+" | Stoped Recording Video! "+" Record = "+str(self.Record_video))
            else:
                self.Record_video = True
                self.Videoout = cv.VideoWriter('C:/Users/mohse/Pictures/Tello/V'+ str(time.time()) + '.avi',cv.VideoWriter_fourcc(*'MJPG'),self.FPS,self.frame_size)
                print(" Keyboard Event: "+" r "+" | Started Recording Video! "+" Record = "+str(self.Record_video))
        
        def PalmLand():
            self.drone.palm_land()
            print(" Keyboard Event: "+" Backspace "+" | Palm Landing Drone! ")
        def Land():
            self.drone.land()
            print(" Keyboard Event: "+" L "+" | Landing Drone! ")
            time.sleep(1)
        def TakeOff():
            self.drone.takeoff()
            print(" Keyboard Event: "+" T "+" | Drone Taking off! ")
            time.sleep(1)
        def TakeOffThrow():
            self.drone.throw_and_go()
            print(" Keyboard Event: "+" Tab "+" | Throw Drone to Take off! ")
            time.sleep(1)
        
        def IncreaseAlt(x):
            self.drone.up(self.speed)
            print(" Keyboard Event: "+" Space "+" | Increasing Altitude! ")
        def DecreaseAlt(x):
            self.drone.down(self.speed)
            print(" Keyboard Event: "+" Shift "+" | Decreasing Altitude! ")
        
        def RotateClockwise(x):
            self.drone.clockwise(self.speed)
            print(" Keyboard Event: "+" E "+" | Rotating Clockwise! ")
        def RotateAntiClockwise(x):
            self.drone.counter_clockwise(self.speed)
            print(" Keyboard Event: "+" Q "+" | Rotating AntiClockwise! ")
            
        def Forward(x):
            self.drone.forward(self.speed)
            print(" Keyboard Event: "+" W "+" | Drone going Forward! ")
        def Backward(x):
            self.drone.backward(self.speed)
            print(" Keyboard Event: "+" S "+" | Drone going Backward! ")
        def Right(x):
            self.drone.right(self.speed)
            print(" Keyboard Event: "+" D "+" | Drone going Right! ")
        def Left(x):
            self.drone.left(self.speed)
            print(" Keyboard Event: "+" A "+" | Drone going Left! ")

        def flip_back():
            self.drone.flip_back()
            print(" Keyboard Event: "+" F + S "+" | Drone Flip Backward! ")
        def flip_backleft():
            self.drone.flip_backleft()
            print(" Keyboard Event: "+" F + Z "+" | Drone Flip Backward Left! ")
        def flip_backright():
            self.drone.flip_backright()
            print(" Keyboard Event: "+" F + C "+" | Drone Flip Backward Right! ")
        def flip_forward():    
            self.drone.flip_forward()
            print(" Keyboard Event: "+" F + W "+" | Drone Flip Forward! ")
        def flip_forwardleft():    
            self.drone.flip_forwardleft()
            print(" Keyboard Event: "+" F + Q"+" | Drone Flip Forward Left! ")
        def flip_forwardright():    
            self.drone.flip_forwardright()
            print(" Keyboard Event: "+" F + E "+" | Drone Flip Forward Right! ")      
        def flip_left():    
            self.drone.flip_left()
            print(" Keyboard Event: "+" F + A "+" | Drone Flip Left! ")
        def flip_right():   
            self.drone.flip_right()
            print(" Keyboard Event: "+" F + D "+" | Drone Flip Right! ")
        
        def Release_IncreaseAlt(x):
            self.drone.up(0)
        def Release_DecreaseAlt(x):
            self.drone.down(0)
        def Release_RotateClockwise(x):
            self.drone.clockwise(0)
        def Release_RotateAntiClockwise(x):
            self.drone.counter_clockwise(0)
        def Release_Forward(x):
            self.drone.forward(0)
        def Release_Backward(x):
            self.drone.backward(0)
        def Release_Right(x):
            self.drone.right(0)
        def Release_Left(x):
            self.drone.left(0)

        keyboard.add_hotkey("8", SpeedIncrease)
        keyboard.add_hotkey("2", SpeedDecrease)

        keyboard.add_hotkey("0", ExposureMode)
        keyboard.add_hotkey("9", CameraMode)

        keyboard.add_hotkey("m", MissionMode)
        
        keyboard.add_hotkey("p", TakePic)
        keyboard.add_hotkey("r", RecordVid)

        keyboard.add_hotkey("tab", TakeOffThrow)
        keyboard.add_hotkey("t", TakeOff)
        keyboard.add_hotkey("l", Land)
        keyboard.add_hotkey("backspace", PalmLand)

        keyboard.add_hotkey("f+w",flip_forward)
        keyboard.add_hotkey("f+a",flip_left)
        keyboard.add_hotkey("f+s",flip_back)
        keyboard.add_hotkey("f+d",flip_right)
        keyboard.add_hotkey("f+z",flip_backleft)
        keyboard.add_hotkey("f+c",flip_backright)
        keyboard.add_hotkey("f+q",flip_forwardleft)
        keyboard.add_hotkey("f+e",flip_forwardright)

        keyboard.on_press_key("space",IncreaseAlt)
        keyboard.on_release_key("space",Release_IncreaseAlt)
        keyboard.on_press_key("shift", DecreaseAlt)
        keyboard.on_release_key("shift", Release_DecreaseAlt)
        keyboard.on_press_key("e", RotateClockwise)
        keyboard.on_release_key("e", Release_RotateClockwise)
        keyboard.on_press_key("q", RotateAntiClockwise)
        keyboard.on_release_key("q", Release_RotateAntiClockwise)

        keyboard.on_press_key("w", Forward)
        keyboard.on_release_key("w", Release_Forward)
        keyboard.on_press_key("a", Left)
        keyboard.on_release_key("a", Release_Left)
        keyboard.on_press_key("s", Backward)
        keyboard.on_release_key("s", Release_Backward)
        keyboard.on_press_key("d", Right)
        keyboard.on_release_key("d", Release_Right)