#python import
import os
from datetime import datetime

# pijuice import
try:
    from autopilot_modules.pijuice import PiJuice
except ModuleNotFoundError:
    from pijuice import PiJuice

pijuice = PiJuice(1, 0x14)

# influxdb import
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class PiJuiceModule():
    """pijuice APIs"""

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

    def run(self, _):
            
        pijuice_status = pijuice.status.GetStatus()['data']
        pijuice_charge = pijuice.status.GetChargeLevel()['data']
        pijuice_voltage = pijuice.status.GetIoVoltage()['data']
        pijuice_current = pijuice.status.GetIoCurrent()['data']
        pijuice_wakeup = pijuice.power.GetWakeUpOnCharge()['data']
        point = Point("energy") \
          .tag("device", "PiJuice_BP7X_3.7VDC_1820mAh") \
          .field("isFault", pijuice_status['isFault'])   \
          .field("isButton", pijuice_status['isButton'])   \
          .field("battery", pijuice_status['battery'])   \
          .field("powerInput", pijuice_status['powerInput'])   \
          .field("powerInput5vIo", pijuice_status['powerInput5vIo'])   \
          .field("charge", pijuice_charge)   \
          .field("voltage", pijuice_voltage)   \
          .field("current", pijuice_current)   \
          .field("wakeup", pijuice_wakeup)   \
          .time(datetime.utcnow(), WritePrecision.NS)

        self.write_api.write(self.bucket, self.org, point)


if __name__ == "__main__":
    pijuice_data = pijuice.status.GetStatus()
    pijuice_status = pijuice_data['data'] 
    print(pijuice_status)
    print(pijuice.status.GetChargeLevel())
    print(pijuice.status.GetIoVoltage())
    print(pijuice.status.GetIoCurrent())
