from time import sleep
from threading import Thread
import keyboard

def func():
    while True:
        if keyboard.is_pressed("1"):
            print("Pressed")

t1 = Thread(target=func())
t1.start()
a = 0
while True:
    a = a + 1
    sleep(1)
    print(" " + str(a) + "")