#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time
import cv2 as cv

from src.pi.object_detector import ObjectDetector
from src.pi.controller import Controller

cap = cv.VideoCapture(0) # index 2 for linux, index 0 for Pi

detector = ObjectDetector(conf_thresh=0.5)
# Linux Serial port: '/dev/ttyACM0'
# Windows Serial Port: 'COM3'
controller = Controller(serial_port='/dev/ttyACM0')


if __name__ == '__main__':
    while True:
        
        # Simple loop that lets the robot drive around looking for potted plants
        controller.act('L5', duration_s=0.5) # Center camera
        controller.act('M9', duration_s=5) # Move at 60% speed
        controller.act('S0') # Stop
        retval, img = cap.read()
        detected = controller.detect_target('potted-plant', img, detector)

        controller.act('L3', duration_s=2) # Look around
        retval, img = cap.read()
        detected = controller.detect_target('potted-plant', img, detector)

        controller.act('S0') # Stop
        controller.act('L7', duration_s=2)
        retval, img = cap.read()
        detected = controller.detect_target('potted-plant', img, detector)

        controller.act('S0') # Stop

