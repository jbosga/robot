import serial
import time
import random
import re


class Controller(object):

    def __init__(self, serial_port):
        """Initializes the Controller object.

        :param serial_port: The port the Arduino is connected to. 
        :type serial_port: str
        """
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.min_safe_dist = 40
        self.steps_since_dist_check = 0

    def act(self, command, duration_s=None):
        """Passes commands to the Arduino microcontroller. It keeps retrying until the command
        is confirmed by the Arduino. Also allows for a command duration, useful for navigation commands.
        Valid commands:
            M0-9 - Move at speed 
            S0   - Stop
            L0-9 - Look around. Value is mapped to 180 degree FOV where 90 is forward facing. 0=0 degrees, 9=180 degrees.

        :param command: Valid command in the form of a capital character followed by a power parameter between 0 and 9. 
        :type command: str
        :param duration_s: Desired duration of the command in seconds, defaults to None
        :type duration_s: int, optional
        :return: 1 upon successful exection, or dist if a sonar measurement action was taken. 
        :rtype: float
        """
        command_given = False

        cmd = command + "\n"
        i = 0
        while not command_given:
            try:
                self.ser.flush()
                self.ser.write(cmd.encode('utf-8'))
                line = self.ser.readline().decode('utf-8').rstrip()
                # print(line)
                if line == f'Received: {command[0]}':
                    command_given = True
                    print(f"{command}: {i}")
            except UnicodeDecodeError as u:
                print(f"Error: {u}")
            i += 1
            # print(i)

        if duration_s:
            print(f"Sleeping for {duration_s} s")
            time.sleep(duration_s)

        if command == 'P':
            dist = self.read_sonar()
            return dist
        else:
            return 1

    def read_sonar(self):
        """Listens to Arduino serial output for sonar returns. 
        It collects 5 sonar pings before returning the average reported distance in centimeters.

        :return: Average distance in centimeters over 5 sonar measurements
        :rtype: float
        """
        received_ping = False
        pings = []
        dist_cm = -1
        i = 0
        while i < 5:
            while not received_ping:
                try:
                    self.ser.flush()
                    line = self.ser.readline().decode('utf-8').rstrip()
                    if re.match(r'^Ping: \d{1,3}$', line):
                        dist_cm = float(line.split(' ')[-1])
                        if dist_cm == 0:
                            dist_cm = 250
                        received_ping = True

                except UnicodeDecodeError:
                    dist_cm = None
            i += 1
            pings.append(dist_cm)
            received_ping = False
            dist_cm = None
        return sum(pings)/len(pings)

    def look_direction(self, degrees):
        pass

    def detect_target(target='potted-plant', img, detector):
        """Lets the robot look around and search for targets.

        :param target: should be from the same set of labels as the pretrained net, defaults to 'potted-plant'
        :type target: str
        :param img: image to use for detection
        :type img: array
        :param detector: object detection object
        :type detector: object
        :return: True or False depending on succesful target detection
        :rtype: bool
        """
        print("Looking around..")
        detections = detector.detect(img)
        print("Got readings..")
        print(detections)
        target_detected = False
        for detection in detections:
            if detection['label']==target:
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
            print("Nothing of interest found.")
            return False