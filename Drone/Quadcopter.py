import serial
import serial.tools.list_ports
from time import sleep

class Motors:
    def __init__(self):
        ports = list(serial.tools.list_ports.comports())
        self.arduino = serial.Serial(ports[0][0], 9600)
        sleep(2)

    def position(self,sp1=1000,sp2=1000,sp3=1000,sp4=1000,thrust=1000,takeoff=0,turnoff=1,ax=0,ay=0,az=0,t=0.0021):
        data = str(sp1)+','+str(sp2)+','+str(sp3)+','+str(sp4)+','+str(thrust)+','+str(takeoff)+','+str(turnoff)+','+str(az)+','+str(ay)+','+str(az)
        for char in data:
            self.arduino.write(char.encode())
        sleep(t)
        else:
            pass



