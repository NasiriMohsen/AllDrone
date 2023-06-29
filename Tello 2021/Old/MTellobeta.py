import sys
import traceback
import tellopy
import av
import cv2 as cv
import numpy
import time

class Mohsen_Tello():
    def flightDataHandler(self,event, sender, data):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            print(data)

    def __init__(self):
        retry = 3
        self.frame_skip = 300
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
        self.drone.quit()

    def Cap_Webcam(self):
        for Raw_frame in self.frame_container.decode(video=0):
            if 0 < self.frame_skip:
                self.frame_skip = self.frame_skip - 1
                continue
            
            start_time = time.time()
            #################Image Proccesing goes here#############
            frame = cv.cvtColor(numpy.array(Raw_frame.to_image()),cv.COLOR_RGB2BGR)
            #################Image Proccesing ends here#############
           #Recalculate the frame-skip-rate
            if Raw_frame.time_base < 1.0/60:
                time_base = 1.0/60
            else:
                time_base = Raw_frame.time_base
            self.frame_skip = int((time.time() - start_time)/time_base)
            return frame
