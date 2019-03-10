import serial
import pyaudio
import numpy as np


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.1   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float



# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 


ser = serial.Serial('COM3',9600) #/dev/ttyS3
print("Program started")
while(True):
    nums_str = ser.readline()
    nums_str_stripped = nums_str.decode().strip('\n')
    print(nums_str_stripped)
    nums_str_list = nums_str_stripped.split(" ")
    # generate samples, note conversion to float32 array
    f = 600 * int(nums_str_list[1])/318
    f2 = 440 * int(nums_str_list[2])/600
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32) + (np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)).astype(np.float32)
    stream.write(volume*samples)
    #nums.append(num_str.decode().strip('\n'))

stream.stop_stream()
stream.close()

p.terminate()


