from gpiozero import LED
import time

class MotorsRelay():

    def __init__(self):
        """on and off switched"""
        right_motor = LED(17)
        right_motor.on()
        left_motor = LED(18)
        left_motor.on()

    def run(self, autopilot):
        """commands in the form FORWARD or FORWARD-3"""
        command = autopilot.request_text
        if command == '':
            return False

        if 'STOP' in command:
            right_motor.on()
            left_motor.on()
        if 'LEFT' in command:
            right_motor.off()
            left_motor.on()
        if 'RIGHT' in command:
            right_motor.on()
            left_motor.off()
        if 'FORWARD' in command:
            right_motor.off()
            left_motor.off()

        length = 2
        if len(command.split('-')) > 1:
            length = command.split('-')[1]
        time.sleep(int(length))
        return True
