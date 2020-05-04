#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time
import cv2 as cv

# from src.pi.object_detector import ObjectDetector
from src.pi.controller import Controller

cap = cv.VideoCapture(0)

detector = ObjectDetector(conf_thresh=0.3)
# Linux Serial port: '/dev/ttyACM0'
# Windows Serial Port: 'COM3'
controller = Controller(serial_port='/dev/ttyACM0')

moves = ['F', 'S', 'P', 'F', 'S', 'P']

if __name__ == '__main__':


    while True:
        controller.act('M6', duration_s=3) # Move at 60% speed
        controller.act('S') # Stop
        controller.act('L') # Look around

