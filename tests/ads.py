import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)  
ads = ADS.ADS1115(i2c)
ads.gain = 2/3

while True:
    chan = AnalogIn(ads, ADS.P0)  
    print(f"Raw ADC value: {chan.value}")
    print(f"Voltage: {chan.voltage} V")
    time.sleep(1)
