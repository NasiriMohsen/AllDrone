#include <MPU6050_tockn.h>
#include <Wire.h>
#include <Servo.h>

#define m1 5
#define m2 6
#define m3 10
#define m4 11

MPU6050 mpu6050(Wire);

float AcX,AcY,AcZ,AX,AY,AXE,AYE,GyX,GyY,GyZ,GX,GY,GZ,GXE,GYE,GZE,Temp;
float et,pt,ct;
float rad_to_deg = 180/3.141592654;

float danglex = 0,dangley = 0,danglez = 0;
float errorx,errory,perrx,perry,pidx,opx,oix,odx,pidy,opy,oiy,ody;
float P,I,D; //0.9 , 0.01 , 0.1


String data;
float vars[] = {1000,1000,1000,1000,1000,0,0,0,0,0,0};

int speeed[] = {vars[0],vars[1],vars[2],vars[3]};
int Thrust = vars[4];

Servo ESC1;
Servo ESC2;
Servo ESC3;
Servo ESC4;

void setup(){
  ESC1.attach(m1,1000,2000);
  ESC2.attach(m2,1000,2000);
  ESC3.attach(m3,1000,2000);
  ESC4.attach(m4,1000,2000);
  ESC1.writeMicroseconds(1000);
  ESC2.writeMicroseconds(1000);
  ESC3.writeMicroseconds(1000);
  ESC4.writeMicroseconds(1000);

  ct = millis();
  
  Serial.begin(9600);  
  
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

void loop(){
  
  while(Serial.available()){
    delay(2); 
    char datac = Serial.read();
    data += datac;
  }
  if(data != ""){
    char* delimeter = ",";
    char* token = strtok(data.c_str(),delimeter);
    int counter = 0;
    while( token != NULL ) {
      //Serial.println(atoi(token));
      vars[counter] = atoi(token);
      token = strtok(NULL,delimeter);
      counter++;
    }}
  data="";

  speeed[0] = vars[0];
  speeed[1] = vars[1];
  speeed[2] = vars[2];
  speeed[3] = vars[3];
  Thrust = vars[4];
  danglex = vars[5];
  dangley = vars[6];
  danglez = vars[7];
  P = vars[8];
  I = vars[9];
  D = vars[10];
  
  mpu6050.update();
  
  pt = ct;
  ct = millis();                        
  et = (ct-pt)/1000;
  
  AX = mpu6050.getAngleY();
  AY = mpu6050.getAngleX();
  AXE = mpu6050.getAccAngleX();
  AYE = mpu6050.getAccAngleY();
  GX = mpu6050.getGyroAngleX();
  GY = mpu6050.getGyroAngleY();
  
  errorx = AX - danglex;
  errory = AY - dangley;
  errorx = errorx;
  errory = errory;
  
  opx = P*errorx;
  oix = oix+(I*errorx);  
  odx = D*((errorx-perrx)/et);
  pidx = opx+oix+odx;
  
  opy = P*errory;
  oiy = oiy+(I*errory);  
  ody = D*((errory-perry)/et);
  pidy = opy+oiy+ody;

  perrx = errorx;
  perry = errory;

  if(Thrust <= 1000){
    ESC1.writeMicroseconds(1000);
    ESC2.writeMicroseconds(1000);
    ESC3.writeMicroseconds(1000);
    ESC4.writeMicroseconds(1000);
  }else{
    ESC1.writeMicroseconds(speeed[0]+Thrust-1000+pidx+pidy);
    ESC2.writeMicroseconds(speeed[1]+Thrust-1000+pidx-pidy);
    ESC3.writeMicroseconds(speeed[2]+Thrust-1000-pidx-pidy);
    ESC4.writeMicroseconds(speeed[3]+Thrust-1000-pidx+pidy);
  }
  for (int i=0;i<=10;i++){
    Serial.print(" "); Serial.print(vars[i]);
  }
  Serial.print(" x= "); Serial.print(AX);
  Serial.print(" Y= "); Serial.println(AY); 
}
