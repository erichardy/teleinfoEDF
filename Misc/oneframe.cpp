
/*
alias a='./a.out' ; alias c='c++ oneframe.cpp'
*/

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

/* set the fields of a value from each which contains
   label\tvalue\tchecksum\r
   or
   label\t[horo\t]value\tchecksum\r
   \t = ht = 9
   \r = cr = 13
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
	// cout << strlen(line) << " " << line;
	// premier passage pour compter les champs
	// si 4 champs => le second champ est l'horodatage
	field = strtok(line, "\t");
	while (field != NULL) {
		// cout << field << endl;
		nb_fields++;
		field = strtok(NULL, "\t");
	}
	/*
	line = value->line;
	cout << line << " ";
	*/
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
	// cout << value->label;

	/*
	if (nb_fields == 1) cout << "1" << endl;
	if (nb_fields == 2) cout << "2" << endl;
	if (nb_fields == 3) cout << "3" << endl;
	if (nb_fields == 4) cout << "4" << endl;
	if (nb_fields == 5) cout << "5" << endl;
	if (nb_fields < 1) cout << "< 1 !!!" << endl;
	if (nb_fields > 5) cout << "> 5 !!!" << endl;
	cout << "---" << endl;
	*/
	return(*value);
}

valuesList getLinesFromFrame(char * frame) {
	valuesList values;
	uint32_t number = 0;
	char * F_line; // one line from Frame _F_
	int len;
	char * element;
	// Value current_value;
	Value * prev_value;

	F_line = strtok(frame, "\n");
	while (F_line != NULL) {
		len = strlen(F_line) + 1;
		Value * current_value = new Value;
		// prev_line = &line; // store line pointer for next if any...
		// line.next = NULL;
		// strcpy(line.data, F_line);
		// getDataFromLine(str_line);
		// cout << F_line << endl;
		//cout << "============" << endl;

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
	// streampos size;
	uint32_t size;
	char * memblock;
	char * frame;
	valuesList values;
	Value * val;
	const char *file = "platformio-device-monitor-220904-190632.log";
	// ifstream esp32logs ("platformio-device-monitor-220904-190632.log", ios::in|ios::binary|ios::ate);
	ifstream esp32logs (file, ios::in|ios::binary|ios::ate);
	size = esp32logs.tellg();
	// cout << size << endl;
	memblock = new char [size];
	frame = new char [size];
	// cout << sizeof(memblock)  <<endl;
	// frame[frame_idx++] = 10;
	
	if (esp32logs.is_open()) {
		// cout << "Fichier ouvert" <<endl;
		esp32logs.seekg (0, ios::beg);
		esp32logs.read (memblock, size);
		esp32logs.close();
	}

	bool start = false;
	char * flagStart;
	uint32_t start_idx = 0;
	flagStart = new char[5];

	for (i = 0; i < size ; i++) {
		// cout << memblock[i];
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
				// cout << memblock[i] << memblock[i + 1] << memblock[i + 2] << memblock[i + 3] << " " << start << endl;
				// cout << memblock[i] << memblock[i + 1] << memblock[i + 2] << memblock[i + 3] << " " << start << " " << i << endl;
			}
		}
		if (start) {
			if (ch != 13) frame[frame_idx++] = ch;
		}
	}
	// cout << "fin de boucle, frame_idx = " << frame_idx << endl;
	frame[frame_idx++] = 0;
	/*
	for (i = 0; i < frame_idx; i++) {
		cout << frame[i];
	}
	*/
	values = getLinesFromFrame(frame);
	/*
	cout << values.number << endl;
	val = values.first;
	cout << val->line << endl;
	val = val->next;
	cout << val->line << endl;
	for (i = 0; i <= values.number; i++) {
		if (i == 0) {
			val = values.first;
		} else {
			val = val->next;
		}
		cout << val->line << endl;
	}
	cout << "i = " << i << endl;
	cout << "============================" << endl;
	*/
	val = values.first;
	while (val) {
		// cout << val->line;
		setValueFields(val);
		displayValue(val);
		cout << "=====================" << endl;
		val = val->next;
	}

	return 0;
}
