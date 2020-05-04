import serial
import time
import random
import re

class Controller(object):

    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.min_safe_dist = 40
        self.steps_since_dist_check = 0

    def act(self, command, duration_s=None):
        """Passes commands to the Arduino microcontroller. It keeps retrying until the command
        is confirmed by the Arduino. Also allows for a command duration, useful for navigation commands."""
        command_given = False

        
        cmd = command + "\n"
        i = 0
        while not command_given:
            try:
                self.ser.flush()
                self.ser.write(cmd.encode('utf-8'))
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)
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


    def dist_check(self):
        # wiggle wiggle

        # move a little left
        # measure sonar
        # move a little right
        # measure sonar
        # sort of center
        # take in
        pass

    def read_sonar(self):
        """Listens to Arduino serial output for sonar returns. 
        It collects 5 sonar pings before returning the average reported distance in centimeters. """
        received_ping = False
        pings=[]
        dist_cm = -1
        i = 0
        while i<5:
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
            i +=1
            pings.append(dist_cm)
            received_ping = False
            dist_cm = None
        return sum(pings)/len(pings)


    def look_direction(self, degrees):
        pass


    def simple_navigation(self):
        while True:
            self.act('F', duration_s=2)

            self.act('S', duration_s=0.1)

            dist = self.act('P', duration_s=None)
            print(f"Ping: {dist} cm")
            if 0 < dist < self.min_safe_dist:
                self.act('L', duration_s=1)

