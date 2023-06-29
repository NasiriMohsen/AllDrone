from mpu6050 import mpu6050
import time

class gyro:

    def __init__(self):
        sensor = mpu6050(0x68)

        ncalibration = 500
        self.xgyroavg = 0
        self.ygyroavg = 0
        self.zgyroavg = 0

        for i in range(0,ncalibration):
            gyro = sensor.get_gyro_data()
            self.xgyroavg = self.xgyroavg + gyro['x']
            self.ygyroavg = self.ygyroavg + gyro['y']
            self.zgyroavg = self.zgyroavg + gyro['z']

        self.xgyroavg = self.xgyroavg/ncalibration
        self.ygyroavg = self.ygyroavg/ncalibration
        self.zgyroavg = self.zgyroavg/ncalibration

    def gyrodata(self):
        #acceldata = sensor.get_accel_data()
        gyrodata = sensor.get_gyro_data()

        xgyro = int(((gyrodata['x'] - self.xgyroavg)/57.14286)*100)/100
        ygyro = int(((gyrodata['y'] - self.ygyroavg)/57.14286)*100)/100
        zgyro = int(((gyrodata['z'] - self.zgyroavg)/57.14286)*100)/100

        Gyrodata = {'x':xgyro , 'y':ygyro ,'z':zgyro}
        return Gyrodata