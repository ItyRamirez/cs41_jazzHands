

const int FLEX_PIN_1 = A0; //Pin connected to the voltage divider output of the first flex sensor
//const int FLEX_PIN_2 = A1; //Pin connected to the voltage divider output of the second flex sensor

//Measure the voltage at 5V and the actual resistance of the 50k equivalent resistor, and
//enter them below. This makes the angle calculation much more accurate.

const float VCC = 4.84; //Measured voltage of Arduino 5V line
//const float R_DIV = 49000.0; //Actual resistance of the 50k equivalent resistor
const float R_DIV = 40000.0;

//Upload the code and try to determine an average value of resistance when the 
//sensor is not bent, and when it it bent at 90 degrees. Enter those and reload
//the code for a more accurate angle estimate.
//const float STRAIGHT_RESISTANCE_1 = 32773.25; //resistance when straight
//const float BEND_RESISTANCE_1 = 73559.91; //resistance at 90 degrees = 50% of range of motion


//const float STRAIGHT_RESISTANCE_2 = 23753; //resistance of second flex sensor when straight
//const float BEND_RESISTANCE_2 = 55000; //resistance of second flex sensor when finger at 90 degrees = 50% range of motion

const float STRAIGHT_RESISTANCE_1 = 0;
const float BEND_RESISTANCE_1 = 20000;

void setup() {
  //set the data rate for the SoftwareSerial port
  //BT.begin(9600);
 Serial.begin(9600);
}

void loop() {
   //Read the ADC
   int flexADC_1 = analogRead(FLEX_PIN_1);
   //int flexADC_2 = analogRead(FLEX_PIN_2);

   //Calculate the voltage that the ADC read
   float flexV_1 = flexADC_1 * VCC/1023.0;
   //float flexV_2 = flexADC_2 * VCC/1023.0;

   //Calculate the resistance of the flex sensor
   float flexR_1 = R_DIV * (VCC - flexV_1) / flexV_1;
   //float flexR_2 = R_DIV * (VCC - flexV_2) / flexV_2;

   //Use the calculated resistance to estimate the range of motion that the sensor
   //is currently exhibiting. This is estimated by mapping the measured resistance
   //onto the known resistance at 0% of range of motion (finger fully extended) to
   //50% of range of motion (finger bent at 90 degrees).
   float percentage1 = map(flexR_1, STRAIGHT_RESISTANCE_1, BEND_RESISTANCE_1, 0, 50);
   //float percentage2 = map(flexR_2, STRAIGHT_RESISTANCE_2, BEND_RESISTANCE_2, 0, 50);  

    int percentage1Int = percentage1 / 1; 
//    int percentage2Int = percentage2 / 1; 
    
    if (percentage1Int < 10) {     
      //BT.print("0");
      Serial.print("0");
    }
    
    //BT.print(percentage1Int); //Range of motion of index finger
    //BT.print(" "); 
    Serial.print(percentage1Int); //Range of motion of index finger
    Serial.print("\n"); 
   
    //if (percentage2Int < 10) {     
      //BT.print("0");
      //Serial.print("0");
    //}

    //BT.print(percentage2Int); //Range of motion of middle finger
    //BT.println(";");
    //BT.println();

//    Serial.print(percentage2Int); //Range of motion of middle finger
    //Serial.println(";");
    //Serial.println();
  

   delay(250); //Read the sensor at 4Hz (4 times per second)
}
