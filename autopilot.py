#python imports
import sys
import traceback
import logging
import time
logging.basicConfig(filename="/home/pi/Desktop/self-driving-boat/autopilot.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())
import requests
import requests.exceptions

#theselfdrivingboat imports
import autopilot_modules.example
import autopilot_modules.ADC
import autopilot_modules.pijuice_module
import autopilot_modules.motors
import autopilot_modules.camera


class Autopilot():
    def __init__(self, active_clock=10, inactive_clock=60*30):
        """
        active_clock: (seconds) communication loop while receiving orders
        inactive_clock: (seconds) communication loop while not receiving orders
        """
        self.active_clock = active_clock
        self.inactive_clock = inactive_clock
        self.current_clock = active_clock
        self.current_clock_iteration = 0 
        with open('boat.secret', 'r') as f:
            self.boat_name = f.read()

        self.request_endpoint = 'https://theselfdrivingboat.herokuapp.com/read_last_command?boat_name={}'.format(self.boat_name)

        self.modules = []

    def _update_clock(self):
        """
        clocks goes incrementally from active to inactive to save energy
        """
        self.current_clock_iteration += 1
        if self.request_text != '':
            self.current_clock = self.active_clock
        else:
            self.current_clock = min(2 * self.current_clock, self.inactive_clock)
        logging.info("iteration: {}, clock: {}".format(
            self.current_clock_iteration, self.current_clock))

    def add_module(self, module_class):
        """
        functional modules to add/remove features from the autopilot

        modules will be called with a .run(Autopilot()) method
        and need to return True if there has been any input communication from the remote
        """
        try:
            self.modules.append(module_class())
            logging.info("{}: INITIALIZED".format(module_class))
        except Exception:
            logging.error("{}: INITIALIZATION FAILED".format(module_class))
            logging.error(traceback.format_exc())

    def run(self):
        while True:
            try:
                self.request = requests.get(self.request_endpoint)
                self.request_text = self.request.text
            except requests.exceptions.ConnectionError as e:
                logging.warning("NO CONNECTION TO ENDPOINT {}".format(self.request_endpoint))
                self.request_text = ''

            for module in self.modules:

                try:
                    module.run(self)
                    logging.info("{}: SUCCEED".format(module))
                except Exception:
                    logging.warning("{}: FAILS".format(module))
                    logging.warning(traceback.format_exc())
            self._update_clock()
            time.sleep(self.current_clock)

if __name__ == "__main__":
    pilot = Autopilot(active_clock=10, inactive_clock=120)
    #pilot.add_module(autopilot_modules.example.ExampleModule)
    pilot.add_module(autopilot_modules.ADC.ADC)
    pilot.add_module(autopilot_modules.pijuice_module.PiJuiceModule)
    pilot.add_module(autopilot_modules.motors.MotorsRelay)
    pilot.add_module(autopilot_modules.camera.Camera)
    pilot.run()
