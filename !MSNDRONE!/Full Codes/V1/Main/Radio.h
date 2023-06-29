//Radio Reciver Code
//#####################################Radio###############################################
#define Roll_Min 1002
#define Roll_Max 2002
#define Pitch_Min 1002
#define Pitch_Max 2002
#define Yaw_Min 2000
#define Yaw_Max 1000
#define Thrust_Min 2002
#define Thrust_Max 1002

int R_Thrust,R_Pitch,R_Roll,R_Yaw,Switch_B,Switch_C,Pot_B,Pot_R,Pot_L;
//#########################################################################################
#define Radio_Channels 9

#define RC_CH1_INPUT  34 //Pot (Back)
#define RC_CH2_INPUT  35 //Top pot (LEFT)
#define RC_CH3_INPUT  32 //Switch (C)
#define RC_CH4_INPUT  33 //Roll
#define RC_CH5_INPUT  25 //Pitch
#define RC_CH6_INPUT  26 //Thrust
#define RC_CH7_INPUT  27 //Yaw
#define RC_CH8_INPUT  14 //Switch (B)s
#define RC_CH9_INPUT  12 //Top pot (RIGHT)

#define RC_CH1  0
#define RC_CH2  1
#define RC_CH3  2
#define RC_CH4  3 
#define RC_CH5  4 
#define RC_CH6  5 
#define RC_CH7  6 
#define RC_CH8  7 
#define RC_CH9  8

uint16_t rc_values[Radio_Channels];
uint32_t rc_start[Radio_Channels];
volatile uint16_t rc_shared[Radio_Channels];
//#########################################################################################
void rc_read_values() {
  noInterrupts();
  memcpy(rc_values, (const void *)rc_shared, sizeof(rc_shared));
  interrupts();
}

void calc_input(uint8_t channel, uint8_t input_pin) {
  if (digitalRead(input_pin) == HIGH) {
    rc_start[channel] = micros();
  } else {
    uint16_t rc_compare = (uint16_t)(micros() - rc_start[channel]);
    rc_shared[channel] = rc_compare;
  }
}
//#########################################################################################
void calc_ch1() { 
  calc_input(RC_CH1, RC_CH1_INPUT); 
}
//-----------2--------------
void calc_ch2() { 
  calc_input(RC_CH2, RC_CH2_INPUT); 
}
//-----------3--------------
void calc_ch3() { 
  calc_input(RC_CH3, RC_CH3_INPUT); 
}
//-----------4--------------
void calc_ch4() { 
  calc_input(RC_CH4, RC_CH4_INPUT); 
}
//-----------5--------------
void calc_ch5() { 
  calc_input(RC_CH5, RC_CH5_INPUT); 
}
//-----------6--------------
void calc_ch6() { 
  calc_input(RC_CH6, RC_CH6_INPUT); 
}
//-----------7--------------
void calc_ch7() { 
  calc_input(RC_CH7, RC_CH7_INPUT); 
}
//-----------8--------------
void calc_ch8() { 
  calc_input(RC_CH8, RC_CH8_INPUT); 
}
//-----------9--------------
void calc_ch9() { 
  calc_input(RC_CH9, RC_CH9_INPUT); 
}

void RadioInit() {
  pinMode(RC_CH1_INPUT, INPUT);
  pinMode(RC_CH2_INPUT, INPUT);
  pinMode(RC_CH3_INPUT, INPUT);
  pinMode(RC_CH4_INPUT, INPUT);
  pinMode(RC_CH5_INPUT, INPUT);
  pinMode(RC_CH6_INPUT, INPUT);
  pinMode(RC_CH7_INPUT, INPUT);
  pinMode(RC_CH8_INPUT, INPUT);
  pinMode(RC_CH9_INPUT, INPUT);

  attachInterrupt(RC_CH1_INPUT, calc_ch1, CHANGE);
  attachInterrupt(RC_CH2_INPUT, calc_ch2, CHANGE);
  attachInterrupt(RC_CH3_INPUT, calc_ch3, CHANGE);
  attachInterrupt(RC_CH4_INPUT, calc_ch4, CHANGE);
  attachInterrupt(RC_CH5_INPUT, calc_ch5, CHANGE);
  attachInterrupt(RC_CH6_INPUT, calc_ch6, CHANGE);
  attachInterrupt(RC_CH7_INPUT, calc_ch7, CHANGE);
  attachInterrupt(RC_CH8_INPUT, calc_ch8, CHANGE);
  attachInterrupt(RC_CH9_INPUT, calc_ch9, CHANGE);
}

void UpdateRadio() {
  rc_read_values();
}

int CH1() {
  //Roll
  return rc_values[3];
}
int CH2() {
  //Pitch
  return rc_values[4];
}
int CH3() {
  //Thrust
  return rc_values[5];
}
int CH4() {
  //Yaw
  return rc_values[6];
}
int CH5() {
  //Switch C
  return rc_values[2];
}
int CH6() {
  //Potantiometer Front Left
  return rc_values[1];
}
int CH7() {
  //Potantiometer Back Left
  return rc_values[0];
}
int CH8() {
  //Potantiometer Front Right
  return rc_values[8];
}
int CH9() {
  //Switch B
  return rc_values[7];
}

/*
void setup(){
  RadioInit();
}



  Serial.print(rc_values[0]);
  Serial.print(" - ");
  Serial.print(rc_values[1]);
  Serial.print(" - ");
  Serial.print(rc_values[2]);
  Serial.print(" - ");
  Serial.print(rc_values[3]);
  Serial.print(" - ");
  Serial.print(rc_values[4]);
  Serial.print(" - ");
  Serial.print(rc_values[5]);
  Serial.print(" - ");
  Serial.print(rc_values[6]);
  Serial.print(" - ");
  Serial.print(rc_values[7]);
  Serial.print(" - ");
  Serial.println(rc_values[8]);



void loop(){
  UpdateRadio();
}
*/
