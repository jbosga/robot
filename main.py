#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time

moves = [ 'F', 'F', 'B', 'R', 'L', 'S']

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    for move in moves:
        ser.flush()
        move_cmd = move + "\n"
        ser.write(move_cmd.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(3)
