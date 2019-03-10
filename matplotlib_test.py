import matplotlib.pyplot as plt
import numpy as np

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.5   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

y = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
x = np.linspace(0,duration,fs*duration) #plot one period to start

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-')

ax.set_xlim(0,(1.0/f))
for i in range(200):
    xmin,xmax = plt.xlim()
    f = 440*((i+1)/100)
    T = 1.0/f

    #If there are more than 4 periods in the window, halve window size
    #If there are less than 1 period in the window, double window size

    if(xmax/T > 4):
        plt.xlim(xmax=(xmax/2))
    elif((xmax/T) < 1):
        plt.xlim(xmax=(2*xmax))

    line1.set_ydata((np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32))
    fig.canvas.draw()
    fig.canvas.flush_events()

