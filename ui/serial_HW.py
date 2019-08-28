import serial
import time

s = serial.Serial('/dev/ttyS0',
	baudrate=9600,
	bytesize = serial.EIGHTBITS,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	timeout = 0.5)

while True:
	line = s.readline()
	print(line)
