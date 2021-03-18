import time
import os

class Camera():

    def __init__(self):
        pass

    def run(self, autopilot):
        """commands in the form CAMERA"""
        command = autopilot.request_text
        if 'CAMERA' not in command:
            return False

        pic_name = time.ctime().replace(' ', '_')
        os.system('raspistill -o ./imgs/{}'.format(pic_name))

        #TODO: send post to heroku

        return True
