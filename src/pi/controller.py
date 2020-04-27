import serial
import time
import random
import re

class Controller(object):

    def __init__(self, serial_port):
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.valid_moves = [ 'F', 'B', 'R', 'L', 'S']
        self.min_safe_dist = 40
        self.steps_since_dist_check = 0

    def move(self, direction):
        if direction in self.valid_moves:
            if direction == 'F':
                dist_to_obj = self.read_sonar()
                if 0 < dist_to_obj < self.min_safe_dist:
                    direction = random.choice(['B', 'R', 'L'])

            self.ser.flush()
            move_cmd = direction + "\n"
            self.ser.write(move_cmd.encode('utf-8'))
            line = self.ser.readline().decode('utf-8').rstrip()
            print(f"Serial feedback: {line}")
            self.steps_since_dist_check += 1
            return 1
        else:
            return 0


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
        received_ping = False
        pings=[]
        dist_cm = -1
        i = 0
        while i<5:
            while not received_ping:
                try:
                    self.ser.flush()
                    line = self.ser.readline().decode('utf-8').rstrip()
                    if re.match('^Ping: \d{1,3}$', line):
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
