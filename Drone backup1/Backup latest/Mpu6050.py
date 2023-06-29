from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)

while True:
    data = sensor.get_accel_data()
    print(data)
    sleep(0.1)