#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time
import cv2 as cv

from src.pi.object_detector import ObjectDetector
from src.pi.controller import Controller

cap = cv.VideoCapture(2) # index 2 for linux, index 0 for Pi

detector = ObjectDetector(conf_thresh=0.3)
# Linux Serial port: '/dev/ttyACM0'
# Windows Serial Port: 'COM3'
controller = Controller(serial_port='/dev/ttyACM0')


def detect_target(target, cap=cap, detector=detector):
            retval, img = cap.read()
            detections = detector.detect(img)
            target_detected = False
            for detection in detections:
                if detection['label']=='person':
                    target_detected = True
                    break
            if target_detected:
                print("Target detected!")
                for _ in range(3):
                    controller.act('L7', duration_s=0.5)
                    controller.act('L5', duration_s=0.5)
                controller.act('S0', duration_s=1)
                return True
            else:
                return False

if __name__ == '__main__':
    while True:
        
        controller.act('L5', duration_s=0.5) # Center camera
        controller.act('M9', duration_s=2) # Move at 60% speed
        controller.act('S0') # Stop
        detected = detect_target('person')
        if detected:
            print("Target detected!!")
            break
        controller.act('L3', duration_s=2) # Look around
        detected = detect_target('person')
        if detected:
            break
        controller.act('S0') # Stop
        controller.act('L7', duration_s=2)
        detected = detect_target('person')
        if detected:
            break
        controller.act('S0') # Stop
        controller.act('L5', duration_s=0.5) # Center camera
        controller.act('M9', duration_s=1) # Move at 60% speed
        controller.act('S0') # Stop`

