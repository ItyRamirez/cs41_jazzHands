import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Max values expected to come from each sensor
NORMALIZE_SENS = [450, 800, 1600]

# Adjust sounds as a factor of the base note. 440Hz is A.
BASE_FREQUENCY = 440.0

# Ratio of major 3rd frequency to base note
M3_RATIO = (81.0 / 64.0)

# Ratio of perfect 5th frequency to base note
P5_RATIO = (3.0 / 2.0)

# Baud rate that the Arduino is using to transmit measurements to the computer
BAUD_RATE = 9600

# CHANGE THIS; DEPENDS ON COMPUTER
# Serial port on your computer that the Arduino is communicating to.
SERIAL_PORT = 'COM3'

print("Program started.")

# Set up serial input from Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Set up pyaudio
p = pyaudio.PyAudio()
volume = 0.5    # range [0.0, 1.0]
fs = 44100      # sampling rate, Hz, must be integer
duration = 2.0  # in seconds, may be float
f = BASE_FREQUENCY      # sine frequency, Hz, may be float
stream = p.open(format=pyaudio.paFloat32,  # for paFloat32 sample values must be in range [-1.0, 1.0]
                channels=1,
                rate=fs,
                output=True)

# Initial sine wave to plot in time domain visualization
x = np.linspace(0, duration, fs * duration)
y = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

# Set up visualization
plt.ion()  # turn on interactive mode so functions draw immediately to screen
fig = plt.figure()  # create the figure to plot to

# Set up time domain visualization (sum of sines)
ax = fig.add_subplot(2, 1, 1)
line1, = ax.plot(x, y, 'r-')
ax.set_xlim(0, (1.0 / BASE_FREQUENCY))
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Sound Waveform")

# Set up frequency domain visualization (bar chart of frequency weights)
ax2 = fig.add_subplot(2, 1, 2)
frequency_labels = ["A", "C#", "E"]
y_pos = np.arange(len(frequency_labels))
frequency_weights = [1, 1, 1]  # Starting frequency weights
ax2 = plt.bar(y_pos, frequency_weights, align='center', alpha=0.5)
plt.xticks(y_pos, frequency_labels)
plt.ylabel("Amplitude")
plt.title("Frequency Components")
ax.set_ylim(ymin=-2.5, ymax=2.5)

# Set frequency bins
chord_frequencies = [
    BASE_FREQUENCY,
    M3_RATIO *
    BASE_FREQUENCY,
    P5_RATIO *
    BASE_FREQUENCY]


def process_serial(ser):
    """
    Collects serial input and processes it. Returns flex sensor measurements as an array.

    ser: PySerial object
    """

    # Reads in the resistance values as a string from the serial input
    meas_str = ser.readline()

    # Parses the values into a list of numbers
    meas_str_list = meas_str.decode().strip('\n').split(" ")

    # Convert the strings into ints
    meas_raw = np.array(list(map(lambda x: int(x), meas_str_list)))

    return meas_raw


def normalize_and_clip(meas):
    """
    Clips flex sensor measurements to a maximum value to avoid buzzing.
    Normalizes sensor values to weight each frequency component.

    meas: An array containing the raw frequency measurements
    """
    frequency_weights = np.zeros(len(meas))

    for i in range(len(meas)):
        if(meas[i] > NORMALIZE_SENS[i]):
            meas[i] = NORMALIZE_SENS[i]
        frequency_weights[i] = meas[i] / NORMALIZE_SENS[i]

    return frequency_weights


def generate_sound_samples(chord_frequencies, frequency_weights):
    """
    Generate sound samples by summing up the sine waves for each frequency

    chord_frequencies: Frequencies to generate sine waves for
    frequency_weights: Weights for each of the chord frequencies
    """
    samples = 0
    for i in range(len(frequency_weights)):
        samples = samples + (frequency_weights[i]) * (np.sin(2 * np.pi * np.arange(
            fs * duration) * chord_frequencies[i] / fs)).astype(np.float32)
    return samples


def update_plots(plt, ax, ax2, frequency_weights, chord_frequencies, samples):
    """
    Updates plot data with the latest measurements.

    plt: pyplot object
    ax: Axes object for time domain plot
    ax2: Axes object for frequency domain plot
    frequency_weights: Weights to plot in frequency domain plot
    chord_frequencies: Frequencies to be displayed on time domain plot
    samples: Sound samples for time domain plot
    """

    # Update the frequency domain bar chart with new frequency weights
    plt.subplot(2, 1, 2)
    for i in range(3):
        ax2.patches[i].set_height(frequency_weights[i])

    # Dynamically rescale the x axis of time domain plot to appropriately fit the visualization
    # Useful if you want to dynamically change chord frequencies with a new
    # potentiometer
    xmin, xmax = ax.get_xlim()
    smallest_frequency = min(chord_frequencies)
    longest_period = 1.0 / smallest_frequency
    ax.set_xlim(xmax=(100 * longest_period))

    # Update the time domain waveform with new measurements
    line1.set_ydata(samples)


while(True):

    # Process measurements from flex sensors
    meas_raw = process_serial(ser)

    # Normalize and clip measurements from flex sensors to get frequency
    # weights
    frequency_weights = normalize_and_clip(meas_raw)

    # Generate summed sine waves
    samples = generate_sound_samples(chord_frequencies, frequency_weights)

    # Play sound samples
    stream.write(volume * samples)

    # Update plot data
    update_plots(plt, ax, ax2, frequency_weights, chord_frequencies, samples)

    # Update plot visualizations
    fig.canvas.draw()
    fig.canvas.flush_events()

stream.stop_stream()
stream.close()
p.terminate()
