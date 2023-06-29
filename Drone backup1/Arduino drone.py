from Arduino import Arduino
from time import sleep
import time
import pygame as pg
from mpu6050 import mpu6050

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
def speeder2(x,in_min=0,in_max=10,out_min=1100,out_max=2200):
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

def pid(currtime,previousTime,err,lasterr,Kp,Kd):
    etime = currtime-previousTime               
    rateError = (err-lasterr)/etime   
    pid = (Kp*err)+(Kd*rateError)
    print(int((Kp*err)*100)/100,int((Kd*rateError)*100)/100,int(pid*100)/100)
    return pid
        
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

arduino.Servos.attach(m1, min=1000, max=2100)
arduino.Servos.attach(m2, min=1100, max=2200)
arduino.Servos.attach(m3, min=1000, max=2100)
arduino.Servos.attach(m4, min=1000, max=2100)

previousTime = 0
lasterrx = 0
lasterry = 0
Kp = 0
Kd = 0
Kpx = Kp
Kdx = Kd
Kpy = Kp
Kdy = Kd
stime = time.time()

arduino.Servos.writeMicroseconds(m1,speeder(0))
arduino.Servos.writeMicroseconds(m2,speeder(0))
arduino.Servos.writeMicroseconds(m3,speeder(0))
arduino.Servos.writeMicroseconds(m4,speeder(0))

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
    currtime = int(round((time.time()-stime)*1000))
    errx = gyro['x']
    erry = gyro['y']
    pidx = pid(currtime,previousTime,errx,lasterrx,Kpx,Kdx)
    pidy = pid(currtime,previousTime,erry,lasterry,Kpy,Kdy)
    pidx = int(pidx*10000)/10000
    pidy = int(pidy*10000)/10000
    lasterrx = errx
    lasterry = erry 
    previousTime = currtime
#########################################################################
    if tspeed == 0:
        pass
    else:
        if pidx > 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 - abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx) + abs(pidy)))
        elif pidx < 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 + abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx) + abs(pidy)))
        elif pidx < 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 + abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx) - abs(pidy)))
        elif pidx > 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx) - abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 - abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx) + abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx) - abs(pidy)))
        elif pidx > 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidx)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 - abs(pidx)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidx)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidx)))
        elif pidx < 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidx)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 + abs(pidx)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidx)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidx)))
        elif pidx == 0 and pidy > 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 + abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 - abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 - abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 + abs(pidy)))
        elif pidx == 0 and pidy < 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1 - abs(pidy)))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2 + abs(pidy)))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3 + abs(pidy)))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4 - abs(pidy)))
        elif pidx == 0 and pidy == 0:
            arduino.Servos.writeMicroseconds(m1, speeder(tspeed + speed1))
            arduino.Servos.writeMicroseconds(m2, speeder2(tspeed + speed2))
            arduino.Servos.writeMicroseconds(m3, speeder(tspeed + speed3))
            arduino.Servos.writeMicroseconds(m4, speeder(tspeed + speed4))
#########################################################################
    #print(tspeed)
    #sleep(0.05)

