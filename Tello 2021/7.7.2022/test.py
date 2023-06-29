import keyboard
import time
from threading import Thread

def func(x):
    print("pressed")
    time.sleep(2)

def func2(x):
    print("released")
    time.sleep(2)
def t():
    keyboard.on_press_key("1",func)
    keyboard.on_release_key("1",func2)

t1 = Thread(target=t)
t1.start()

while True:
    print(0)
    time.sleep(0.1)