import sys
import traceback
import tellopy
import av
import cv2 as cv
import numpy
import time
#################################################################
retry = 3
frame_container = None
frame_skip = 100
#################################################################
drone = tellopy.Tello()
#################################################################

try:
    drone.connect()
    drone.wait_for_connection(60.0)
    
   #Try to get stream
    while frame_container is None and 0 < retry:
        retry -= 1
        try:
            frame_container = av.open( drone.get_video_stream() )
        except av.AVError as ave:
            print(ave)
            print('Stream Error! retrying... ')

   #Skip first frames for a better accuracy
    while True:
        for Raw_frame in frame_container.decode(video=0):
            if 0 < frame_skip:
                frame_skip = frame_skip - 1
                continue

            start_time = time.time()

            #################Image Proccesing goes here#############
            frame = cv.cvtColor(numpy.array(Raw_frame.to_image()),cv.COLOR_RGB2BGR)
            
            cv.imshow('Original',frame)            
            cv.waitKey(1)
            #################Image Proccesing ends here#############
            
           #Recalculate the frame-skip-rate
            if Raw_frame.time_base < 1.0/60:
                time_base = 1.0/60
            else:
                time_base = Raw_frame.time_base
            frame_skip = int((time.time() - start_time)/time_base)
                
except Exception as ex:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print(ex)

finally:
    print("Exiting program... ")
    drone.quit()
    cv.destroyAllWindows()
