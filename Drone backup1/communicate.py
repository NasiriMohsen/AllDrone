import serial
import serial.tools.list_ports
from time import sleep

ports = list(serial.tools.list_ports.comports())
arduino = serial.Serial(ports[0][0], 9600)


while True:
    data = input("What you say? ")
    for char in data:
        arduino.write(char.encode())