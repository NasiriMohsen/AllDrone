#include <Wire.h>
#include <Servo.h>
//############################################################
#define baudrate 9600

#define m1 5
#define m2 6
#define m3 10
#define m4 11

const int MPU = 0x68;

float AcX,AcY,AcZ,AX,AY,AXE,AYE,GyX,GyY,GyZ,GX,GY,GZ,GXE,GYE,GZE,Temp;
float et,pt,ct;
float rad_to_deg = 180/3.141592654;

float danglex = 0,dangley = 0;
float errorx,errory,perrx,perry,pidx,opx,oix,odx,pidy,opy,oiy,ody;

float P = 10,I = 0,D = 0;

int speeed[] = {1000,1000,1000,1000};
int Thrust = 1000;

String data;

Servo ESC1;
Servo ESC2;
Servo ESC3;
Servo ESC4; 
//############################################################
void setup(){
  ESC1.attach(m1,1000,2000);
  ESC2.attach(m2,1000,2000);
  ESC3.attach(m3,1000,2000);
  ESC4.attach(m4,1000,2000);
  
  ct = millis();
  
  Serial.begin(baudrate); 
  
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
  Wire.write(0);    
  Wire.endTransmission(true);
//############################################################
  for(int i=0;i<200;i++){
    Wire.beginTransmission(0x68);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU,6,true); 
    
    AcX = Wire.read()<<8|Wire.read();
    AcY = Wire.read()<<8|Wire.read();
    AcZ = Wire.read()<<8|Wire.read();

    AXE = AXE+((atan((AcY/4096)/sqrt(pow((AcX/4096),2)+pow((AcZ/4096),2)))*rad_to_deg));
    AYE = AYE+((atan(-1*(AcX/4096)/sqrt(pow((AcY/4096),2)+pow((AcZ/4096),2)))*rad_to_deg)); 
  
    if(i==199){
      AXE = AXE/200;
      AYE = AYE/200;
    }
  }
  for(int i=0;i<200;i++){
    Wire.beginTransmission(MPU);             
    Wire.write(0x43);          
    Wire.endTransmission(false);
    Wire.requestFrom(MPU,6,true);
         
    GyX=Wire.read()<<8|Wire.read();     
    GyY=Wire.read()<<8|Wire.read();
    GyZ=Wire.read()<<8|Wire.read();
   
    GXE = GXE+(GyX/32.8); 
    GYE = GYE+(GyY/32.8);
    GZE = GZE+(GyZ/32.8);
    
    if(i==199){ 
      GXE = GXE/200;
      GYE = GYE/200;
      GZE = GZE/200;
    }
  }  
}
//############################################################
void loop(){
  pt = ct;
  ct = millis();                        
  et = (ct-pt)/1000;
//--------------------------------------------  
  while(Serial.available()){
    delay(2); 
    char datac = Serial.read();
    data += datac;
  }
  if(data.length() >0){
    Serial.println(data);
    if(data.length()>0){
      Thrust = data.substring(0,4).toInt();
    }
  }
  data="";
//--------------------------------------------
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,14,true);  
  
  AcX = Wire.read()<<8|Wire.read();    
  AcY = Wire.read()<<8|Wire.read();  
  AcZ = Wire.read()<<8|Wire.read();
  Temp = (Wire.read()<<8|Wire.read())/340.00+36.53;
  GyX = Wire.read()<<8|Wire.read();  
  GyY = Wire.read()<<8|Wire.read();  
  GyZ = Wire.read()<<8|Wire.read(); 
  
  AX = ((atan((AcY/4096)/sqrt(pow((AcX/4096),2)+pow((AcZ/4096),2)))*rad_to_deg))-AXE;
  AY = ((atan(-1*(AcX/4096)/sqrt(pow((AcY/4096),2)+pow((AcZ/4096),2)))*rad_to_deg))-AYE; 

  GX = ((GyX/32.8)-GXE)*et; 
  GY = ((GyY/32.8)-GYE)*et;
  GZ = ((GyZ/32.8)-GZE)*et;
//--------------------------------------------  
  errorx = AX - danglex;
  errory = AY - dangley;
  
  opx = P*errorx;
  oix = oix+(I*errorx);  
  odx = D*((errorx-perrx)/et);
  pidx = opx+oix+odx;
  
  opy = P*errory;
  oiy = oiy+(I*errory);  
  ody = D*((errorx-perry)/et);
  pidy = opy+oiy+ody;

  perrx = errorx;
  perry = errory;
//--------------------------------------------
  if(Thrust <= 1000){
    ESC1.writeMicroseconds(1000);
    ESC2.writeMicroseconds(1000);
    ESC3.writeMicroseconds(1000);
    ESC4.writeMicroseconds(1000);
  }else{
    ESC1.writeMicroseconds(Thrust-pidx+pidy);
    ESC2.writeMicroseconds(Thrust-pidx-pidy);
    ESC3.writeMicroseconds(Thrust+pidx-pidy);
    ESC4.writeMicroseconds(Thrust+pidx+pidy);
  }
//--------------------------------------------
  Serial.print(" "); Serial.print(Thrust);
  Serial.print(" PID: "); Serial.println(pidx); 
}
