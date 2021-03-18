from gpiozero import LED
import time
import requests
from datetime import datetime

# hardware import
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

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

right_motor = LED(17)
right_motor.on()
left_motor = LED(18)
left_motor.on()

import logging
logging.basicConfig(filename="/home/pi/Desktop/self-driving-boat/selfdriving.logs",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
logging.info('starting new session')
logging.info(datetime.utcnow())

try:
    cnt=0
    while True:
        try: 
            r=requests.get('https://theselfdrivingboat.herokuapp.com/state')
            print(r.text)
            if r.text == 'STOP':
                right_motor.on()
                left_motor.on()
            if r.text == 'LEFT':
                right_motor.off()
                left_motor.on()
            if r.text == 'RIGHT':
                right_motor.on()
                left_motor.off()
            if r.text == 'FORWARD':
                right_motor.off()
                left_motor.off()
            time.sleep(3)
            right_motor.on()
            left_motor.on()
            time.sleep(3)
        except Exception as e:
            logging.error('ERROR A')
            logging.error(e)
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
            log = "Read voltage {}: {} V".format(MCP.P0, voltage)
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
            log = "Read voltage {}: {} V".format(MCP.P1, voltage)
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
            log = "Read voltage {}: {} V".format(MCP.P2, voltage)
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
        try:
            requests.post('https://theselfdrivingboat.herokuapp.com/ping', {'source':'1kgboat'.format(cnt)})
            cnt+=1
        except Exception as e:
            logging.error('ERROR C')
            logging.error(e)

except Exception as e:
    logging.error('ERROR B')
    logging.error(e)


