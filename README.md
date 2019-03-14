# cs41_jazzHands
CS41 Final Project
*Team: Meera Radhakrishnan, Andrea Ramirez*

## Introduction
Welcome to Jazz Hands! 

This project uses a glove equipped with flex sensors on each finger to control sounds and visuals. The glove uses an Adafruit Metro Mini microcontroller to transmit flex measurements for each finger to the computer via serial communication. Python is used to read the measurements, do appropriate processing, and then generate the final sounds and visualizations. Each finger controls the weight of a different frequency component to add to the final sound, and visuals display the weights of each of the frequencies and the sound waveform in the time domain in real time. Our code plays an A major chord, and each of three flex sensors control the weights of A, C#, and E in the output sound.

## Technical Overview

Our code makes use of four key Python modules: PySerial (to process serial input from the glove), PyAudio (to generate sound), Numpy (for data processing of sound samples) and Matplotlib (to generate visuals).

To better understand the flow of our Python code, it is helpful to understand how our glove hardware works.

#### Hardware Overview
Flex sensors (such as the ones here: https://www.adafruit.com/product/1070) are simply variable resistors, or potentiometers, with a maximum value of approximately 50kOhm. As the finger is flexed, the resistance of the flex sensor decreases. Since the Metro Mini can only read voltage signals, we use a simple application of Ohm's Law (voltage = current * resistance) to convert the resistance measurements to voltage signals that the Metro Mini can read. We include a picture of the circuit schematic HERE. TODO The Metro Mini then collects resistance measurements from all of the fingers 4 times per second. These resistance measurements are normalized and then transmitted continuously to the computer via serial.

#### Software Overview
At a high level, our code sets up our serial link, audio, and visualizations and then runs continuously in a while(True) loop. Within this loop, it continuously reads in flex sensor measurements from the Metro Mini, normalizes them to an expected maximum value, uses them to weight each of the frequency components, generates weighted sine waves for each of the frequencies, and writes them to the audio stream. The time domain and frequency domain plots are then updated using the latest measurements. 

#### Reading and Processing Serial Output
The PySerial library can be used to read serial data sent to a computer via USB. First, the serial link must be set up using the appropriate serial port on the computer (all serial data into the computer goes to a particular serial port on the computer, which can be thought of as an address for the serial data) and the baud rate expected from the Metro Mini (9600). We expect the data to be in the following format: numbers from all of the flex sensors at a given point in time are in one line, and the measurements from each of the fingers are space-separated on that line. We manipulate these measurement strings into an array of numbers, which can then be used to manipulate our output sound.

#### Creating Sound Samples and Generating Audio
All sounds can be thought of as a sum of sine waves of different amplitudes and phase shifts. In our code, we generate a simple sound: a pure A major chord. This sound is a sum of only three sine waves: one with a frequency of 440 Hz (A), one with a frequency of 554.37 Hz (C#) and one with a frequency of 659.25 Hz (E).

First, we need to set up the audio stream. We create a pyaudio object, and set up the volume, sampling rate, and duration of the sound. We then open the audio stream using pyaudio.open().

Next, within our while(True) loop, we need to transform the flex sensor outputs into appropriately weighted sound samples.

#### Generating and Updating Visualizations


## Lessons Learned
- Better understand compatibility and dependencies
- Permissions issue to access serial ports through WSL
- WSL doesn't even support audio
- More confidence in using Python to interface with hardware, which is exciting for future project possibilities


## Setup
#### Software
In order to run our code, make sure to install the following libraries:
* PySerial (pip install serial)
* PyAudio (pip install pyaudio)
* Numpy (pip install numpy)
* Matplotlib (pip install matplotlib)

*Notes:* 

*1. The PyAudio library isn't compatible with Python 3.7. Please make sure you are using Python 3.6 or lower.*

*2. Do not run this code in a Windows Subsytem for Linux, as WSL does not support audio.* 

You may also need Xming or a similar program to be able to see the frequency plots.

#### Hardware
Our code's serial communication was tested with an Adafruit Metro Mini at 9600 baud rate. The Metro Mini sent data from 3 sensors (or potentiometers) to our computer through serial. The flex sensors used had a 50k resistance, so its preferrable to use 50k potentiometers if not enough flex sensors are available. The relevant Arduino code can be found in pot_test.
TODO probably more instructions on how to build the circuit

## Running the Code
- Upload Arduino code

To run the code, first make sure your Metro Mini is outputing serial data at a 9600 baud rate. The data from the 3 sensors should be all transmitted in the same line/buffer, separtaed by spaces. Check which serial port your Metro Mini is connected to (COM ports for Windows  or /dev/tty port for Mac and Linux). Update the serial port definition depending on the port you are using. An example definition is shown below: 

    #Serial port definition. Change this line according to the port you are using for serial communication.
    #COM3 is the serial communication port in this example
    ser = serial.Serial('COM3', 9600);

Once the serial port is set, run full_audio_test.py and have fun playing with the sensors!

*Optional: Each sensor has a different range of values it can transmit as no two sensors are equal. You can edit the NORMALIZE_SENS list to match your specific sensor for better results.*

## Possible Modifications for More Fun
- Can add more pots
- Can change the base frequency

## Acknowledgments 
We want to thank Sam Redmond and the CS41 staff for all their help and support!




