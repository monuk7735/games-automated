from ppadb.client import Client
from PIL import Image
import pytesseract as pyts
import numpy as np
import cv2
import solver
import random
import sys

# boardSize = int(sys.argv[1])
boardSize = int(input("Board Size: "))

adb = Client(host='127.0.0.1', port=5037)

devices = adb.devices()

if len(devices) == 0:
    print("No Devices Attached")
    quit()

device = devices[0]

image = device.screencap()

with open("screen_cap.png", 'wb') as f:
    f.write(image)

image = cv2.imread("screen_cap.png", cv2.IMREAD_GRAYSCALE)

image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# img = image.crop((20, 330, 1060, 1413))

data_up = image[440:630, 194:1063]
data_left = image[639:1508, 10:185]

# cv2.imshow("upp", image)
# cv2.imshow("up", data_up)
# cv2.imshow("left", data_left)
# cv2.waitKey(0)

custom_config = r'--oem 3 --psm 6 outputbase digits'

topData = []

cv2.imwrite("temp.png", data_up)

for i in range(boardSize):
    temp = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)

    imgpart = cv2.rectangle(temp, (0,0), ( int(i * len(data_up[0])/boardSize), len(data_up)), (255, 255, 255), -1)
    imgpart = cv2.rectangle(imgpart, (int((i+1) * len(data_up[0])/boardSize),0), ( len(data_up[0]), len(data_up)), (255, 255, 255), -1)
    cv2.imwrite("temp1.png", imgpart)

    basewidth = 1200
    img = Image.open("temp1.png")
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.LANCZOS)
    # img.show()

    text = pyts.image_to_string(img, lang="eng", config=custom_config)
    text = [int(char) for char in text.splitlines()]
    topData.append(text)

leftData = []

cv2.imwrite("temp.png", data_left)

for i in range(boardSize):
    temp = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
    imgpart = temp[int(i*len(data_left)/boardSize):int((i+1) * len(data_left)/boardSize), 0:len(temp[0])]
    # imgpart = cv2.rectangle(temp, (0,0), ( len(data_left[0]), int(i*len(data_left)/boardSize)), (255, 255, 255), -1)
    # imgpart = cv2.rectangle(imgpart, (0, int((i+1) * len(data_left)/boardSize)), ( len(data_left[0]), len(data_left)), (255, 255, 255), -1)
    cv2.imwrite("temp1.png", imgpart)

    basewidth = 250
    img = Image.open("temp1.png")
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.LANCZOS)
    # img.save("temp2.png")
    text = pyts.image_to_boxes(img, lang="eng", config=custom_config)
    ans = []

    lines = text.splitlines()

    for line in lines:
        data = line.split(" ")
        # print(data)
        ans.append(data[:2])
    # print(ans)
    if len(ans) > 1:
        j = 0
        while j < (len(ans) - 1):
            diff = int(ans[j+1][1]) - int(ans[j][1])
            if diff <= 30:
                ans[j][0] += ans[j+1][0]
                ans[j][1] = ans[j+1][1]
                ans.remove(ans[j+1])
                j -= 1
            j += 1
    # print(ans)
    # text = text.split("")
    text = [int(char[0]) for char in ans]
    leftData.append(text)

# print(leftData)

# leftData = [[1], [2], [5], [14], [11, 1], [2, 7, 2], [5, 3, 3], [7, 4], [9, 4], [12], [10], [7], [4], [1], [1]]

print(topData)
print(leftData)


allSolutions = solver.solve([leftData, topData])

x1, y1 = 190, 640
x2, y2 = 1061, 1509

verList = [h for h in range(len(leftData))]
horList = [h for h in range(len(topData))]
random.shuffle(verList)
random.shuffle(horList)

allList = []

for i in verList:
    for j in horList:
        allList.append([i,j])

random.shuffle(allList)


for solution in allSolutions:
    print(np.matrix(solution))
    for k, (i, j) in enumerate(allList) :
        if(solution[i][j] == "#"):
            inp = "input tap " + str(int( x1 + j * (x2-x1)/boardSize + (x2-x1)/(2*boardSize))) + " " + str(int( y1 + i * (y2-y1)/boardSize + (y2-y1)/(2*boardSize)))
            # print(inp)
            device.shell(inp)
        print( "  " + str(int(k*100/len(allList))),"% Complete    \r", end="")
    break
