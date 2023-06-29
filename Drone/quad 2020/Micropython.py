import machine   
from time import sleep
pin = machine.Pin(2, machine.Pin.OUT)


class pins:
    def __init__(self):
        print("SimplePins created by: Mohsen Nasiri")

    def pinmode(self,PinNumber,PinMode):
        if PinMode == "OUT":
            pin = machine.Pin(PinNumber, machine.Pin.OUT)
        elif PinMode == "IN":
            pin = machine.Pin(PinNumber, machine.Pin.IN)
        return pin

    def changestate(self,Pin,State):
        if State == "ON":
            Pin.on()
        elif State == "OFF":
            Pin.off()
        elif State == "Toggle":
            Pin.value(not Pin.value())
        elif State == "Flash":
            for i in range(0,10):
                Pin.value(not Pin.value())
                sleep(0.2)  
        elif State == "FastFlash":
            for i in range(0,20):
                Pin.value(not Pin.value())
                sleep(0.1)    

    def state(self,Pin):
        return Pin.value()

        
        