# cs41_jazzHands
CS41 Final Project

*Team: Meera Radhakrishnan, Andrea Ramirez*

Go to: https://github.com/ItyRamirez/cs41_jazzHands for pictures

## Introduction
Welcome to Jazz Hands! 

This project uses a glove equipped with flex sensors on each finger to control sounds and visuals. The glove uses an Adafruit Metro Mini microcontroller to transmit flex measurements for each finger to the computer via serial communication. Python is used to read the measurements, do appropriate processing, and then generate the final sounds and visualizations. Each finger controls the weight of a different frequency component to add to the final sound, and visuals display the weights of each of the frequencies and the sound waveform in the time domain in real time. Our code plays an A major chord, and each of three flex sensors control the weights of A, C#, and E in the output sound.

## Technical Overview

Our code makes use of four key Python modules: PySerial (to process serial input from the glove), PyAudio (to generate sound), Numpy (for data processing of sound samples) and Matplotlib (to generate visuals).

To better understand the flow of our Python code, it is helpful to understand how our glove hardware works.

#### Hardware Overview
Flex sensors (such as the ones here: https://www.adafruit.com/product/1070) are simply variable resistors, or potentiometers, with a maximum value of approximately 50kOhm. As the finger is flexed, the resistance of the flex sensor decreases. Since the Metro Mini can only read voltage signals, we use a simple application of Ohm's Law (voltage = current * resistance) to convert the resistance measurements to voltage signals that the Metro Mini can read. We include a picture of the circuit schematic below. The Metro Mini then collects resistance measurements from all of the fingers 4 times per second. These resistance measurements are normalized and then transmitted continuously to the computer via serial.

![alt text](https://github.com/ItyRamirez/cs41_jazzHands/blob/master/Schematic.JPG)

#### Software Overview
At a high level, our code sets up our serial link, audio, and visualizations and then runs continuously in a while(True) loop. Within this loop, it continuously reads in flex sensor measurements from the Metro Mini, normalizes them to an expected maximum value, uses them to weight each of the frequency components, generates weighted sine waves for each of the frequencies, and writes them to the audio stream. The time domain and frequency domain plots are then updated using the latest measurements. 

#### Reading and Processing Serial Output
The PySerial library can be used to read serial data sent to a computer via USB. First, the serial link must be set up using the appropriate serial port on the computer (all serial data into the computer goes to a particular serial port on the computer, which can be thought of as an address for the serial data) and the baud rate expected from the Metro Mini (9600). We expect the data to be in the following format: numbers from all of the flex sensors at a given point in time are in one line, and the measurements from each of the fingers are space-separated on that line. We manipulate these measurement strings into an array of numbers, which can then be used to manipulate our output sound.

#### Creating Sound Samples and Generating Audio
All sounds can be thought of as a sum of sine waves of different amplitudes and phase shifts. In our code, we generate a simple sound: a pure A major chord. This sound is a sum of only three sine waves: one with a frequency of 440 Hz (A), one with a frequency of 554.37 Hz (C#) and one with a frequency of 659.25 Hz (E).

First, we need to set up the audio stream. We create a pyaudio object, and set up the volume, sampling rate, and duration of the sound. We then open the audio stream using pyaudio.open().

Next, within our while(True) loop, we need to transform the flex sensor outputs into appropriately weighted sound samples. From the processed serial data, on each iteration we have an array of three numbers: the weight of A, the weight of C#, and the weight of E. We first normalize these weights to the maximum expected value from each sensor to get a fraction. Then, for each note, we generate a set of samples representing that note's sine wave, multiply all of the samples by that note's weight, and then add it to the final sample. The result is an array of sound samples containing a sum of all three sine waves appropriately weighted.

To play the sound, we simply call stream.write(samples).

#### Generating and Updating Visualizations
Having successfully generated sounds weighted by the flex sensor inputs, we decided to develop visualizations of the music using matplotlib. Generating real-time visualizations was particularly challenging and required us to gain more proficiency with the matplotlib library.

Our visualizations consist of a single window with two subplots. The top subplot displays the time domain waveform (i.e. the final sum of sine waves plotted vs. time) and the bottom subplot displays a bar graph that shows the weights of each of the frequencies. Both subplots are updated with every new measurement.

First, we set up the figure that will hold the visualizations before the while(True) loop. Inside the while(True) loop, we dynamically rescale the x axis of the time domain plot (based on the frequency content of the notes) and update the data for both plots in each iteration. matplotlib.draw() updates the plot visuals.

Here is an example of the visual output:

![alt text](https://github.com/ItyRamirez/cs41_jazzHands/blob/master/visualizations.PNG)

## Lessons Learned
By doing this project, we got a much better understanding of how to navigate the Python ecosystem and anticipate compatibility and dependency issues. We ran into multiple issues, including implementing PySerial and PyAudio effectively on WSL. Including hardware added an additional layer of complexity, but we learned lots of useful concepts that expand the range of exciting possibilities for interfacing with future hardware projects.

## Setup
#### Software
In order to run our code, make sure to install the following libraries:
* PySerial (pip install pyserial)
* PyAudio (pip install pyaudio)
* Numpy (pip install numpy)
* Matplotlib (pip install matplotlib)

*Notes:* 

*1. The PyAudio library isn't compatible with Python 3.7. Please make sure you are using Python 3.6 or lower.*

*2. Do not run this code in a Windows Subsytem for Linux, as WSL does not support audio.* 

You may also need Xming or a similar program to be able to see the frequency plots.

#### Hardware
To set up the circuit, create a simple voltage divider between each potentiometer/flex sensor and a known resistor (our Arduino code in pot_test assumes a known resistor of 65kOhm, but any resistor relatively close to 50kOhms will work as long as the relevant R_FIXED value in the Arduino code is updated). Connect the middle node of the voltage divider to one of the Metro Mini's analog input pins. (Between A0 and A5; see Arduino code to see which ones are currently implemented.)

Our code's serial communication was tested with an Adafruit Metro Mini at 9600 baud rate. The Metro Mini sent data from 3 sensors (or potentiometers) to our computer through serial. The flex sensors used had a 50k resistance, so its preferable to use 50k potentiometers if not enough flex sensors are available. The relevant Arduino code can be found in pot_test.

## Running the Code
First, upload the Arduino sketch to your Metro Mini and connect it to your computer via USB. To run the Python code, first make sure your Metro Mini is outputing serial data at a 9600 baud rate. The data from the 3 sensors should be all transmitted in the same line/buffer, separated by spaces. Check which serial port your Metro Mini is connected to (COM ports for Windows  or /dev/tty port for Mac and Linux). Update the serial port definition depending on the port you are using. An example definition is shown below: 

    #Serial port definition. Change this line according to the port you are using for serial communication.
    #COM3 is the serial communication port in this example
    ser = serial.Serial('COM3', 9600);

Once the serial port is set, run full_audio_test.py and have fun playing with the sensors!

*Optional: Each sensor has a different range of values it can transmit as no two sensors are equal. You can edit the NORMALIZE_SENS list to match your specific sensor for better results.*

## Possible Modifications for More Fun
There are many possible extensions to build upon this project. Here are some ideas that we came up with:

-> More sensors and/or potentiometers can be added to have more variables available. The Metro Mini has 6 analog inputs, so up to 6 sensors could be read. Using a different microcontroller with more analog inputs would allow for even more sensor inputs. Each of these sensors could be used to add another frequency to the chord, or even be set to vary volume, pitch, or other aspects of the audio.

-> Our code currently generates an A major chord using a 440 Hz base frequency. Editing this frequency would allow other chords to be produced, so feel free to experiment with it!

-> The current audio stream plays sound for the set duration and then stops the stream. However, the PyAudio library allows for sound to be played continuosly while varying the stream in real time. This can be done by creating a callback function for the PyAudio object. This function gets called at the end of the set duration, and new audio data can be attached to the stream to continue playing sounds without stopping the stream, generating a continuous audio output. 

## Acknowledgments 
We want to thank Sam Redmond and the CS41 staff for all their help and support!




