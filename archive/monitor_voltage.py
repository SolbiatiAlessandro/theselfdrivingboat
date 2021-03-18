"""
script to monitor voltage, sends to influxDB APIs
"""
from datetime import datetime
import time
import logging

# hardware import
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from gpiozero import LED
booster_adc = LED(26)
booster_adc.on()


# pijuice import
from pijuice import PiJuice
pijuice = PiJuice(1, 0x14)

# influxdb import
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# hardware setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# influx db setup
token = "L8LEe0QrLQysteAE6-cLLEy8ezz-gOJdO-eRpZ4ugRJdpgNsFy66P0BXlziYjqtRabn-R-4lNsemAatT8xPkqg=="
org = "alessandro.solbiati@gmail.com"
bucket = "alessandro.solbiati's Bucket"
client = InfluxDBClient(url="https://westeurope-1.azure.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)
SAMPLING_TIME = 3


def main():
    while True:
        try:
            #PIJUICE STATUS
            pijuice_data = pijuice.status.GetStatus()
            pijuice_status = pijuice_data['data'] 
            log = "Read pijuice status: {}%".format(pijuice_status['battery'])
            logging.info(log)
            print(log)
            point = Point("charge") \
              .tag("battery", "PiJuice_BP7X_3.7VDC_1820mAh") \
              .field("isFault", pijuice_status['isFault'])   \
              .field("isButton", pijuice_status['isButton'])   \
              .field("battery", pijuice_status['battery'])   \
              .field("powerInput", pijuice_status['powerInput'])   \
              .field("powerInput5vIo", pijuice_status['powerInput5vIo'])   \
              .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            logging.info("Sent to API")

            # PIJUICE CHARGE
            pijuice_data = pijuice.status.GetChargeLevel()
            pijuice_charge = pijuice_data['data'] 
            log = "Read pijuice charge: {}%".format(pijuice_charge)
            logging.info(log)
            print(log)
            point = Point("charge") \
              .tag("battery", "PiJuice_BP7X_3.7VDC_1820mAh") \
              .field("value", pijuice_charge)   \
              .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            logging.info("Sent to API")


            # MOTOR BATTERY
            # for p in [MCP.P0,MCP.P1,MCP.P2,MCP.P3,MCP.P4,MCP.P5,MCP.P6,MCP.P7]:
            analog_input_channel = AnalogIn(mcp, MCP.P0)
            #print('Raw Voltage', channel.value)
            voltage = analog_input_channel.voltage
            log = "real voltage {}: {} V".format(MCP.P0, voltage * 3)
            logging.info(log)
            print(log)
            point = Point("charge") \
              .tag("battery", "YF18650_7.4V_5200mAh") \
              .field("value", voltage)   \
              .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            logging.info("Sent to API")

            # SOLAR PANELS
            analog_input_channel = AnalogIn(mcp, MCP.P1)
            voltage = analog_input_channel.voltage
            log = "real voltage {}: {} V".format(MCP.P1, voltage * 2)
            logging.info(log)
            print(log)
            point = Point("charge") \
              .tag("battery", "solar panels") \
              .field("value", voltage)   \
              .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            logging.info("Sent to API")

            # SOLAR PANELS
            analog_input_channel = AnalogIn(mcp, MCP.P2)
            voltage = analog_input_channel.voltage
            log = "real voltage {}: {} V".format(MCP.P2, voltage * 3)
            logging.info(log)
            print(log)
            point = Point("charge") \
              .tag("battery", "booster") \
              .field("value", voltage)   \
              .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            logging.info("Sent to API")


        except Exception as e:
            print("NOT LOGGING")
            print(e)
            logging.critical("NOT LOGGING")
            logging.critical(e)
        time.sleep(SAMPLING_TIME)

if __name__ == "__main__":
    logging.basicConfig(filename='monitor_voltage.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.getLogger().setLevel(logging.INFO)
    try:
        main()
    except Exception as e:
        logging.critical("main() exited")
        logging.critical(e)
