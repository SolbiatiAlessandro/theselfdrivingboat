from gpiozero import LED
import time

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

analog_input_channel = AnalogIn(mcp, MCP.P0)
voltage = analog_input_channel.voltage
print("BATTERY LEVEL BEFORE TEST: "+str(voltage))

right_motor = LED(17)
right_motor.on()
left_motor = LED(18)
left_motor.on()

print("STARTING TEST IN 3")
time.sleep(1)
print("STARTING TEST IN 2")
time.sleep(1)
print("STARTING TEST IN 1")
time.sleep(1)
"""
print("RIGHT MOTOR TEST START")
right_motor.off()
time.sleep(1)
right_motor.on()
time.sleep(1)
print("LEFT MOTOR TEST START")
left_motor.off()
time.sleep(1)
left_motor.on()

time.sleep(2)
"""
print("BOTH MOTORS TEST")
left_motor.off()
right_motor.off()
time.sleep(2)
left_motor.on()
right_motor.on()

analog_input_channel = AnalogIn(mcp, MCP.P0)
voltage = analog_input_channel.voltage
print("BATTERY LEVEL AFTER TEST: "+str(voltage))
