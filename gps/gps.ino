#include <SoftwareSerial.h>
#include <TinyGPS.h> 

SoftwareSerial GPS(8,7);
TinyGPS gps;

void setup(){
  Serial.begin(9600);
  GPS.begin(9600);
}
void loop(){
  while(GPS.available()){
    Serial.write(gps.encode(GPS.read()));
    Serial.println(gps.encode(GPS.read()));
  }

  if(Serial.available()){
    GPS.write(Serial.read());
  }
}
