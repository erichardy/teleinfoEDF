
// ESP32 API references : https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/index.html
//
// https://arduinojson.org/

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

/*
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
This version suffer of memory management.
An other version should be developped !!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
We will use static variables/arrays/...to store data
*/

#include <cstring>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstring>
#include <string>
#include <stdio.h>
#include <stdlib.h>

// https://github.com/plerup/espsoftwareserial/
#include <SoftwareSerial.h>
#include <WiFi.h>
#include "ESPNowW.h"

using namespace std;

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
#define LINE_MAX 150
#define VALUES_MAX 55  // max number of fields

// #include "LibTeleinfo.h" 

uint8_t receiver_mac[] = {0x36, 0x33, 0x33, 0x33, 0x33, 0x33};
char c;
uint32_t i = 0;
uint32_t n = 0;

char buff[3000];
uint32_t buff_idx = 0;
bool buff_started = false;
uint32_t nb_frames = 0;
uint8_t nb_fields = 0;

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
  char  line[LINE_MAX];    // The full raw line containing label [+ horo] + value + checksum
};

Value values[55];

void clearValues() {
  uint8_t i = 0;
  for (i = 0; i < VALUES_MAX; i++) {
    values[i].checksum = 0;
    memset(values[i].label, 0, LABEL_MAX);
    memset(values[i].value, 0, VALUE_MAX);
    memset(values[i].horo, 0, HORO_MAX);
    memset(values[i].line, 0, LINE_MAX);
  }
}
/*
   displayValue : should replace cout with Serial.print
*/
void displayValue(Value * val) {
    cout << "Label :" << val->label << endl;
    cout << "Value :" << val->value << endl;
    if (val->horo) {
        cout << "Horo :" << val->horo << endl;
    } else {
        cout << "Horo : NONE" << endl;
    }
    cout << "Checksum :" << val->checksum << endl;
}

void displayValue2(Value * val) {
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
}


void clearBuffer() {
  memset(buff, 0, BUFF_SIZE);
  buff_idx = 0;
  buff_started = false;
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
void setValueFields(Value val) {
    char * line;
    char * field;
    uint8_t i = 0;
    // first read of the line to count the fields
    // maybe more efficient with strpbrk
    // see https://cplusplus.com/reference/cstring/strpbrk/
    field = strtok(line, "\t");
    while (field != NULL) {
        nb_fields++;
        field = strtok(NULL, "\t");
    }
    i = 0;
    free(line);
    // strcpy(line, value->line);
    field = strtok(line, "\t");
    while (field != NULL) {
        // cout << field;
        if (i == 0) {
        }
        if (nb_fields == 3) {
        }
        if (nb_fields == 4) {
        }
        field = strtok(NULL, "\t");
        i++;
    }
    return;
}

/*
return _nb_fields
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

Value * getValueFor(char * label)   {
    Value *val; // pointer returned
    /* val = values.first;
    while (val) {
        if (!strcmp(val->label, label)) {
            break;
        }
        val = val->next;
    }
    */
    return val;
}

/*
buffer == frame
*/
void manageFrame() {
  char * F_line;
  uint8_t nb_lines;
  uint8_t i = 0;

  // Serial.println(ESP.getFreeHeap());
  nb_lines = getLinesFromFrame();
  Serial.print("nb lines :");
  Serial.println(nb_lines);
  if (nb_lines > 0) {
    for (i = 0; i < nb_lines; i++) {
      Serial.print(values->line);
      // setValueFields(values[i]);
      // displayValue2(val);
    }
    // Serial.println("================");
    /*
    char x_label[] = "SINSTS1";
    Value * x_val;
    x_val = getValueFor(x_label);
    displayValue2(x_val);
    */
  }
  // Serial.println(ESP.getFreeHeap());
  clearBuffer();
}

// raw data acquired form Serial
// buff is a global variable.
void fillBuffer(char c) {
  switch (c)  {
    case STX:
      // Serial.println("Start") ;
      // clearBuffer();
      buff_started = true;
      break;
    case ETX:
      // we convert buffer to frame, then later used data
      // Serial.println("End") ;
      buff_started = false;
      buff[buff_idx] = 0;
      manageFrame();
      // Serial.println(nb_frames++);
      break;
    default:
      // Serial.print(c);
      if (buff_started) {
        buff[buff_idx++] = c;
      }
  }
}


void setup() {
  Serial.begin(115200);
  Serial.println("ESPNow..");
  Serial.print("MAC Address : ");
  Serial.println(WiFi.macAddress());
  // pinMode(ONBOARD_LED, OUTPUT);
  Linky.begin(9600, SWSERIAL_7E1, 16, 4);
  // Linky.begin(16, 4);
  /*
  WiFi.mode(WIFI_MODE_STA);
  WiFi.disconnect();
  ESPNow.init();
  ESPNow.add_peer(receiver_mac);
  */
 clearValues();
}

void loop() {
  static uint32_t i = 0;
  /* static uint8_t a = 0;
  delay(100);
  ESPNow.send_message(receiver_mac, &a, 1);
  Serial.println(a++); */
  if (Linky.available()){
    c = Linky.read();
    // we should gnore \r (== cr == 13)
    if (c != 13) {
      fillBuffer(c);
      i++;
    }
  }
  
  if (i > 5000){
    // Serial.println(F("XXXX"));
    delay(5000);
    i = 0;
  }
}