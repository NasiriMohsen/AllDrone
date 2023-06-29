from time import sleep
import pygame as pg
import Quadcopter
from mpu6050 import mpu6050

#############################################################################################################
def speeder(x,out_min,out_max,in_min=0,in_max=10):
    if x >= in_max:
        x = in_max
    if x <= in_min:
        x = in_min
    speed = (x-in_min)*(out_max-out_min)/(in_max - in_min)+out_min
    if speed >= out_max:
        speed = out_max
    if speed <= out_min:
        speed = out_min
    return speed

def pid(lasti,err,lasterr,p,i,d):
    P = p*err
    I = (i*err)+lasti
    D = d*(err-lasterr)  
    pid = (P+I+D)/100
    print((int(P*100)/100),(int(I*100)/100),(int(D*100)/100),(int(pid*100)/100))
    return pid,I
#############################################################################################################      
sensor = mpu6050(0x68)
pg.init()
window = pg.display.set_mode([20,20])
pg.display.update()
motors = Quadcopter.Motors()

m1 = 5
m2 = 6
m3 = 10
m4 = 11

tspeed = 0
speed1 = 0
speed2 = 0
speed3 = 0
speed4 = 0

min1 = 1000
min2 = 1000
min3 = 1000
min4 = 1000

max1 = 2000
max2 = 2000
max3 = 2000
max4 = 2000

lastix = 0
lastiy = 0
lasterrx = 0
lasterry = 0
############################################## 
Kp = 0
Kd = 0
Ki = 0

Kpx = 0
Kix = 0
Kdx = 0
Kpy = Kp
Kiy = Ki
Kdy = Kd
##############################################
motors.position(1000,1000,1000,1000)
#############################################################################################################
while True:
#########################################################################
    for event in pg.event.get():
        msg = ""
        if event.type == pg.KEYDOWN:
        #######################################
            if event.key == pg.K_i:
                msg = "Speed-up"
                tspeed = tspeed + 0.5
                if tspeed >= 10:
                    tspeed = 10

            elif event.key == pg.K_k:
                msg = "Speed-down"
                tspeed = tspeed - 0.5                  
                if tspeed <= 0:
                    tspeed = 0
        #######################################
        elif event.type == pg.QUIT:
            msg = "Exiting!"
            pg.quit()
            break
        elif event.type == pg.KEYUP:
            pass
        print(msg)   
#########################################################################
    gyro = sensor.get_accel_data()
    errx = gyro['x']
    erry = gyro['y']
    pidxx = pid(lastix,errx,lasterrx,Kpx,Kix,Kdx)
    pidyy = pid(lastiy,erry,lasterry,Kpy,Kiy,Kdy)
    pidx = int(pidxx[0]*10000)/10000
    pidy = int(pidyy[0]*10000)/10000
    lastix = pidxx[1]
    lastiy = pidyy[1]
    lasterrx = errx
    lasterry = erry 
#########################################################################
    if tspeed == 0:
        motors.position(
            speeder(tspeed + speed1,out_min=min1,out_max=max1),
            speeder(tspeed + speed2,out_min=min2,out_max=max2),
            speeder(tspeed + speed3,out_min=min3,out_max=max3),
            speeder(tspeed + speed4,out_min=min4,out_max=max4))
    else:
        motors.position(
            speeder(tspeed + speed1 - pidx + pidy,out_min=min1,out_max=max1),
            speeder(tspeed + speed2 - pidx - pidy,out_min=min2,out_max=max2),
            speeder(tspeed + speed3 + pidx - pidy,out_min=min3,out_max=max3),
            speeder(tspeed + speed4 + pidx + pidy,out_min=min4,out_max=max4))
        
        
        
        


