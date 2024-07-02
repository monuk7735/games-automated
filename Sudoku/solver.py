def isPossible(y, x, n, grid):
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

def solve(gr):
    # print("run")
    for x in range(9):
        for y in range(9):
            if gr[y][x] == 0:
                for n in range(1, 10):
                    if isPossible(y, x, n, gr) :
                        gr[y][x] = n
                        solve(gr)
                        gr[y][x] = 0
                return
    raise FileNotFoundError

def oneSolver(grid):
    try:
        print("Solving")
        solve(grid) 
    except FileNotFoundError:
        print("Solved")
        return grid
