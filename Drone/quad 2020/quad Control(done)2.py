import pygame as pg
import Quadcopter
from time import sleep,time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

quad = Quadcopter.Motors()

def matlib():
    x_len = 100 
    y_range = [-50, 50]  
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = list(range(0, 100))
    ys = [0] * x_len
    ys2 = [0] * x_len
    midline = [0] * x_len    
    ax.set_ylim(y_range)
    line, = ax.plot(xs, ys)
    line2, = ax.plot(xs, ys2)
    line3, = ax.plot(xs, midline)
    plt.ylabel('gyro')

    def animate(i, ys,ys2):
        data = quad.readdata()
        datas = data.split(",")
        #print(data)
        sens = float(datas[0])
        sens2 = float(datas[1])
        ys.append(sens)
        ys = ys[-x_len:]
        ys2.append(sens2)
        ys2 = ys2[-x_len:]
        line.set_ydata(ys)
        line2.set_ydata(ys2)
        return line,line2,
    
    while len(quad.readdata().split(",")) <= 1:
        print(quad.readdata())
    print("Exited")
    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,ys2,),
        interval=1,
        blit=True)
    plt.show()

t = threading.Thread(target=matlib,)
t.start()

pg.init()
window = pg.display.set_mode([20,20])
pg.display.update()

def cleaner(x):
    r = int(x*1000)/1000
    return r
#############################################################################################################      
stime = time()
wait = 0.08

speed1 = 1000
speed2 = 1000
speed3 = 1000
speed4 = 1000
tspeed = 1000
takeoffspeed = 1300
xslope = 0
yslope = 0
yangle = 15
xangle = 15

P = 0 #0.85 , 0.9
I = 0 #0.003 , 0.002
D = 0#0.3 , 0.05

while len(quad.readdata().split(",")) <= 1:
    print("wait")
quad.position(sp1=1000,sp2=1000,sp3=1000,sp4=1000,thrust=1000,ax=0,ay=0,az=0,P=0,I=0,D=0,t=wait)
#############################################################################################################
while True:
#########################################################################
    for event in pg.event.get():
        msg = ""
        if event.type == pg.KEYDOWN:
        #######################################
            if event.key == pg.K_i:
                msg = "Speed-up"
                tspeed = tspeed + 50
                if tspeed >= 2000:
                    tspeed = 2000

            elif event.key == pg.K_k:
                msg = "Speed-down"
                tspeed = tspeed - 50                  
                if tspeed <= 1000:
                    tspeed = 1000

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

            if event.key == pg.K_t:
                msg = "Take off"
                if tspeed == 1000:
                    tspeed = takeoffspeed
                else:
                    tspeed = 1000       
            if event.key == pg.K_l:
                msg = "Shutdown"
                tspeed = 1000


            if event.key == pg.K_y:
                msg = "P increase"
                P = P + 0.1
            elif event.key == pg.K_h:
                msg = "P decrease"
                P = P - 0.1
            
            if event.key == pg.K_u:
                msg = "D increase"
                D = D + 0.01
            elif event.key == pg.K_j:
                msg = "D decrease"
                D = D - 0.01
            if event.key == pg.K_n:
                msg = "I increase"
                I = I + 0.001
            elif event.key == pg.K_m:
                msg = "I decrease"
                I = I - 0.001






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
            if (event.key == pg.K_l):
                turnoff = 0
        print(msg)   
#########################################################################
        quad.position(
                    sp1=cleaner(speed1),
                    sp2=cleaner(speed2),
                    sp3=cleaner(speed3),
                    sp4=cleaner(speed4),
                    thrust=cleaner(tspeed),
                    ax=cleaner(xslope),
                    ay=cleaner(yslope),
                    az=0,
                    P=cleaner(P),
                    I=cleaner(I),
                    D=cleaner(D),
                    t=wait)
    print(  
        #speed1,
        #speed2,
        #speed3,
        #speed4,
        tspeed,
        xslope,
        yslope,
        #0,
        cleaner(P),
        cleaner(I),
        cleaner(D)
        )

    
#plt.show()

#1000,1000,1000,1000,1050,0,0,0,2,0,1