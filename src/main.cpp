
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
#include <../lib/homeWifi.h>
#include <WebServer.h>
// const char* ssid = HOME_SSID;
// const char* password = HOME_WIFI_PASS;
WebServer server(80);

// #include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define WIRE Wire
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &WIRE);

#define DEBUG
// #undef DEBUG

#ifdef DEBUG
  #define debug(x) Serial.print(x)
  #define debugln(x) Serial.println(x)
#else
  #define debug(x)
  #define debugln(x)
#endif

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
// uint8_t receiver_mac[] = {0x24, 0x0A, 0xC4, 0x5F, 0x77, 0xB0};
// esp_now_peer_info_t peerInfo;


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
bool frame_ok = false;
bool buffer_full = false;

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
  // bool frame_ok;

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
      buffer_full = true;
      break;
    default:
      if (buff_started) {
        buff[buff_idx++] = c;
      }
    }
}

// buff is a global variable
void fillBuffer2() {
  buff_idx = 0;
  c = Linky.read();
  // we read a char until we meet the begining of the frame (STX)
  while (c != STX) {
    c = Linky.read();
  }
  // we fill the buffer until we get ETX
  while (c != ETX) {
    // buff[buff_idx++] = c;
    debug(c);
    c = Linky.read();
  }
  return ;

  // we end the buffer with a 0
  buff[buff_idx] = 0;
}

void getData() {
  while (1) {
    if (Linky.available()){
      c = Linky.read();
      fillBuffer(c);
      if (buffer_full) {
        break;
      }
      // debug(c);
    }
  }
}

/* Old version, before webserver.
void getData() {
  while (1) {
    if (Linky.available()){
      c = Linky.read();
      fillBuffer(c);
    }
  }
}
*/

void handleRoot(){  // Page d'accueil La page HTML est mise dans le String page
//  Syntaxe d'écriture pour être compatible avec le C++ / Arduino
// String page = " xxxxxxxx ";
// page += " xxxxx ";
// etc ...
  String page = "<!DOCTYPE html>";  // Début page HTML
    page += "<head>";
    page += "    <title>Serveur ESP32</title>";
    page += "    <meta http-equiv='refresh' content='60' name='viewport' content='width=device-width, initial-scale=1' charset='UTF-8'/>";
    page += "</head>";
    page += "<body lang='fr'>";
    page += "    <h1>Serveur</h1>";
    page += "    <p>Ce serveur est hébergé sur un ESP32</p>";
    page += "    <p><i>Créé par EH</i></p>";
    page += "    <p>Une partie du code \"web server\" provient de ";
    page += "<a target=\"_blank\" href=\"http://emery.claude.free.fr/esp32-serveur-web-simple.html\">";
    page += "http://emery.claude.free.fr/esp32-serveur-web-simple.html</a></p>";
    page += "</body>";
    page += "</html>";  // Fin page HTML

    server.send(200, "text/html", page);  // Envoie de la page HTML
}

void handleNotFound(){  // Page Not found
  server.send(404, "text/plain","404: Not found");
}

void handle_getEDF_Data() {
  char x_label[20];
  char * x_val;
  char cc[10];
  static u_int16_t ii = 0;
  /*
  clearValues();
  clearBuffer();
  debug("fram_ok : ");
  debugln(frame_ok);
  getData();
  strcpy(x_label,"SINSTS1");
  x_val = getValueFor(x_label);
  
  Serial.print("x_val = ");
  Serial.println(x_val);
  */
  
  // server.sendHeader("Location","/");
  // server.send(303);
  // server.send(200, "text/plain", x_val);
  server.send(200, "text/plain", itoa(ii, cc, 10));
  ii++;
  clearBuffer();
  fillBuffer2();
  return;
  /*
  fillBuffer2();
  c = buff[i];
  while (c) {
    debug(c);
    c = buff[i++];
  }
  */
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
  
  // pinMode(ONBOARD_LED, OUTPUT);
  Linky.begin(9600, SWSERIAL_7E1, 16, 4);
  delay(1000);
  Serial.print("Linky.available() = ");
  Serial.println(Linky.available());
  Serial.println(WiFi.macAddress());
  clearValues();
  Serial.print("Connecting to Wifi...");

  WiFi.begin(HOME_SSID, HOME_WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");
  Serial.println(WiFi.localIP());
  server.on("/", handleRoot);
  server.on("/data", handle_getEDF_Data);
  server.onNotFound(handleNotFound);
  server.begin();
}

void loop() {
  static u_int64_t nb = 0;
  // getData();
  /* */
  if (Linky.available()){
     c = Linky.read();
     nb++;
     fillBuffer(c);
     // debug(c);
  }
  
  /* */
  // server.handleClient();
}