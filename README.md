# cs41_jazzHands
CS41 Final Project
*Team: Meera Radhakrishnan, Andrea Ramirez*

## Introduction
Welcome to Jazz Hands! This project aimed to create sounds and visuals from data gathered from a glove with flex sensors. By using serial communcation, we transmitted values from the flex sensors (and some potentiometers) to our computer. The weights of different frequencies were adjusted depending on the sensors. These weights determined the audio output from our code, which played a C major chord and displayed the output audio waveform as well as the weights of the notes creating the chords. 

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
Our code's serial communication was tested with an Adafruit Metro Mini at 115200 baud rate. The Metro Mini sent data from 3 sensors (or potentiometers) to our computer through serial. The flex sensors used had a 50k resistance, so its preferrable to use 50k potentiometers if not enough flex sensors are available. 




This writeup should contain a technical overview of the project and the code therein. In effect, you're writing documentation for your project - if the first thing someone reads about your project is the README, what information does she need to know? We're asking you to also include a technical section in your README to describe the code design, the purpose of various modules, and any requirements (e.g. must run a certain version of Python, or must have a particular operating system, or must have a Postgres database running, or must have a Google account, or anything else).

In addition, we're asking you to write short installation/execution instructions. After we download your code, what steps do we have to perform to get it up and running? For many projects, the answer will just be "run the main python script named something.py," but several others will have more complex configuration. If we can't set up your project, we have no way to confirm that your project works, so we hope that your installation instructions are clear, correct, replicable, and concise.

Other general sections of a README usually include, but are not limited to: known bugs, contact information for the maintainer (that's you!), and credits/acknowledgements.

