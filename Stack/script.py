from ppadb.client import Client
import time
from datetime import date, datetime

adb = Client(host='127.0.0.1', port=5037)

devices = adb.devices()

if len(devices) == 0:
    print("No Devices Attached")
    quit()

device = devices[0]

while True:
    device.shell("input tap 500 1000 80")
    time.sleep(0.6)
