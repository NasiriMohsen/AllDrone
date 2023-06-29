#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

void MPUInit(){
  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  bool Msgr = false;
  while(status!=0){ 
    if (Msgr == false){
      Serial.println("Disconnected. Going inside a loop! ");
      Msgr = true;
    }
  }
  Serial.println("Connected. ");

  Serial.println(F("Calculating offsets, do not move MPU6050"));
  mpu.calcOffsets(true,true); // gyro and accelero
  Serial.println("Done!\n");
}

void UpdateMPU(){
  mpu.update();
}

int Temperature(){
  return mpu.getTemp();
}

int AccelerationX(){
  return mpu.getAccY();
}

int AccelerationY(){
  return mpu.getAccY();
}

int AccelerationZ(){
  return mpu.getAccZ();
}

int GyroX(){
  return mpu.getGyroX();
}

int GyroY(){
  return mpu.getGyroY();
}

int GyroZ(){
  return mpu.getGyroZ();
}

int AngleX(){
  return mpu.getAngleX();
}

int AngleY(){
  return mpu.getAngleY();
}

int AngleZ(){
  return mpu.getAngleZ();
}

int AccelerationAngleX(){
  return mpu.getAccAngleX();
}

int AccelerationAngleY(){
  return mpu.getAccAngleY();
}





void setup() {
  Serial.begin(115200);
  MPUInit();
}




void loop() {  
  UpdateMPU();
  Serial.println(GyroX());
}
