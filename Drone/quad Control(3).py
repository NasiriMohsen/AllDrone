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
    return int(speed)

def pid(lasti,err,lasterr,p,i,d):
    P = p*err
    I = (i*err)+lasti
    D = d*(err-lasterr)  
    pid = (P+I+D)/100
    #print((int(P*100)/100),(int(I*100)/100),(int(D*100)/100),(int(pid*100)/100))
    return pid,I
#############################################################################################################      
sensor = mpu6050(0x68)
pg.init()
window = pg.display.set_mode([20,20])
pg.display.update()
motors = Quadcopter.Motors()

wait = 0.05

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
xslope = 0
yslope = 0
yangle = 2.5
xangle = 2.5

Kp = 3
Ki = 0.25
Kd = 2.5

Kpx = Kp
Kix = Ki
Kdx = Kd
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
            
            if event.key == pg.K_u:
                msg = "PIDy P increase"
                Kpy = kpy + 0.1

            elif event.key == pg.K_j:
                msg = "PIDy P decrease"
                Kpy = kpy - 0.1

            if event.key == pg.K_y:
                msg = "PIDx P increase"
                Kpx = kpx + 0.1

            elif event.key == pg.K_h:
                msg = "PIDx P decrease"
                Kpx = kpx - 0.1

            if event.key == pg.K_o:
                msg = "PIDy D increase"
                Kdy = kdy + 0.1

            elif event.key == pg.K_l:
                msg = "PIDy D decrease"
                Kdy = kdy - 0.1

            if event.key == pg.K_p:
                msg = "PIDx D increase"
                Kdx = kdx + 0.1

            elif event.key == pg.K_;:
                msg = "PIDx D decrease"
                Kdx = kdx - 0.1

            if event.key == pg.K_w:
                msg = "Forward"
                yslope = yangle

            elif event.key == pg.K_s:
                msg = "Backward"
                yslope = -yangle

            if event.key == pg.K_d:
                msg = "Right"
                xslope = xangle

            elif event.key == pg.K_a:
                msg = "Left"
                xslope = -xangle
                
        #######################################
        elif event.type == pg.QUIT:
            msg = "Exiting!"
            pg.quit()
            break
        elif event.type == pg.KEYUP:
            if (event.key == pg.K_a or event.key == pg.K_d):
                xslope = 0
            if (event.key == pg.K_s or event.key == pg.K_w):
                yslope = 0
        print(msg)   
#########################################################################
    if tspeed == 0:
        motors.position(
            speeder(tspeed + speed1,out_min=min1,out_max=max1),
            speeder(tspeed + speed2,out_min=min2,out_max=max2),
            speeder(tspeed + speed3,out_min=min3,out_max=max3),
            speeder(tspeed + speed4,out_min=min4,out_max=max4),
            t=wait)
    else:
        gyro = sensor.get_accel_data()
        errx = gyro['x'] + xslope
        erry = gyro['y'] + yslope
        print(xslope,yslope)
        pidxx = pid(lastix,errx,lasterrx,Kpx,Kix,Kdx)
        pidyy = pid(lastiy,erry,lasterry,Kpy,Kiy,Kdy)
        pidx = int(pidxx[0]*10000)/10000
        pidy = int(pidyy[0]*10000)/10000
        lastix = pidxx[1]
        lastiy = pidyy[1]
        lasterrx = errx
        lasterry = erry 
        motors.position(
            speeder(tspeed + speed1 - pidx + pidy,out_min=min1,out_max=max1),
            speeder(tspeed + speed2 - pidx - pidy,out_min=min2,out_max=max2),
            speeder(tspeed + speed3 + pidx - pidy,out_min=min3,out_max=max3),
            speeder(tspeed + speed4 + pidx + pidy,out_min=min4,out_max=max4),
            t=wait)
        
        
        
        


