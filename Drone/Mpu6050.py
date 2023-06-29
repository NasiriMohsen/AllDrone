from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
#####################################
ncalibration = 500
xgyroavg = 0
ygyroavg = 0
zgyroavg = 0

for i in range(0,ncalibration):
    gyro = sensor.get_gyro_data()
    xgyroavg = xgyroavg + gyro['x']
    ygyroavg = ygyroavg + gyro['y']
    zgyroavg = zgyroavg + gyro['z']

xgyroavg = xgyroavg/ncalibration
ygyroavg = ygyroavg/ncalibration
zgyroavg = zgyroavg/ncalibration
#####################################
while True:
    #data = sensor.get_temp()
    #data = sensor.get_gyro_data()
    #data = sensor.get_all_data()
    #acceldata = sensor.get_accel_data()
    gyrodata = sensor.get_gyro_data()
    
    xgyro = int(((gyrodata['x'] - xgyroavg)/57.14286)*100)/100
    ygyro = int(((gyrodata['y'] - ygyroavg)/57.14286)*100)/100
    zgyro = int(((gyrodata['z'] - zgyroavg)/57.14286)*100)/100
    
    print("xgyro: ", xgyro)
    print("ygyro: ", ygyro)
    print("zgyro: ", zgyro)
    
    time.sleep(0.1)