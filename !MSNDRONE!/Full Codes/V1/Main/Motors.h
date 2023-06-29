//Motors Code
//#####################################Motors##############################################
int Roll_Angle = 10;
int Pitch_Angle = 10;
int Yaw_Angle = 1;
#define Thrust_Min_Speed 0
#define Thrust_Max_Speed 1000

int Thrust = 0;
int M1_Speed = 0;
int M2_Speed = 0;
int M3_Speed = 0;
int M4_Speed = 0;
//#########################################################################################
#include <Servo.h>

#define F_R_PIN 19  //Red Front Right Motor
#define F_L_PIN 18 //Red Front Left Motor
#define B_R_PIN 15 //Black Back Right Motor
#define B_L_PIN 5 //Black Back Left Motor

#define minMotorspeed 0
#define maxMotorspeed 1000
#define minPulseWidth 1000
#define maxPulseWidth 2000

Servo F_R;
Servo F_L;
Servo B_R;
Servo B_L;

void MotorsInit(){
    F_R.attach(F_R_PIN,-1,minMotorspeed,maxMotorspeed,minPulseWidth,maxPulseWidth);
    F_L.attach(F_L_PIN,-1,minMotorspeed,maxMotorspeed,minPulseWidth,maxPulseWidth);
    B_R.attach(B_R_PIN,-1,minMotorspeed,maxMotorspeed,minPulseWidth,maxPulseWidth);
    B_L.attach(B_L_PIN,-1,minMotorspeed,maxMotorspeed,minPulseWidth,maxPulseWidth);
    
    delay(1000); //wait for motors to turn on properly 
    F_R.write(0);
    F_L.write(0);
    B_R.write(0);
    B_L.write(0);
    delay(1000);
    F_R.write(5);
    F_L.write(5);
    B_R.write(5);
    B_L.write(5);
    delay(10);
}

void AllMotors(int speed){
    F_R.write(speed);
    F_L.write(speed);
    B_R.write(speed);
    B_L.write(speed);
}

void FR_M(int speed){
    F_R.write(speed);
}

void FL_M(int speed){
    F_L.write(speed);
}

void BR_M(int speed){
    B_R.write(speed);
}

void BL_M(int speed){
    B_L.write(speed);
}

void M1_M2_M3_M4(int speed1,int speed2,int speed3,int speed4){
    F_R.write(speed1);
    B_R.write(speed2);
    B_L.write(speed3);
    F_L.write(speed4);
    
}

int SpeedChecker(int MSpeed){
  if (MSpeed >= maxMotorspeed){
    return maxMotorspeed;
  }
  else if(MSpeed <= minMotorspeed){
    return minMotorspeed;
  }
  else{
    return MSpeed;
  }
}


/*
void setup(){ 
    MotorsInit();

    AllMotors(10);
    delay(1000);
    AllMotors(0);
    delay(2000);
}

void loop(){
    AllMotors(0);
    FR_M(50);
    delay(500);
    AllMotors(0);
    BR_M(50);
    delay(500);
    AllMotors(0);
    BL_M(50);
    delay(500);
    AllMotors(0);
    FL_M(50);
    delay(500);

}
*/
