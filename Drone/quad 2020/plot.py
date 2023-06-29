import threading
import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

quad = Quadcopter.Motors()
plt.style.use('fivethirtyeight')
plt.ion()

global xv
global yv
xv = [0]
yv = [0]

i = 0
ptime = 0


def worker():
    print('gone')
    #plt.show(block=True)
    time.sleep(5)


def my_service(i):
    global xv
    global yv
    #print(xv,yv)
    xv = range(i)
    yv = range(i)
    #print(i)
    ## plt.gca().cla() # optionally clear axes
    plt.plot(xv, yv)
    plt.draw()
    plt.pause(0.001)
    plt.show(block=True)




show = threading.Thread(target=worker)


while True:
    i = i + 1
    time.sleep(0.002)
    t = threading.Thread(target=my_service,args=(i,))
    t.start()




