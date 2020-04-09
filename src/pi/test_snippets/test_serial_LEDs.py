#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
	ser = serial.Serial('COM3', 9600, timeout=1)
	ser.flush()
	while True:
		ser.flush()
		ser.write(b"F\n")
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		time.sleep(1)