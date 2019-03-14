# cs41_jazzHands
CS41 Final Project
*Team: Meera Radhakrishnan, Andrea Ramirez*

## Introduction
Welcome to Jazz Hands! 

This project uses a glove equipped with flex sensors on each finger to control sounds and visuals. The glove uses an Adafruit Metro Mini microcontroller to transmit flex measurements for each finger to the computer via serial communication. Python is used to read the measurements, do appropriate processing, and then generate the final sounds and visualizations. Each finger controls the weight of a different frequency component to add to the final sound, and visuals display the weights of each of the frequencies and the sound waveform in the time domain in real time. Our code plays an A major chord, and each of three flex sensors control the weights of A, C#, and E in the output sound.

##Technical Overview

Our code makes use of four key Python modules: PySerial (to process serial input from the glove), PyAudio (to generate sound), Numpy (for data processing of sound samples) and Matplotlib (to generate visuals).


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
To run the code, first make sure your Metro Mini is outputing serial data at a 9600 baud rate. The data from the 3 sensors should be all transmitted in the same line/buffer, separtaed by spaces. Check which serial port your Metro Mini is connected to (COM ports for Windows  or /dev/tty port for Mac and Linux). Update the serial port definition depending on the port you are using. An example definition is shown below: 

    #Serial port definition. Change this line according to the port you are using for serial communication.
    #COM3 is the serial communication port in this example
    ser = serial.Serial('COM3', 9600);

Once the serial port is set, run full_audio_test.py and have fun playing with the sensors!

*Optional: Each sensor has a different range of values it can transmit as no two sensors are equal. You can edit the NORMALIZE_SENS list to match your specific sensor for better results.*

## Acknowledgments 
We want to thank Sam Redmond and the CS41 staff for all their help and support!




