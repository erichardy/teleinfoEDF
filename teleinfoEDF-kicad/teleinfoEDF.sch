EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Isolator:4N35 U?
U 1 1 624B23ED
P 4400 2950
F 0 "U?" H 4400 3275 50  0000 C CNN
F 1 "4N35" H 4400 3184 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 4200 2750 50  0001 L CIN
F 3 "https://www.vishay.com/docs/81181/4n35.pdf" H 4400 2950 50  0001 L CNN
	1    4400 2950
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N4148 D?
U 1 1 624B42BB
P 3750 2900
F 0 "D?" V 3704 2979 50  0000 L CNN
F 1 "1N4148" V 3795 2979 50  0000 L CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 3750 2725 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 3750 2900 50  0001 C CNN
	1    3750 2900
	0    1    1    0   
$EndComp
$Comp
L Transistor_FET:2N7000 Q?
U 1 1 624B7FB6
P 5250 3050
F 0 "Q?" H 5454 3096 50  0000 L CNN
F 1 "2N7000" H 5454 3005 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 5450 2975 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N7000.pdf" H 5250 3050 50  0001 L CNN
	1    5250 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 624BA605
P 3250 2700
F 0 "R?" V 3043 2700 50  0000 C CNN
F 1 "1.3k" V 3134 2700 50  0000 C CNN
F 2 "" V 3180 2700 50  0001 C CNN
F 3 "~" H 3250 2700 50  0001 C CNN
	1    3250 2700
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 624BAE89
P 4900 3350
F 0 "R?" H 4830 3304 50  0000 R CNN
F 1 "10k" H 4830 3395 50  0000 R CNN
F 2 "" V 4830 3350 50  0001 C CNN
F 3 "~" H 4900 3350 50  0001 C CNN
	1    4900 3350
	-1   0    0    1   
$EndComp
$Comp
L Device:R R?
U 1 1 624BB5DC
P 5350 2450
F 0 "R?" H 5280 2404 50  0000 R CNN
F 1 "10k" H 5280 2495 50  0000 R CNN
F 2 "" V 5280 2450 50  0001 C CNN
F 3 "~" H 5350 2450 50  0001 C CNN
	1    5350 2450
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 624C1900
P 4900 3650
F 0 "#PWR?" H 4900 3400 50  0001 C CNN
F 1 "GND" H 4905 3477 50  0000 C CNN
F 2 "" H 4900 3650 50  0001 C CNN
F 3 "" H 4900 3650 50  0001 C CNN
	1    4900 3650
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR?
U 1 1 624C20A3
P 5350 2150
F 0 "#PWR?" H 5350 2000 50  0001 C CNN
F 1 "VCC" H 5367 2323 50  0000 C CNN
F 2 "" H 5350 2150 50  0001 C CNN
F 3 "" H 5350 2150 50  0001 C CNN
	1    5350 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 2150 5350 2200
Wire Wire Line
	5350 2200 4950 2200
Wire Wire Line
	4950 2200 4950 2950
Wire Wire Line
	4950 2950 4700 2950
Connection ~ 5350 2200
Wire Wire Line
	5350 2200 5350 2300
Wire Wire Line
	4700 3050 4900 3050
Wire Wire Line
	5350 2850 5350 2750
Wire Wire Line
	4900 3200 4900 3050
Connection ~ 4900 3050
Wire Wire Line
	4900 3050 5050 3050
Wire Wire Line
	4900 3500 4900 3600
Wire Wire Line
	5350 3250 5350 3600
Wire Wire Line
	5350 3600 4900 3600
Connection ~ 4900 3600
Wire Wire Line
	4900 3600 4900 3650
Wire Wire Line
	3750 3050 4100 3050
Wire Wire Line
	4100 2700 3750 2700
Wire Wire Line
	4100 2700 4100 2850
Wire Wire Line
	3750 2700 3750 2750
Connection ~ 3750 2700
Wire Wire Line
	3750 2700 3400 2700
Wire Wire Line
	5350 2750 5750 2750
Connection ~ 5350 2750
Wire Wire Line
	5350 2750 5350 2600
Wire Wire Line
	3750 3050 2800 3050
Connection ~ 3750 3050
Wire Wire Line
	3100 2700 2800 2700
Wire Wire Line
	2800 2700 2800 2800
Wire Wire Line
	2800 2800 2650 2800
Text Label 5650 2750 0    50   ~ 0
Out
Text Label 2650 2800 0    50   ~ 0
I2
Text Label 2650 2950 0    50   ~ 0
I1
Wire Wire Line
	2800 3050 2800 2950
Wire Wire Line
	2800 2950 2650 2950
Text Notes 7100 6700 0    50   ~ 0
à partir de http://sarakha63-domotique.fr/nodemcu-teleinformation-wifi/#prettyPhoto
$EndSCHEMATC
