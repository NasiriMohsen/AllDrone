#define baudrate 9600
#define ledPin 13
String data;

void setup(){
  pinMode(ledPin,OUTPUT);
  Serial.begin(baudrate);
}

void loop(){
  while(Serial.available()){
    delay(2); 
    char datac = Serial.read();
    data += datac;
  }

  if(data.length() >0){
    Serial.println(data);
    if(data == "on"){
      digitalWrite(ledPin, HIGH);
      Serial.println("LED ON");
    }
    if(data == "off"){
      digitalWrite(ledPin, LOW);
      Serial.println("LED OFF");
    }
    
  }
  data="";
}
