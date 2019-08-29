import serial
import time

s = serial.Serial('/dev/serial0',
	baudrate=9600,
	bytesize = serial.EIGHTBITS,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	timeout = 2)

while True:
	line = s.readline()
	print(line)
	time.sleep(1)
