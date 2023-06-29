from Arduino import Arduino
from time import sleep
import pygame as pg
from mpu6050 import mpu6050
#############################################################################################################
def speeder(x,in_min=0,in_max=10,out_min=1000,out_max=2100):
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
arduino = Arduino()

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
min2 = 1165
min3 = 1045
min4 = 1005

max1 = 2000
max2 = 2165
max3 = 2045
max4 = 2005

lastix = 0
lastiy = 0
lasterrx = 0
lasterry = 0

Kp = 0
Kd = 0
Ki = 0

Kpx = 0
Kix = 0
Kdx = 0
Kpy = Kp
Kiy = Ki
Kdy = Kd

arduino.Servos.attach(m1, min=min1, max=max1)
arduino.Servos.attach(m2, min=min2, max=max2)
arduino.Servos.attach(m3, min=min3, max=max3)
arduino.Servos.attach(m4, min=min4, max=max4)

arduino.Servos.writeMicroseconds(m1,speeder(0,out_min=min1,out_max=max1))
arduino.Servos.writeMicroseconds(m2,speeder(0,out_min=min2,out_max=max2))
arduino.Servos.writeMicroseconds(m3,speeder(0,out_min=min3,out_max=max3))
arduino.Servos.writeMicroseconds(m4,speeder(0,out_min=min4,out_max=max4))
#############################################################################################################
while True:
    gyro = sensor.get_accel_data()
    #gyro = {'x':0,'y':0}
    #sleep(0.001)
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
        pass
    else:
        if pidx > 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx) + abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 - abs(pidx) - abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx) - abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx) + abs(pidy),out_min=min4,out_max=max4))
        elif pidx < 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx) + abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 + abs(pidx) - abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx) - abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx) + abs(pidy),out_min=min4,out_max=max4))
        elif pidx < 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx) - abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 + abs(pidx) + abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx) + abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx) - abs(pidy),out_min=min4,out_max=max4))
        elif pidx > 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx) - abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 - abs(pidx) + abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx) + abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx) - abs(pidy),out_min=min4,out_max=max4))
        elif pidx > 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 - abs(pidx),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx),out_min=min4,out_max=max4))
        elif pidx < 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 + abs(pidx),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx),out_min=min4,out_max=max4))
        elif pidx == 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 - abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidy),out_min=min4,out_max=max4))
        elif pidx == 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidy),out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2 + abs(pidy),out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidy),out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidy),out_min=min4,out_max=max4))
        elif pidx == 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1,out_min=min1,out_max=max1))
            arduino.Servos.writeMicroseconds(m2, speeder(tspeed + speed2,out_min=min2,out_max=max2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3,out_min=min3,out_max=max3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4,out_min=min4,out_max=max4))
#########################################################################
    #print(tspeed)
    #sleep(0.05)

