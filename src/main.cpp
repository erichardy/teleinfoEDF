
// ESP32 API references : https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/index.html
//
// https://arduinojson.org/
//
// Fatal errors :
// https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/fatal-errors.html

#include <Arduino.h>
/*
E01	24:0A:C4:5F:82:A8
// E02	24:62:AB:F3:30:BC
E03	24:0A:C4:5F:77:B0
*/
/*
cf strtok fonction: https://en.cppreference.com/w/cpp/string/byte/strtok
could be very usefull here !!!
https://www.javatpoint.com/how-to-split-strings-in-cpp
*/

#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstring>
#include <string>
#include <stdio.h>
#include <stdlib.h>
using namespace std;

// https://github.com/plerup/espsoftwareserial/
#include <SoftwareSerial.h>
#include <WiFi.h>
#include <esp_now.h>

// #include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define WIRE Wire
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &WIRE);

// #include <ArduinoJson.h>
// const int capacity = JSON_OBJECT_SIZE(3) + 2 * JSON_OBJECT_SIZE(1);
// StaticJsonDocument<capacity> doc;

/*
DATE    E220909150127
SINSTS1 00243
SINSTS2 00040
SINSTS3 00019
SMAXSN1 E220909121952   00321
SMAXSN2 E220909125609   01682
SMAXSN3 E220909045921   00018
SMAXSN1-1   E220908223959   01305
SMAXSN2-1   E220908001241   01347
SMAXSN3-1   E220908020951   00019
*/
typedef struct teleinfoData {
  char date[14];
  char sinsts1[6];
  char sinsts2[6];
  char sinsts3[6];
} teleinfoData;
teleinfoData tData;

// E03	24:0A:C4:5F:77:B0
uint8_t receiver_mac[] = {0x24, 0x0A, 0xC4, 0x5F, 0x77, 0xB0};
esp_now_peer_info_t peerInfo;


#define STX 0x02
#define ETX 0x03
#define HT  0x09
#define SGR '\n' // start of data
#define EGR '\r' // End of data

#define BUFF_SIZE 3000
#define BLOCKSIZE 50

// max sizes of null terminated strings
#define LABEL_MAX 10
#define VALUE_MAX 110
#define HORO_MAX 15
#define DATA_LINE_MAX 150
#define VALUES_MAX 55  // max number of fields

char c;
uint32_t i = 0;
uint32_t n = 0;

char buff[3000];
uint32_t buff_idx = 0;
bool buff_started = false;
uint32_t nb_frames = 0;
uint8_t nb_fields = 0;
bool frame_corrupted = false;

SoftwareSerial Linky;

/* struct partialy from LibTeleinfo created by C. Hallard
   thanks to C. Hallard http://hallard.me/category/tinfo */
typedef struct _Value Value;
struct _Value
{
  char checksum;// checksum
  char  label[LABEL_MAX];    // LABEL of value name
  char  value[VALUE_MAX];   // value
  char  horo[HORO_MAX];    // date if any
  char  line[DATA_LINE_MAX];    // The full raw line containing label [+ horo] + value + checksum
};

Value values[55];

void clearValues() {
  uint8_t i = 0;
  for (i = 0; i < VALUES_MAX; i++) {
    values[i].checksum = 0;
    memset(values[i].label, 0, LABEL_MAX);
    memset(values[i].value, 0, VALUE_MAX);
    memset(values[i].horo, 0, HORO_MAX);
    memset(values[i].line, 0, DATA_LINE_MAX);
  }
}

void clearBuffer() {
  memset(buff, 0, BUFF_SIZE);
  buff_idx = 0;
  buff_started = false;
}

void displayValue(Value * val) {
    Serial.print("Label :");
    Serial.println(val->label);
    Serial.print("Value :");
    Serial.println(val->value);

    if (val->horo) {
        Serial.print("Horo :");
        Serial.println(val->horo);
    } else {
        Serial.print("Horo :");
        Serial.println("NONE");
    }
    Serial.print("Checksum :");
    Serial.println(val->checksum);
    Serial.println(val->line);
}


/* set the fields from each line which contains
   label\tvalue\tchecksum\0
   or
   label\thoro\tvalue\tchecksum\0
   \t = ht = 9
   everything is in struct Value

   From datasheet : Enedis-NOI-CPT_54E.pdf
   Le format utilisé pour les horodates est SAAMMJJhhmmss,
   c'est-à-dire Saison, Année, Mois, Jour, heure, minute, seconde.
*/
bool setValueFields(Value *val) {
  char line[DATA_LINE_MAX];
  char * field;
  char _c;
  uint8_t i = 0;
  uint8_t nb_fields = 0;
  strcpy(line, val->line) ;
  i = 0;
  _c = line[i];
  while (_c) {
    if (_c == HT) {
      nb_fields++;
    }
    _c = line[++i];
  }
  i = 0;
  field = strtok(line, "\t");
  strcpy(val->label, field);
  //
  field = strtok(NULL, "\t");
  if (nb_fields == 2) {
    strcpy(val->value, field);
  } else {
    strcpy(val->horo, field);
  }
  //
  field = strtok(NULL, "\t");
  if (field != NULL) {
    if (nb_fields == 2) {
      val->checksum = field[0];
    } else {
      strcpy(val->value, field);
    }
  } else {
    frame_corrupted = true;
    return(false);
  }
  //
  field = strtok(NULL, "\t");
  if (field != NULL) {
    val->checksum = field[0];
  }
  if (!strcmp(val->label, "DATE")) {
    uint8_t idate = 0;
    uint8_t ihoro = 0;
    for (idate = 5; idate < 18; idate++) {
      val->value[ihoro] = line[idate];
      val->horo[ihoro++] = line[idate];
    }
    val->horo[ihoro] = 0;
    val->checksum = line[20];
  }
  return(true);
}

