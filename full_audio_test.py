import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

#Max values expected to come from each sensor
NORMALIZE_SENS = [450, 800, 1600]
#Adjust sounds as a factor of the base note. 440Hz is A.
BASE_FREQUENCY = 440.0
#Ratio of major 3rd frequency to base note
M3_RATIO = (81.0/64.0)
#Ratio of perfect 5th frequency to base note
P5_RATIO = (3.0/2.0)

print("Program started.")

#Set up serial input from Arduino
ser = serial.Serial('COM3',9600)

#Set up pyaudio
p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 2.0  # in seconds, may be float
f = BASE_FREQUENCY       # sine frequency, Hz, may be float
stream = p.open(format=pyaudio.paFloat32, # for paFloat32 sample values must be in range [-1.0, 1.0]
                channels=1,
                rate=fs,
                output=True)

#Initial sine wave to plot
y = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
x = np.linspace(0,duration,fs*duration)

#Set up visualization
plt.ion() #turn on interactive mode so functions draw immediately to screen
fig = plt.figure() #create the figure to plot to

#Set up time domain visualization (sum of sines)
ax = fig.add_subplot(2,1,1)
line1, = ax.plot(x, y, 'r-')
ax.set_xlim(0,(1.0/BASE_FREQUENCY))

#Set up frequency domain visualization (bar chart of frequency weights)
ax2 = fig.add_subplot(2,1,2)
frequency_bins = ["A","C#","E"]
y_pos = np.arange(len(frequency_bins))
frequency_weights = [0,0,0]
ax2 = plt.bar(y_pos,frequency_weights, align='center',alpha=0.5)
plt.xticks(y_pos,frequency_bins)
plt.ylabel("Amplitude")
plt.title("Frequency Components")
ax.set_ylim(ymin = -2.5,ymax = 2.5)

#Set frequency bins
chord_frequencies = [BASE_FREQUENCY, M3_RATIO * BASE_FREQUENCY, P5_RATIO * BASE_FREQUENCY]
#f[0] = BASE_FREQUENCY #* frequency_weights[0] #600 * int(nums_str_list[1])/318
#f[1] =  * BASE_FREQUENCY #Major third #554.37 #2 * BASE_FREQUENCY #* frequency_weights[1]#440 * int(nums_str_list[2])/600
#f[2] =  * BASE_FREQUENCY #659.25#3 * BASE_FREQUENCY #* frequency_weights[2]

while(True):

    #Reads in the resistance values as a string from the serial input
    nums_str = ser.readline()

    #Parses the values into a list of numbers
    nums_str_list = nums_str.decode().strip('\n').split(" ")

    #TODO either do all numpy arrays or all lists
    #TODO consolidate for loops
    frequency_weights = np.zeros(len(nums_str_list))
    nums = np.zeros(len(nums_str_list))

    #Convert the strings into ints - can we do this with map or something? TODO
    for i in range(len(nums_str_list)):
        nums[i] = int(nums_str_list[i])

    #Clip the values above a certain threshold to prevent buzzing
    #Normalize sensor values to weight each frequency component
    for i in range(len(nums)):
        if(nums[i] > NORMALIZE_SENS[i]):
            nums[i] = NORMALIZE_SENS[i]
        frequency_weights[i] = nums[i]/NORMALIZE_SENS[i]

    #frequency_weights.append(nums[0]/NORMALIZE_SENS[0])
    #frequency_weights.append(nums[1]/NORMALIZE_SENS[1])
    #frequency_weights.append(nums[2]/NORMALIZE_SENS[2])

    #Generate sound samples by summing up the sine waves for each frequency
    samples = 0
    for i in range(len(frequency_weights)):
        samples = samples + (frequency_weights[i])*(np.sin(2*np.pi*np.arange(fs*duration)*chord_frequencies[i]/fs)).astype(np.float32)

    stream.write(volume*samples)

    #Update the frequency domain bar chart with new frequency weights
    plt.subplot(2,1,2)
    for i in range(3):
        ax2.patches[i].set_height(frequency_weights[i])

    #Rescale the x axis of time domain plot to appropriately fit the visualization
    xmin,xmax = ax.get_xlim()
    smallest_frequency = min(f)
    longest_period = 1.0/smallest_frequency
    ax.set_xlim(xmax = (100* longest_period))

    #Update the time domain waveform
    line1.set_ydata(samples)

    fig.canvas.draw() #Update all the plots
    fig.canvas.flush_events()

stream.stop_stream()
stream.close()
p.terminate()
