class ExampleModule():
    def __init__(self, example_config=2):
        self.example_config = example_config

    def run(self, autopilot):
        if autopilot.current_clock > self.example_config:
            return True
        return False
