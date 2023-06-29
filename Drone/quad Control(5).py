from time import sleep
import time
import pygame as pg
import Quadcopter
import Gyroscope

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

def pid(currtime,previousTime,lasti,err,lasterr,p,i,d):
    xm = 600
    ym = 3
    etime = currtime - previousTime 
    P = p*err
    if -ym < err and err < ym:
        I = i*((etime*err)+lasti)
    else :
        I = 0
    D = d*((err-lasterr)/etime)  
    pid = (P+I+D)
    if pid > xm:
        pid = xm
    if pid < -xm:
        pid = -xm
    #print((int(P*100)/100),(int(I*100)/100),(int(D*100)/100),(int(pid*100)/100))
    return pid,I
#############################################################################################################      
Gyro = Gyroscope.gyro()
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
previoustimex = 0
previoustimey = 0
stime = time.time()
############################################## 
xslope = 0
yslope = 0
zslope = 0
yangle = 5
xangle = 5

Kp = 0
Ki = 0
Kd = 10

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
                Kpy = int((Kpy + 1)*100)/100

            elif event.key == pg.K_j:
                msg = "PIDy P decrease"
                Kpy = int((Kpy - 1)*100)/100

            if event.key == pg.K_y:
                msg = "PIDx P increase"
                Kpx = int((Kpx + 0.1)*100)/100

            elif event.key == pg.K_h:
                msg = "PIDx P decrease"
                Kpx = int((Kpx - 0.1)*100)/100

            if event.key == pg.K_m:
                msg = "PIDy D increase"
                Kdy = int((Kdy + 1)*100)/100

            elif event.key == pg.K_n:
                msg = "PIDy D decrease"
                Kdy = int((Kdy - 1)*100)/100

            if event.key == pg.K_b:
                msg = "PIDx D increase"
                Kdx = int((Kdx + 0.1)*100)/100

            elif event.key == pg.K_v:
                msg = "PIDx D decrease"
                Kdx = int((Kdx - 0.1)*100)/100

            if event.key == pg.K_w:
                msg = "Forward"
                yslope = -yangle

            elif event.key == pg.K_s:
                msg = "Backward"
                yslope = yangle

            if event.key == pg.K_d:
                msg = "Right"
                xslope = -xangle

            elif event.key == pg.K_a:
                msg = "Left"
                xslope = xangle
                
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
    print(Kpy,Kdy)
    if tspeed == 0:
        motors.position(
            speeder(tspeed + speed1,out_min=min1,out_max=max1),
            speeder(tspeed + speed2,out_min=min2,out_max=max2),
            speeder(tspeed + speed3,out_min=min3,out_max=max3),
            speeder(tspeed + speed4,out_min=min4,out_max=max4),
            t=wait)
    else:
        dgyro = Gyro.gyrodata()
        errx = dgyro['x'] - xslopes
        erry = dgyro['y'] - yslope
        errz = dgyro['z'] - zslope
        currtimex = int(round((time.time()-stime)*1000))
        pidxx = pid(currtimex,previoustimex,lastix,errx,lasterrx,Kpy,Kiy,Kdy)
        currtimey = int(round((time.time()-stime)*1000))
        pidyy = pid(currtimey,previoustimey,lastiy,erry,lasterry,Kpy,Kiy,Kdy)
        pidx = int(pidxx[0]*10000)/10000
        pidy = int(pidyy[0]*10000)/10000
        print("pidy: ",pidy," pidx: ",pidx)
        lastix = pidxx[1]
        lastiy = pidyy[1]
        previoustimex = currtimex
        previoustimey = currtimey
        lasterrx = errx
        lasterry = erry 
        motors.position(
            int(speeder(tspeed + speed1,out_min=min1,out_max=max1) - pidx + pidy),
            int(speeder(tspeed + speed2,out_min=min2,out_max=max2) - pidx - pidy),
            int(speeder(tspeed + speed3,out_min=min3,out_max=max3) + pidx - pidy),
            int(speeder(tspeed + speed4,out_min=min4,out_max=max4) + pidx + pidy),
            t=wait)
        
        
        
        


