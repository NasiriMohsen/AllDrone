//Main Code

    
// Error = Input and Sensor = OUTPUT for PID
// Desired = Setpoint 


/*Motor Orientation
      4      1
       \    /
       /    \
      3      2
*/
//#########################################################################################
#include "IMU.H"
#include "Motors.H"
#include "Radio.h"

#define BAUD_RATE 115200  
#define PID_Limit 300


#define Ki 0.01
#define KiY 0




float Kp,Kd;
float PreError_Yaw,PreError_Pitch,PreError_Roll;
float Roll_I,Pitch_I,Yaw_I; 
float PID_Output_Pitch,PID_Output_Roll,PID_Output_Yaw;

int KillSwitch = 0;
int SpeedSwitch = 1;
//#########################################################################################
float Calc_PD(int Error,int PreError){
    float P,D;
    P = Kp * Error;
    D = Kd * (Error - PreError);
    return P+D;
}

float PID_Limiter(float PID){
  if (PID >= PID_Limit){
    return PID_Limit;
  }
  else if (PID <= -PID_Limit){
    return -PID_Limit;
  }
  else{
    return PID;
  }
}
//#########################################################################################
void setup() {
  Serial.begin(BAUD_RATE);

  RadioInit();
  MPUInit();
  MotorsInit();
  
  Thrust = 0;
}
//#########################################################################################
void loop() {
  UpdateRadio();
  UpdateMPU();

  R_Roll   = CH1();
  R_Pitch  = CH2();
  R_Thrust = CH3();
  R_Yaw    = CH4();
  Switch_C = CH5();
  Pot_L    = CH6();
  Pot_B    = CH7();
  Pot_R    = CH8();
  Switch_B = CH9();

  KillSwitch = map(Switch_B,1000,2000,0,1);
  SpeedSwitch = map(Switch_C,2000,1000,1,3);

  Kp = map(Pot_L,1000,2000,0,1000)/100;
  //Ki = map(Pot_B,2000,1000,0,1000)/100;
  Kd = map(Pot_R,1000,2000,0,1000)/100;


  if(SpeedSwitch == 3){
    Roll_Angle = 15;
    Pitch_Angle = 15;
    Yaw_Angle = 5;
  }
  else if(SpeedSwitch == 2){
    Roll_Angle = 13;
    Pitch_Angle = 13;
    Yaw_Angle = 3;
  }
  else{
    Roll_Angle = 10;
    Pitch_Angle = 10;
    Yaw_Angle = 1; 
  }

  Desired_Pitch = map(R_Pitch,Pitch_Min,Pitch_Max,-Pitch_Angle,Pitch_Angle);
  Desired_Roll = map(R_Roll,Roll_Min,Roll_Max,-Roll_Angle,Roll_Angle); 
  Desired_Yaw += map(R_Yaw,Yaw_Min,Yaw_Max,-Yaw_Angle,Yaw_Angle);
  Thrust = map(R_Thrust,Thrust_Min,Thrust_Max,Thrust_Min_Speed,Thrust_Max_Speed);


  Pitch = KalmanAngleX();
  Roll = KalmanAngleY();
  Yaw = KalmanAngleZ();

  Pitch_error = Pitch - Desired_Pitch;
  Roll_error = Roll - Desired_Roll;
  Yaw_error = Yaw - Desired_Yaw;

  
  Yaw_I = (KiY * Yaw_error) + Yaw_I;
  Pitch_I = (Ki * Pitch_error) + Pitch_I;
  Roll_I = (Ki * Roll_error) + Roll_I;

  PID_Output_Pitch = PID_Limiter(Calc_PD(Pitch_error,PreError_Pitch) + Pitch_I);
  PID_Output_Roll = PID_Limiter(Calc_PD(Roll_error,PreError_Roll) + Roll_I);
  PID_Output_Yaw = PID_Limiter(Calc_PD(Yaw_error,PreError_Yaw) + Yaw_I);

  
  
  PreError_Pitch = Pitch_error;
  PreError_Roll = Roll_error;
  PreError_Yaw = Yaw_error;


  M1_Speed = Thrust - PID_Output_Pitch + PID_Output_Roll - PID_Output_Yaw; //front right
  M2_Speed = Thrust + PID_Output_Pitch + PID_Output_Roll + PID_Output_Yaw; //bottom right
  M3_Speed = Thrust + PID_Output_Pitch - PID_Output_Roll - PID_Output_Yaw; //bottom left
  M4_Speed = Thrust - PID_Output_Pitch - PID_Output_Roll + PID_Output_Yaw; //front left

  M1_Speed = SpeedChecker(M1_Speed);
  M2_Speed = SpeedChecker(M2_Speed);
  M3_Speed = SpeedChecker(M3_Speed);
  M4_Speed = SpeedChecker(M4_Speed);

  Serial.print(" Pitch: ");
  Serial.print(PID_Output_Pitch);
  Serial.print(" Roll: ");
  Serial.print(PID_Output_Roll);
  Serial.print(" Yaw: ");
  Serial.print(PID_Output_Yaw);
  
  Serial.print(" M1: ");
  Serial.print(M1_Speed);
  Serial.print(" M2: ");
  Serial.print(M2_Speed);
  Serial.print(" M3: ");
  Serial.print(M3_Speed);
  Serial.print(" M4: ");
  Serial.println(M4_Speed);



  if (KillSwitch == 0 && Thrust > minMotorspeed){
    M1_M2_M3_M4(M1_Speed,M2_Speed,M3_Speed,M4_Speed);
  }
  else{
    M1_M2_M3_M4(0,0,0,0);
  }

  
  delay(8);
}
