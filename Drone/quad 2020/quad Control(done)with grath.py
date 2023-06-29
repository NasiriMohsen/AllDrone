import pygame as pg
import Quadcopter
from time import sleep,time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


x_len = 200 
y_range = [-90, 90]  
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)
line, = ax.plot(xs, ys)
plt.xlabel('Samples')
plt.ylabel('Temperature (deg C)')

def animate(i, ys):
    print(quad.readdata())
    sens = float(quad.readdata().split(",")[1])
    ys.append(sens)
    ys = ys[-x_len:]
    line.set_ydata(ys)
    return line,
    

def cleaner(x):
    r = int(x*100)/100
    return r
#############################################################################################################      
pg.init()
window = pg.display.set_mode([20,20])
pg.display.update()
quad = Quadcopter.Motors()

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

P = 0.8#2.02
I = 0
D = 0#0.58

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
                D = D + 0.1
            elif event.key == pg.K_j:
                msg = "D decrease"
                D = D - 0.1






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

        #print(  
        #        speed1,
        #        speed2,
        #        speed3,
        #        speed4,
        #        tspeed,
        #        xslope,
        #        yslope,
        #        0,
        #        cleaner(P),
        #        cleaner(I),
        #        cleaner(D)
        #    )
    
    
    while len(quad.readdata().split(",")) <= 1:
        print(quad.readdata())

    print("Exited")


    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=1,
        blit=True)
    plt.show()


#plt.show()

#1000,1000,1000,1000,1050,0,0,0,2,0,1