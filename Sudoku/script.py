from ppadb.client import Client
from PIL import Image
import pytesseract as trt
import copy
import cv2
import solver

adb = Client(host='127.0.0.1', port=5037)

devices = adb.devices()


if len(devices) == 0:
    print("No Devices Attached")
    quit()

device = devices[0]

image = device.screencap()

with open(".screen_cap.png", 'wb') as f:
    f.write(image)

posButtons = [
    [185, 1815],
    [365, 1815],
    [540, 1815],
    [720, 1815],
    [893, 1815],
    [185, 2005],
    [365, 2005],
    [540, 2005],
    [720, 2005],
    [893, 2005]
]

image = cv2.imread(".screen_cap.png", cv2.IMREAD_GRAYSCALE)

# for i in range(len(image)):
#     for j in range(len(image[0])):
#         if image[i][j] == 0:
#             image[i][j] = 255

# image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
# image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# while True:
    # x = int(input("Press Number: "))

#     device.shell("input tap " + str(posButtons[x][0]) + " " + str(posButtons[x][1]))

# board = screen_cap.150, 205, 930, 985))
# print(image)
# board = image[205:984, 150:933] #My App
board = image[427:1498, 5:1075] 

cv2.imwrite(".board.png", board)

# cv2.imshow("im", board)

# cv2.waitKey(0)

w, h = len(board[0]), len(board)

custom_config = r'--oem 1 --psm 8 outputbase digits'


boardList=[]
for i in range(9):
    row = []
    for j in range(9):
        # img = board.crop((j * w/9, i * h/9, (j+1) * w/9, (i+1) * h/9))
        img = board[int(i*h/9)+10:int((i+1)*h/9)-10, int(j*w/9)+10:int((j+1)*w/9)-10]
        cv2.imwrite(".temp1.png", img)

        basewidth = 300
        img = Image.open(".temp1.png")
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.LANCZOS)
        text = trt.image_to_string(img, lang="eng", config=custom_config)
        # print(text.strip())
        if text.strip() not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            text = "0"
        row.append(int(text.strip()))
    print(row)
    boardList.append(row)

boardListOld = copy.deepcopy(boardList)
solution = solver.oneSolver(boardList)

print(boardListOld)
print(solution)

boardSize = 9
x1, y1, x2, y2 = 5, 427, 1075, 1497

for k in range(9):
    device.shell("input tap " + str(posButtons[k][0]) + " " + str(posButtons[k][1]))
    for i in range(len(boardList)):
        for j in range(len(boardList[0])):
            if boardList[i][j] == (k+1) and boardListOld[i][j] == 0:
                inp = "input tap " + str(int( x1 + j * (x2-x1)/boardSize + (x2-x1)/(2*boardSize))) + " " + str(int( y1 + i * (y2-y1)/boardSize + (y2-y1)/(2*boardSize)))
                device.shell(inp)
