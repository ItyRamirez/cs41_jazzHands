import serial

ser = serial.Serial('COM3',9600) #/dev/ttyS3
print("Program started")
while(True):
    nums_str = ser.readline()
    nums_str_stripped = nums_str.decode().strip('\n')
    print(nums_str_stripped)
    #nums.append(num_str.decode().strip('\n'))




