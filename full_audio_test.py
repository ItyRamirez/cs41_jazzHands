import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

#Max values expected to come from each sensor
NORMALIZE_SENS = [10000, 700, 10000]

#Adjust sounds as a factor of the base note A
BASE_FREQUENCY = 440.0 

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
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-')
ax.set_xlim(0,(1.0/BASE_FREQUENCY))

while(True):
    #Reads in the resistance values as a string from the serial input
    nums_str = ser.readline()
    #nums_str_stripped = nums_str.decode().strip('\n') 

    #Parses the values into a list of numbers
    nums_str_list = nums_str.decode().strip('\n').split(" ") 
    print(nums_str_list)
    
    #The first input sets the fundamental frequency.
    #The second input sets the weight of the even harmonics.
    #The third input sets the weight of the odd harmonics.
    #Subsequent inputs can be used for other things like volume or envelope

    #TODO either do all numpy arrays or all lists
    frequency_weights = []
    frequency_weights.append(int(nums_str_list[0])/NORMALIZE_SENS[0])
    frequency_weights.append(int(nums_str_list[1])/NORMALIZE_SENS[1])
    frequency_weights.append(int(nums_str_list[2])/NORMALIZE_SENS[2])
    #for i in range(len(nums_str_list)): #TODO replace with something more Pythonic
    #   frequency_weights.append()

    f = [0, 0, 0]
    f[0] = BASE_FREQUENCY #* frequency_weights[0] #600 * int(nums_str_list[1])/318
    f[1] = 554.37 #2 * BASE_FREQUENCY #* frequency_weights[1]#440 * int(nums_str_list[2])/600
    f[2] = 659.25#3 * BASE_FREQUENCY #* frequency_weights[2]

    # generate samples 
    samples = 0
    for i in range(len(frequency_weights)):
        samples = samples + (frequency_weights[i])*(np.sin(2*np.pi*np.arange(fs*duration)*f[i]/fs)).astype(np.float32)
    
    stream.write(volume*samples)


    xmin,xmax = plt.xlim()
    smallest_frequency = min(f)
    longest_period = 1.0/smallest_frequency
    plt.xlim(xmax = (3 * longest_period))


    line1.set_ydata(samples)
    fig.canvas.draw()
    fig.canvas.flush_events()
 
    #f_set = 0
    #if(f < f2)

stream.stop_stream()
stream.close()

p.terminate()


