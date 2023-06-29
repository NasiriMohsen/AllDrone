#define BAUD_RATE 115200  


#define Radio_Channels 9

#define RC_CH1_INPUT  34
#define RC_CH2_INPUT  35
#define RC_CH3_INPUT  32
#define RC_CH4_INPUT  33
#define RC_CH5_INPUT  25
#define RC_CH6_INPUT  26
#define RC_CH7_INPUT  27
#define RC_CH8_INPUT  14
#define RC_CH9_INPUT  12
//#define RC_CH10_INPUT  X
//#define RC_CH11_INPUT  X
//#define RC_CH12_INPUT  X


//---------------------------------------------------
#define RC_CH1  0
#define RC_CH2  1
#define RC_CH3  2
#define RC_CH4  3
#define RC_CH5  4
#define RC_CH6  5
#define RC_CH7  6
#define RC_CH8  7
#define RC_CH9  8
//#define RC_CH10  10
//#define RC_CH11  11
//#define RC_CH12  12

//---------------------------------------------------
uint16_t rc_values[Radio_Channels];
uint32_t rc_start[Radio_Channels];
volatile uint16_t rc_shared[Radio_Channels];

//---------------------------------------------------
void rc_read_values() {
  noInterrupts();
  memcpy(rc_values, (const void *)rc_shared, sizeof(rc_shared));
  interrupts();
}
//------------------------
void calc_input(uint8_t channel, uint8_t input_pin) {
  if (digitalRead(input_pin) == HIGH) {
    rc_start[channel] = micros();
  } else {
    uint16_t rc_compare = (uint16_t)(micros() - rc_start[channel]);
    rc_shared[channel] = rc_compare;
  }
}

//---------------------------------------------------
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
//-----------10-------------
/*
void calc_ch10() { 
  calc_input(RC_CH10, RC_CH10_INPUT); 
}
//-----------11-------------
void calc_ch11() { 
  calc_input(RC_CH11, RC_CH11_INPUT); 
}
//-----------12-------------
void calc_ch12() { 
  calc_input(RC_CH12, RC_CH12_INPUT); 
}
*/
//---------------------------------------------------
void setup() {
  Serial.begin(BAUD_RATE);

  //------------------------------
  pinMode(RC_CH1_INPUT, INPUT);
  pinMode(RC_CH2_INPUT, INPUT);
  pinMode(RC_CH3_INPUT, INPUT);
  pinMode(RC_CH4_INPUT, INPUT);
  pinMode(RC_CH5_INPUT, INPUT);
  pinMode(RC_CH6_INPUT, INPUT);
  pinMode(RC_CH7_INPUT, INPUT);
  pinMode(RC_CH8_INPUT, INPUT);
  pinMode(RC_CH9_INPUT, INPUT);
  //pinMode(RC_CH10_INPUT, INPUT);
  //pinMode(RC_CH11_INPUT, INPUT);
  //pinMode(RC_CH12_INPUT, INPUT);

  //------------------------------
  attachInterrupt(RC_CH1_INPUT, calc_ch1, CHANGE);
  attachInterrupt(RC_CH2_INPUT, calc_ch2, CHANGE);
  attachInterrupt(RC_CH3_INPUT, calc_ch3, CHANGE);
  attachInterrupt(RC_CH4_INPUT, calc_ch4, CHANGE);
  attachInterrupt(RC_CH5_INPUT, calc_ch5, CHANGE);
  attachInterrupt(RC_CH6_INPUT, calc_ch6, CHANGE);
  attachInterrupt(RC_CH7_INPUT, calc_ch7, CHANGE);
  attachInterrupt(RC_CH8_INPUT, calc_ch8, CHANGE);
  attachInterrupt(RC_CH9_INPUT, calc_ch9, CHANGE);
  //attachInterrupt(RC_CH10_INPUT, calc_ch10, CHANGE);
  //attachInterrupt(RC_CH11_INPUT, calc_ch11, CHANGE);
  //attachInterrupt(RC_CH12_INPUT, calc_ch12, CHANGE);
}

//---------------------------------------------------
void loop() {
  rc_read_values();

  //------------------------------
  for (int i = 0; i < Radio_Channels ; i++){
    Serial.print("CH");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(rc_values[i]);
    Serial.print("\t");
  }
  Serial.println("");
  //------------------------------
  delay(8);
}
