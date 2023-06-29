#include <Servo.h>
//---------------------------------------------------------------
#define baudrate 9600
//---------------------------------------------------------------
#define m1 5
#define m2 6
#define m3 10
#define m4 11

int speeed[] = {1000,1000,1000,1000};

Servo ESC1;
Servo ESC2;
Servo ESC3;
Servo ESC4; 
//---------------------------------------------------------------
String data;
//---------------------------------------------------------------
void setup(){
  Serial.begin(baudrate);
  ESC1.attach(m1,1000,2000);
  ESC2.attach(m2,1000,2000);
  ESC3.attach(m3,1000,2000);
  ESC4.attach(m4,1000,2000);
}
//---------------------------------------------------------------
void loop(){
//----------------------------------
  while(Serial.available()){
    delay(2); 
    char datac = Serial.read();
    data += datac;
  }
//----------------------------------
  if(data.length() >0){
    Serial.println(data);
    if(data.length() == 19){
      speeed[0] = data.substring(0,4).toInt();
      speeed[1] = data.substring(5,9).toInt();
      speeed[2] = data.substring(10,14).toInt();
      speeed[3] = data.substring(15,19).toInt();
    }
  }
//----------------------------------
  ESC1.writeMicroseconds(speeed[0]);
  ESC2.writeMicroseconds(speeed[1]);
  ESC3.writeMicroseconds(speeed[2]);
  ESC4.writeMicroseconds(speeed[3]);
//----------------------------------
  data="";
}
