from gpiozero import Servo
from time import sleep
import pygame as pg

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

mt1.value = -1
mt2.value = -1
mt3.value = -1
mt4.value = -1

while True:    
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
    mt1.value = speed1
    mt2.value = speed2
    mt3.value = speed3
    mt4.value = speed4
    print(speed1)
    
