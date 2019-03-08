import serial

ser = serial.Serial('/dev/ttyS3',9600)
print("Program started")
nums = []
for i in range(100):
    num_str = ser.readline()
    #nums.append(num_str)
    print(num_str.decode().strip('\n'))

print(nums)



