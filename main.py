#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time
import cv2 as cv

# from src.pi.object_detector import ObjectDetector
from src.pi.controller import Controller

# cap = cv.VideoCapture(0)

# detector = ObjectDetector(conf_thresh=0.3)
controller = Controller(serial_port='/dev/ttyACM0')

moves = [ 'F', 'R', 'B', 'L', 'S', 'F', 'R', 'B', 'L', 'S']

if __name__ == '__main__':


    for move in moves:
        print(move)
        controller.move(move)

    # i =0
    # while True:
    #     # ret, img = cap.read()
    #     # print(f'Loop {i}')
    #     i += 1
    #     # detections = detector.detect(img)
    #     # controller.move('F')
    #     controller.move('F')
    #     print(i)
    #     # print(controller.read_sonar())
    #     # time.sleep(0.02)
        
    #     # for detection in detections:
    #     #     print(detection['label'])

    #     # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #     # ser.flush()
    #     # for move in moves:
    #     #     ser.flush()
    #     #     move_cmd = move + "\n"
    #     #     ser.write(move_cmd.encode('utf-8'))
    #     #     line = ser.readline().decode('utf-8').rstrip()
    #     #     print(line)
    #     #     time.sleep(3)
