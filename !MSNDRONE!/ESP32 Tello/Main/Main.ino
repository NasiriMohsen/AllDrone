//Main Code
//#########################################################################################
#include <Tello.h>
#include "Radio.h"

#define BAUD_RATE 115200
#define BatteryLim 12
#define WifiLim 25

const char * networkName = "Tello38";
const char * networkPswd = "13471347";

boolean connected = false;

Tello tello;

int BlackBox[10];
boolean Takeoff = false,Land = true;
int Speed,RollFlip,PitchFlip,Roll,Pitch,Yaw,Thrust,PreSpeed,PreSwitch_A,PreSwitch_B,PreSwitch_H;
//#########################################################################################
void setup() {
  Serial.begin(BAUD_RATE);
  connectToWiFi(networkName, networkPswd);
  RadioInit();
}
//#########################################################################################
void loop() {  
  if(connected){        
    UpdateRadio();
    Pot_L = CH6();
    Speed = int(map(Pot_L,1000,2000,1,10)*10);
    if(Speed != PreSpeed){
      tello.setSpeed(Speed);
      PreSpeed = Speed;
    }
        
    Switch_A = map(CH7(),1000,2000,0,1);
    if(Switch_A != PreSwitch_A){
      if (Land == false && Takeoff == true){
        tello.land();
        delay(1000);
        Takeoff = false;
        Land = true;
      }
      PreSwitch_A = Switch_A;
    }
    
    Switch_B = map(CH8(),1000,2000,0,1);
    if(Switch_B != PreSwitch_B){
      if (Land == true && Takeoff == false){
        tello.takeoff();
        delay(1000);
        Takeoff = true;
        Land = false;
      }
      PreSwitch_B = Switch_B;
    }
          
    if(Takeoff == true){
      Switch_H = map(CH9(),1000,2000,0,1);
      if(Switch_H == 0){
        R_Roll = CH1();
        Roll = map(R_Roll,1000,2000,-100,100);
        Serial.print("Roll");Serial.println(Roll);
        R_Pitch = CH2();
        Pitch = map(R_Pitch,1000,2000,100,-100);
        Serial.print("Pitch");Serial.println(Pitch);
        R_Thrust = CH3();
        Thrust = map(R_Thrust,1000,2000,100,-100);
        Serial.print("Thrust");Serial.println(Thrust);
        R_Yaw = CH4();
        Yaw = map(R_Yaw,1000,2000,-100,100);
        Serial.print("Yaw");Serial.println(Yaw);
        tello.sendRCcontrol(Roll,Pitch,Thrust,Yaw);  
      }else{
        R_Roll   = CH1();
        RollFlip = map(R_Roll,1000,2000,-1,1);
        Serial.print("RollFlip");Serial.println(RollFlip);
        R_Pitch  = CH2();
        PitchFlip = map(R_Pitch,1000,2000,1,-1);   
        Serial.print("PitchFlip");Serial.println(PitchFlip);
        delay(1000);
        if(PitchFlip == 1 && RollFlip == 0){
          tello.flip_right();  
        }else if(PitchFlip == -1 && RollFlip == 0){
          tello.flip_left();  
        }else if(PitchFlip == 0 && RollFlip == 1){
          tello.flip_front();  
        }else if(PitchFlip == 0 && RollFlip == -1){
          tello.flip_back();  
        } 
      }
    }   
  }
}















void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));
  WiFi.disconnect(true);
  WiFi.onEvent(WiFiEvent);
  WiFi.begin(ssid, pwd);
  Serial.println("Waiting for WIFI connection...");
}

void WiFiEvent(WiFiEvent_t event){
  switch(event){
    case SYSTEM_EVENT_STA_GOT_IP:
      Serial.print("WiFi connected! IP address: ");
      Serial.println(WiFi.localIP());
      tello.init();
      connected = true;
      break;
      
    case SYSTEM_EVENT_STA_DISCONNECTED:
      Serial.println("WiFi lost connection");
      connected = false;
      break;
  }
}