/*
return nb_fields
*/
uint8_t getLinesFromFrame() {
  char * F_line;
  uint8_t _nb_lines = 0;
  F_line = strtok(buff, "\n");
  while (F_line != NULL) {
    strcpy(values[_nb_lines].line, F_line);
    F_line = strtok(NULL, "\n");
    _nb_lines++;
  }
  return(_nb_lines);
}

char * getValueFor(char * label)   {
  uint8_t i;
  for (i = 0; i < nb_fields; i++) {
    if (! strcmp(values[i].label, label)) {
      break;
    }
  }
  return(values[i].value);
}

/*
buffer == frame
*/
void manageFrame() {
  uint8_t i = 0;
  bool frame_ok;

  // Serial.println(ESP.getFreeHeap());
  nb_fields = getLinesFromFrame();
  if (nb_fields == 53) {
    /* */
    for (i = 0; i < nb_fields; i++) {
      frame_ok = setValueFields(&values[i]);
      // displayValue(&values[i]);
    }
    if (!frame_ok) {
      Serial.println("Frame Corrupted");
      return;
    }
    uint16_t i_SINSTS;
    uint16_t i_SINSTS1;
    uint16_t i_SINSTS2;
    uint16_t i_SINSTS3;
    char x_label[20];
    
    char * x_val;
    strcpy(x_label,"SINSTS");
    x_val = getValueFor(x_label);
    i_SINSTS = atoi(x_val);

    strcpy(x_label,"SINSTS1");
    x_val = getValueFor(x_label);
    i_SINSTS1 = atoi(x_val);

    strcpy(x_label,"SINSTS2");
    x_val = getValueFor(x_label);
    i_SINSTS2 = atoi(x_val);

    strcpy(x_label,"SINSTS3");
    x_val = getValueFor(x_label);
    i_SINSTS3 = atoi(x_val);
    memset(x_val, 0, 20);
    sprintf(x_val, "%i %i %i", i_SINSTS1, i_SINSTS2, i_SINSTS3);
    
    display.clearDisplay();
    display.setCursor(0,0);
    display.println(x_val);
    sprintf(x_val,"%i", nb_frames);
    display.print(x_val);
    display.display();
    // Serial.print(" ");
    // Serial.print(nb_frames);
    nb_frames++;
    // delay(1000);
  }
  clearValues();
  clearBuffer();
  // Serial.println(ESP.getFreeHeap());
  
}

// raw data acquired form Serial
// buff is a global variable.
void fillBuffer(char c) {    
  switch (c)  {
    case EGR:
      break;
    case STX:
      buff_started = true;
      break;
    case ETX:
      buff_started = false;
      buff[buff_idx] = 0;
      manageFrame();
      break;
    default:
      if (buff_started) {
        buff[buff_idx++] = c;
      }
    }
}

void getData() {
  while (1) {
    if (Linky.available()){
      c = Linky.read();
      fillBuffer(c);
    }
  }
}

// Callback function called when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void setup() {
  Serial.begin(115200);
  // display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  display.display();
  delay(1000);
  display.setRotation(2); // vertical flip
  display.setTextSize(1.5);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.display();
  display.clearDisplay();
  delay(2000);

  // END display
  Serial.println("ESPNow..");
  Serial.print("MAC Address : ");
  Serial.println(WiFi.macAddress());
  // pinMode(ONBOARD_LED, OUTPUT);
  Linky.begin(9600, SWSERIAL_7E1, 16, 4);
  /* */
  WiFi.disconnect(true, true);
  WiFi.mode(WIFI_STA);
  /* */
  // Initilize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  } else {
    Serial.println("Initializing ESP-NOW : OK");
  }
  
  // Register the send callback
  esp_now_register_send_cb(OnDataSent);
  memcpy(peerInfo.peer_addr, receiver_mac, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  } else {
    Serial.println("Add peer : OK");
  }
  const uint16_t dataSent = 125;
  esp_err_t result = esp_now_send(receiver_mac, (uint8_t *) &dataSent, sizeof(dataSent));
  /* */
  /* */
  clearValues();
}

void loop() {
  getData();
}