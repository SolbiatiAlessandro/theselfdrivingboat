from gpiozero import LED
import logging
import time

class MotorsRelay():

    def __init__(self):
        """on and off switched"""
        self.right_motor = LED(17)
        self.right_motor.on()
        self.left_motor = LED(18)
        self.left_motor.on()

    def run(self, autopilot):
        """commands in the form FORWARD"""
        command = autopilot.received_command
        if command == '' or command is None: 
            return False
        logging.warning('RECEIVED COMMAND {}'.format(command))

        if 'STOP' in command:
            self.right_motor.on()
            self.left_motor.on()
        if 'LEFT' in command:
            self.right_motor.off()
            self.left_motor.on()
        if 'RIGHT' in command:
            self.right_motor.on()
            self.left_motor.off()
        if 'FORWARD' in command:
            self.right_motor.off()
            self.left_motor.off()

        try:
            received_length = autopilot.request.json()['length']
        except KeyError:
            received_length = None
        length = received_length if received_length else 2
        time.sleep(int(length))
        return True
