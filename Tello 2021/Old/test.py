import keyboard
import time
from threading import Thread

def func():
    print("pressed1")

def func2():
    print("pressed2")
    

keyboard.add_hotkey("1",func)
keyboard.add_hotkey("2",func2)

def t():
    while True:
        if keyboard.is_pressed("3"):
            print("pressed3")

t1 = Thread(target=t)
t1.start()

while True:
    print(0)
    time.sleep(0.1)