#!/usr/bin/env python3
# source ./venv_robot/bin/activate     to activate venv
import serial
import time
import cv2 as cv

# from src.pi.object_detector import ObjectDetector
from src.pi.controller import Controller

# cap = cv.VideoCapture(0)

# detector = ObjectDetector(conf_thresh=0.3)
# RPI Serial port: '/dev/ttyACM0'
# Windows Serial Port: 'COM3'
controller = Controller(serial_port='COM3')

moves = ['F', 'S', 'P', 'F', 'S', 'P']

if __name__ == '__main__':

    controller.simple_navigation()
    
