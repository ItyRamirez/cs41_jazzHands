# cs41_jazzHands
CS41 Final Project
*Team: Meera Radhakrishnan, Andrea Ramirez*

## Introduction
Welcome to Jazz Hands! This project aimed to create sounds and visuals from data gathered from a glove with flex sensors. By using serial communcation, we transmitted values from the flex sensors (and some potentiometers) to our computer. The weights of different frequencies were adjusted depending on the sensors. These weights determined the audio output from our code, which played an A major chord and displayed the output audio waveform as well as the weights of the notes creating the chords. 

## Setup
#### Software
In order to run our code, make sure to install the following libraries:
* PySerial
* PyAudio
* Numpy
* Matplotlib

*Notes:* 

*1. The PyAudio library isnt compatible with Python 3.7. Please make sure you are using Python 3.6 or lower*

*2. Do not run this code in a Windows Subsytem for Linux, as audio output isnt supported* 

You may also need Xming or a similar program to be able to see the frequency plots.

#### Hardware
Our code's serial communication was tested with an Adafruit Metro Mini at 9600 baud rate. The Metro Mini sent data from 3 sensors (or potentiometers) to our computer through serial. The flex sensors used had a 50k resistance, so its preferrable to use 50k potentiometers if not enough flex sensors are available. 

## Running the Code
To run the code, first make sure your Metro Mini is outputing serial data at 9600 baud rate. The data from the 3 sensors should be all transmitted in the same line/buffer, separtaed by spaces. Check which serial port your Metro Mini is connected to (COM ports for Windows  or /dev/tty port for Mac and Linux). Update the serial port definition depending on the port you are using. An example definition is shown below: 

    #Serial port definition. Change this line according to the port you are using for serial communication.
    #COM3 is the serial communication port in this example
    ser = serial.Serial('COM3', 9600);

Once the serial port is set, run full_audio_test.py and have fun playing with the sensors!

*Optional: Each sensor has a different range of values it can transmit as no two sensors are equal. You can edit the NORMALIZE_SENS list to match your specific sensor for better results.*

## Acknowledgments 
We want to thank Sam Redmond and the CS41 staff for all their help and support!




