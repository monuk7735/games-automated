import numpy as np
import random

boardWidth = 5
boardHeight = 5

left = [[3], [3, 1], [2, 2], [1, 3], [1]]
top = [[3], [3, 1], [2, 2], [1, 3], [1]]

board = []

for i in range(boardHeight):
    temp = []
    for j in range(boardWidth):
        temp.append(0)
    board.append(temp)

def isValid(y, x):
    index = 0
    count = 0
    for i in range(y+1):
        if board[i][x] == 2 and count > 0:
            if count != top[x][index]:
                return False
            index += 1
            count = 0
        elif board[i][x] == 1:
            if index == len(top[x]):
                return False
            count += 1
        # elif board[i][x] == 0:
        #     return True
        # if index >= len(top[x]):
        #     return False
        if i == boardHeight - 1 and count > 0:
            if count != top[x][index]:
                return False
    index = 0
    count = 0
    for i in range(x+1):
        if board[y][i] == 2 and count > 0:
            if count != left[y][index]:
                return False
            index += 1
            count = 0
        elif board[y][i] == 1:
            if index == len(left[y]):
                return False
            count += 1
        # elif board[y][i] == 0:
        #     return True
        # if index >= len(left[y]):
        #     return False
        if i == boardWidth - 1 and count > 0:
            if count != left[y][index]:
                return False
    return True

def Solve():
    for y in range(boardHeight):
        for x in range(boardWidth):
            if board[y][x] == 0:
                for n in [2,1]:
                    board[y][x] = n
                    if isValid(y,x):
                        Solve()
                    board[y][x] = 0
                return

    print(np.matrix(board))
    input("More?")

Solve()

# print(np.matrix(board))