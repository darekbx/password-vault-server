import serial
import time

s = serial.Serial('/dev/ttyS0',
	baudrate=9600, timeout=2)

while True:
	line = s.readline()
	print(line)
	time.sleep(1)
