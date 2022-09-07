
// ESP32 API references : https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/index.html

#include <Arduino.h>

/*
cf strtok fonction: https://en.cppreference.com/w/cpp/string/byte/strtok
could be very usefull here !!!
https://www.javatpoint.com/how-to-split-strings-in-cpp
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

// #include "LibTeleinfo.h" 

uint8_t receiver_mac[] = {0x36, 0x33, 0x33, 0x33, 0x33, 0x33};
char c;
uint32_t i = 0;
uint32_t n = 0;

char buff[3000];
uint32_t buff_idx = 0;
bool buff_started = false;

SoftwareSerial Linky;

/* struct from LibTeleinfo created by C. Hallard
   thanks to C. Hallard http://hallard.me/category/tinfo */
typedef struct _Value Value;
struct _Value
{
  Value *next; // next element
  time_t  ts;      // TimeStamp of data if any
  char checksum;// checksum
  char  * label;    // LABEL of value name
  char  * value;   // value
  char  * horo;    // date if any
  char  * line;    // The full raw line containing label [+ horo] + value + checksum
};

typedef struct _valuesList valuesList;
struct _valuesList {
    Value * first;
    uint32_t number;
};

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
Value setValueFields(Value * value) {
    char * line;
    char * field;
    uint8_t len;
    uint8_t nb_fields = 0;
    uint8_t i = 0;
    len = strlen(value->line);
    line = (char *) malloc(len + 1);
    strcpy(line, value->line);
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
    line = (char *) malloc(len + 1);
    strcpy(line, value->line);
    field = strtok(line, "\t");
    while (field != NULL) {
        // cout << field;
        if (i == 0) {
            value->label = (char *) malloc(strlen(field));
            strcpy(value->label, field);
        }
        if (nb_fields == 3) {
            if (i == 1) value->value = field;
            if (i == 2) value->checksum = *field;
            value->horo = NULL;
        }
        if (nb_fields == 4) {
            if (i == 1) value->horo = field;
            if (i == 2) value->value = field;
            if (i == 3) value->checksum = *field;
        }
        field = strtok(NULL, "\t");
        i++;
    }
    return(*value);
}

/*
Create a list of all lines of the buffer/frame
Each line is a struct Value. In this function,
only 'line' and 'next' attributes are set.
The struct 'Values' is used to manage the chained list
of values.
*/
valuesList getValuesFromFrame(char * frame) {
    valuesList values;
    uint32_t number = 0;
    char * F_line; // one line from Frame _F_
    int len;
    Value * prev_value;

    F_line = strtok(frame, "\n");
    while (F_line != NULL) {
        len = strlen(F_line) + 1;
        Value * current_value = new Value;

        current_value->line = F_line;
        if (number == 0) {
            current_value->next = NULL;
            values.first = current_value;
            values.number = 0;
        } else {
            current_value->next = NULL;
            prev_value->next = current_value;
            values.number = number;
        }
        prev_value = current_value;
        F_line = strtok(NULL, "\n");
        number++;
    }
    return(values);
}

/* */
void getUsefullData() {
  /* */
}

void sendUsefullData() {
  /* */
}

/*
buffer == frame
*/
void manageFrame(char *frame) {
  valuesList values;
  Value * val;

  values = getValuesFromFrame(frame);
  val = values.first;
  while (val) {
    setValueFields(val);
    // displayValue(val);
    val = val->next;
  }
  val = values.first;
  
}

// raw data acquired form Serial
// buff is a global variable.
void fillBuffer(char c) {
  switch (c)  {
    case STX:
      // Serial.println("Start") ;
      clearBuffer();
      buff_started = true;
      break;
    case ETX:
      // we convert buffer to frame, then later used data
      // Serial.println("End") ;
      buff_started = false;
      buff[buff_idx++] = 0;
      manageFrame(buff);
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
  Serial.println("ESPNow sender Demo");
  // pinMode(ONBOARD_LED, OUTPUT);
  Linky.begin(9600, SWSERIAL_7E1, 16, 4);
  // Linky.begin(16, 4);
  /*
  tinfo.init(TINFO_MODE_STANDARD);
  WiFi.mode(WIFI_MODE_STA);
  WiFi.disconnect();
  ESPNow.init();
  ESPNow.add_peer(receiver_mac);
  */
}

void loop() {
  static uint32_t i = 0;
  /* static uint8_t a = 0;
  delay(100);
  ESPNow.send_message(receiver_mac, &a, 1);
  Serial.println(a++); */
  if (Linky.available()){
    c = Linky.read();
    // we ignore \r (== cr == 13)
    if (c != 13) fillBuffer(c);
    i++;
  }
  if (i > 5000){
    Serial.println(F("XXXX"));
    Serial.println(F("XXXX"));
    Serial.println(F("XXXX"));
    Serial.println(F("XXXX"));
    delay(10000);
    i = 0;
  }
  // Serial.println(F("."));
  // delay(5000);
}