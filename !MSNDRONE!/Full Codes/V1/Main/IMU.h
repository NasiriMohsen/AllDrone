//IMU Code
//######################################IMU################################################
float Pitch,Roll,Yaw, Desired_Pitch,Desired_Roll,Desired_Yaw, Pitch_error,Roll_error,
Yaw_error;

//#########################################################################################
#include "Wire.h"
#include <MPU6050_light.h>
#include <SimpleKalmanFilter.h>

SimpleKalmanFilter KalmanX(1, 1, 0.05);
SimpleKalmanFilter KalmanY(1, 1, 0.05);
SimpleKalmanFilter KalmanZ(1, 1, 0.05);
SimpleKalmanFilter KalmanAcX(1, 1, 0.05);
SimpleKalmanFilter KalmanAcY(1, 1, 0.05);

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

float Temperature(){
  return mpu.getTemp();
}

float AccelerationX(){
  return mpu.getAccY();
}

float AccelerationY(){
  return mpu.getAccY();
}

float AccelerationZ(){
  return mpu.getAccZ();
}

float GyroX(){
  return mpu.getGyroX();
}

float GyroY(){
  return mpu.getGyroY();
}

float GyroZ(){
  return mpu.getGyroZ();
}

float AngleX(){
  return mpu.getAngleX();
}

float AngleY(){
  return mpu.getAngleY();
}

float AngleZ(){
  return mpu.getAngleZ();
}

float AccelerationAngleX(){
  return mpu.getAccAngleX();
}

float AccelerationAngleY(){
  return mpu.getAccAngleY();
}


float KalmanAngleX(){
  return KalmanX.updateEstimate(mpu.getAngleX());
}

float KalmanAngleY(){
  return KalmanY.updateEstimate(mpu.getAngleY());
}

float KalmanAngleZ(){
  return KalmanZ.updateEstimate(mpu.getAngleZ());
}

float KalmanAccelerationAngleX(){
  return KalmanAcX.updateEstimate(mpu.getAccAngleX());
}

float KalmanAccelerationAngleY(){
  return KalmanAcY.updateEstimate(mpu.getAccAngleY());
}


/*
void setup() {
  Serial.begin(115200);
  MPUInit();
}

void loop() {  
  UpdateMPU();
  Serial.println(GyroX());
}
*/
