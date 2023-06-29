from gpiozero import Servo
from time import sleep
import time
import pygame as pg
from mpu6050 import mpu6050

sensor = mpu6050(0x68)

pg.init()
window = pg.display.set_mode([20,20])
pg.display.update()

mt1 = Servo(26)
mt2 = Servo(16)
mt3 = Servo(20)
mt4 = Servo(21)

speed1 = -1
speed2 = -1
speed3 = -1
speed4 = -1
previousTime = 0
lasterrx = 0
lasterry = 0
Kp = 0.003
Kd = 0.001
stime = time.time()



mt1.value = -1
mt2.value = -1
mt3.value = -1
mt4.value = -1
sleep(1)

def pid(currtime,previousTime,err,lasterr,Kp,Kd):
    etime = currtime-previousTime               
    rateError = (err-lasterr)/etime   
    pid = (Kp*err)+(Kd*rateError)
    return pid
def speeder(speed):
    if speed >= 1:
        speed = 1
    if speed <= -1:
        speed = -1
    return speed

while True:
    gyro = sensor.get_accel_data()
#########################################################################
    for event in pg.event.get():
        msg = ""
        if event.type == pg.KEYDOWN:
####################################################
            if event.key == pg.K_i:
                msg = "Speed-up"
                speed1 = speed1 + 0.1
                if speed1 >= 1:
                    speed1 = 1
                speed2 = speed2 + 0.1
                if speed2 >= 1:
                    speed2 = 1
                speed3 = speed3 + 0.1
                if speed3 >= 1:
                    speed3 = 1
                speed4 = speed4 + 0.1
                if speed4 >= 1:
                    speed4 = 1  

            elif event.key == pg.K_k:
                msg = "Speed-down"
                speed1 = speed1 - 0.1                  
                if speed1 <= -1:
                    speed1 = -1
                speed2 = speed2 - 0.1                  
                if speed2 <= -1:
                    speed2 = -1
                speed3 = speed3 - 0.1                  
                if speed3 <= -1:
                    speed3 = -1
                speed4 = speed4 - 0.1                  
                if speed4 <= -1:
                    speed4 = -1
####################################################
        elif event.type == pg.QUIT:
            msg = "Exiting!"
            pg.quit()
            break
        elif event.type == pg.KEYUP:
            pass
        print(msg)   
#########################################################################
    currtime = int(round((time.time()-stime)*1000))
    errx = gyro['x']
    erry = gyro['y']
    pidx = pid(currtime,previousTime,errx,lasterrx,Kp,Kd)
    pidy = pid(currtime,previousTime,erry,lasterry,Kp,Kd)
    pidx = int(pidx*1000)/1000
    pidy = int(pidy*1000)/1000
    lasterrx = errx
    lasterry = erry 
    previousTime = currtime
#############################################  
    speed1 = int(speed1*1000)/1000
    speed2 = int(speed2*1000)/1000
    speed3 = int(speed3*1000)/1000
    speed4 = int(speed4*1000)/1000
#############################################
    if pidx > 0:
        speed1 = speed1 - abs(pidx)
        speed2 = speed2 - abs(pidx)
        speed3 = speed3 + abs(pidx)
        speed4 = speed4 + abs(pidx)
    elif pidx < 0:
        speed1 = speed1 + abs(pidx)
        speed2 = speed2 + abs(pidx)
        speed3 = speed3 - abs(pidx)
        speed4 = speed4 - abs(pidx)
    if pidy > 0:
        speed1 = speed1 + abs(pidy)
        speed2 = speed2 - abs(pidy)
        speed3 = speed3 - abs(pidy)
        speed4 = speed4 + abs(pidy)
    elif pidy < 0:
        speed1 = speed1 - abs(pidy)
        speed2 = speed2 + abs(pidy)
        speed3 = speed3 + abs(pidy)
        speed4 = speed4 - abs(pidy)
######################
    speed1 = speeder(speed1)
    speed2 = speeder(speed2)
    speed3 = speeder(speed3)
    speed4 = speeder(speed4)
##########
    mt1.value = speed1
    mt2.value = speed2
    mt3.value = speed3
    mt4.value = speed4
    
    print(pidx,pidy)
    #sleep(0.05)

