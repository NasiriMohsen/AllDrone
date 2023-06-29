#include <Servo.h>

Servo ESC1;
Servo ESC2;
Servo ESC3;
Servo ESC4;    

int potValue;

void setup() {
  Serial.begin(9600);
  ESC1.attach(5,1000,2000);
  ESC2.attach(6,1000,2000);
  ESC3.attach(10,1000,2000);
  ESC4.attach(11,1000,2000);
}

void loop() {
  potValue = analogRead(A0);
  potValue = map(potValue, 0, 900, 1000, 2000);
  Serial.println(potValue);
  ESC1.writeMicroseconds(potValue);
  ESC2.writeMicroseconds(potValue);
  ESC3.writeMicroseconds(potValue);
  ESC4.writeMicroseconds(potValue);
}
