import numpy as np

top = [[1], [4], [2, 2], [5], [5]]
left = [[3], [4], [1, 2], [5], [4]]

size = 5

table = []
for i in range(size):
    temp = []
    for j in range(size):
        temp.append(0)
    table.append(temp)

print(np.matrix(table))

def check():
    for i in len(table):
        row = table[i]
        if row[0] == 0:
            counting = False
        else:
            counting = True
            

def solve():
    pass
