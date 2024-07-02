import numpy as np

grid = [
[0,0,7,0,4,2,0,0,9],
[2,4,3,0,0,9,0,0,0],
[0,9,8,3,0,0,0,5,0],
[0,0,4,0,5,0,6,0,0],
[0,0,0,0,3,1,0,0,0],
[0,0,0,0,2,6,5,0,0],
[0,0,0,0,7,0,0,0,0],
[8,3,0,6,0,0,7,0,1],
[4,7,5,0,0,3,9,0,0]]

def isPossible(y, x, n):
    for i in range( 9):
        if grid[y][i] == n:
            return False
    for j in range(9):
        if grid[j][x] == n:
            return False
    x0 = (x//3) * 3
    y0 = (y//3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True

def solve():
    for x in range(9):
        for y in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if isPossible(y, x, n) :
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print(np.matrix(grid))
    input("More?")

solve()