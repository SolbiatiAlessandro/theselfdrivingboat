#python import
import os
from datetime import datetime

# hardware import
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# hardware setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# influxdb import
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class ADC():
    """anologue to digital converter (MCP3008)"""

    def __init__(self):
        self.token = os.environ['INFLUX_DB__TOKEN']
        self.org = os.environ['INFLUX_DB__ORG']
        self.bucket = os.environ['INFLUX_DB__BUCKET']
        self.client_url = os.environ['INFLUX_DB__CLIENT_URL']

        self.client = InfluxDBClient(
                url=self.client_url,
                token=self.token,
                org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def _read(self, pin, point, tag_field, tag_value, voltage_multiplier):
        """
        pin: MCP.P1
        point: "charge"
        tag_field: "battery"
        tag_value: "XYZ"
        voltage_multiplier: 2 (based on the hardware voltage divider on the PCB)
        """
        voltage = read_from_pin(pin)
        real_voltage = voltage * voltage_multiplier
        point = Point(point) \
          .tag(tag_field, tag_value) \
          .field("value", real_voltage)   \
          .time(datetime.utcnow(), WritePrecision.NS)

        self.write_api.write(self.bucket, self.org, point)

    def run(self, _):
        """reads voltage input from ADC"""
        self._read(MCP.P0, "energy", "device", "YF18650", 3)
        self._read(MCP.P1, "energy", "device", "SolarPanel1", 2)
        self._read(MCP.P2, "energy", "device", "SolarPanel2", 3)
        return False

def read_from_pin(pin, debug=False):
    analog_input_channel = AnalogIn(mcp, pin)
    voltage = analog_input_channel.voltage
    if debug: print(voltage)
    return voltage

if __name__ == "__main__":
    for p in [MCP.P0, MCP.P1, MCP.P2, MCP.P3, MCP.P4]:
        read_from_pin(p, debug=True)
