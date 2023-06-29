#define baudrate 9600

String data;

void setup(){
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
    
    
  }
  data="";
}
