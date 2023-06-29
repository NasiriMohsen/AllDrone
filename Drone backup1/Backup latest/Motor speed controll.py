from gpiozero import Servo
from time import sleep

mt1 = Servo(26)
mt2 = Servo(16)
mt3 = Servo(20)
mt4 = Servo(21)

mt1.min()
mt2.min()
mt3.min()
mt4.min()
sleep(0.5)
while True:
    for speed in range(-10,11):
        print(speed/10)
        #mt1.value = speed/10
        #mt2.value = speed/10
        #mt3.value = speed/10
        #mt4.value = speed/10
        sleep(1)
        
    
