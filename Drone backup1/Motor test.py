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
    mt4.min()
    mt3.min()
    mt2.min()
    mt1.min()
    print("min")
    sleep(2)
    mt4.mid()
    mt3.mid()
    mt2.mid()
    mt1.mid()
    print("mid")
    sleep(2)
    mt4.max()
    mt3.max()
    mt2.max()
    mt1.max()
    print("max")
    sleep(2)
    
