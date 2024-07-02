from ppadb.client import Client
from PIL import Image
import time

adb = Client(host='127.0.0.1', port=5037)

devices = adb.devices()

if len(devices) == 0:
    print("No Devices Attached")
    quit()

device = devices[0]

while True:

    image = device.screencap()

    with open("screen_cap.png", "wb") as f:
        f.write(image)

    image = Image.open("screen_cap.png").convert("L")
    data = image.load()
    coordinates:list = []

    black_found = False

    for i in range(image.size[0]):
        pixel = data[i, 2000]

        if pixel == 0:
            if not black_found:
                coordinates.append(i)
                black_found = True
        else:
            if black_found:
                coordinates.append(i)
                black_found = False

    # print(coordinates)

    start, targetStart, targetEnd = coordinates[1:4]

    print(start, targetStart, targetEnd)

    gap = targetStart - start
    distance = gap + int(((targetEnd - targetStart)/2)*.98)

    device.shell("input touchscreen swipe 500 500 500 500 " + str(distance))
    time.sleep(3)