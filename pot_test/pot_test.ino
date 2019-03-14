
const int FLEX_PIN_1 = A0; //Pin connected to the voltage divider output of 50k pot
const int FLEX_PIN_2 = A3; //Pin connected to the voltage divider output of the second 50k pot
const int FLEX_PIN_3 = A2; //Pin connected to the voltage divider output of the 20k pot

const float VCC = 4.84; //Measured voltage of Arduino 5V line
const float R_DIV = 65000.0; //Actual resistance of the 130k||130k resistor

const float POT1_LO = 0;
const float POT1_HI = 50000;
const float POT2_LO = 0;
const float POT2_HI = 50000;
const float POT3_LO = 0;
const float POT3_HI = 50000;

void setup() {
  Serial.begin(9600);
}

void loop() {
   //Read the ADC
   int flexADC_1 = analogRead(FLEX_PIN_1);
   int flexADC_2 = analogRead(FLEX_PIN_2);
   int flexADC_3 = analogRead(FLEX_PIN_3);

   //Calculate the voltage that the ADC read
   float flexV_1 = flexADC_1 * VCC/1023.0;
   float flexV_2 = flexADC_2 * VCC/1023.0;
   float flexV_3 = flexADC_3 * VCC/1023.0;

   //Calculate the resistance of the flex sensor
   float flexR_1 = R_DIV * (VCC - flexV_1) / flexV_1;
   float flexR_2 = R_DIV * (VCC - flexV_2) / flexV_2;
   float flexR_3 = R_DIV * (VCC - flexV_3) / flexV_3;

   //Use the calculated resistance to estimate the range of motion that the sensor
   //is currently exhibiting.
   float percentage1 = map(flexR_1, POT1_LO, POT1_HI, 0, 100);
   float percentage2 = map(flexR_2, POT2_LO, POT2_HI, 0, 100);  
   float percentage3 = map(flexR_3, POT3_LO, POT3_HI, 0, 100);  

   int percentage1Int = percentage1 / 1; 
   int percentage2Int = percentage2 / 1; 
   int percentage3Int = percentage3 / 1;
    
    Serial.print(percentage1Int); //Range of motion of index finger
    Serial.print(" ");
    Serial.print(percentage2Int);
    Serial.print(" ");
    Serial.print(percentage3Int);
    Serial.print("\n"); 

   delay(1000); //Read the sensor at 1Hz (1 time per second)
}
