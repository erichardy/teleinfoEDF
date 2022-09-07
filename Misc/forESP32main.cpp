
// https://www.javatpoint.com/how-to-split-strings-in-cpp

#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

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
  char  * line;    // The full raw line containing label + value + horo + checksum
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

Value * getValueFor(valuesList valList, char * label)	{
	Value *val; // pointer returned
	val = valList.first;
	while (val) {
		if (!strcmp(val->label, label)) {
			break;
		}
		val = val->next;
	}
	return val;
}

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



int main() {
	char ch;
	uint32_t i = 0;
	uint32_t n = 0;
	uint32_t frame_idx = 0;
	uint32_t size;
	char * memblock;
	char * frame;
	valuesList values;
	Value * val;
	const char *file = "platformio-device-monitor-220904-190632.log";
	ifstream esp32logs (file, ios::in|ios::binary|ios::ate);
	size = esp32logs.tellg();
	memblock = new char [size];
	frame = new char [size];
	
	if (esp32logs.is_open()) {
		esp32logs.seekg (0, ios::beg);
		esp32logs.read (memblock, size);
		esp32logs.close();
	}

	bool start = false;
	char * flagStart;
	uint32_t start_idx = 0;
	flagStart = new char[5];
	// here we get a block reading a file
	// the frame starts with the label 'ADSC'
	//
	// for the ESP32, the block/frame starts with STX
	// and ends with ETX
	// !!! we must thing to bypass \cr (char 13)
	for (i = 0; i < size ; i++) {
		ch = memblock[i];
		if (i < size - 5) {
			for (n = 0; n < 4; n++) flagStart[n] = memblock[i + n];
			flagStart[5] = 0;
			if (! strcmp(flagStart, "ADSC")) {
				if (start == true) {
					break;
					}
				if (start == false) {
					start = true;
				}
			}
		}
		// we don't need \cr
		if (start) {
			if (ch != 13) frame[frame_idx++] = ch;
		}
	}
	frame[frame_idx++] = 0;
	values = getValuesFromFrame(frame);
	val = values.first;
	while (val) {
		// cout << val->line;
		setValueFields(val);
		displayValue(val);
		val = val->next;
	}

	cout << "======================" << endl;
	char x_label[] = "SINSTS1";
	val = getValueFor(values, x_label);
	displayValue(val);


	return 0;
}
