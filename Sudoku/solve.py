from utils import * 

def solve(puzzle):
    for itrations in range(0, 3):
        zones = extract_zones(puzzle)
        for zone in zones:
            if zone["type"] == "row":
                row = zone["coord"]
                for col in range(0, 9):
                    insert_possibilities(puzzle, row, col)
            elif zone["type"] == "col":
                col = zone["coord"]
                for row in range(0, 9):
                    insert_possibilities(puzzle, row, col)
            else:
                row_begin = zone["coord"][0]
                row_end = zone["coord"][1]
                col_begin = zone["coord"][2]
                col_end = zone["coord"][3]
                for row in range(row_begin, row_end+1):
                    for col in range(col_begin, col_end+1):
                        insert_possibilities(puzzle, row, col)
    print(puzzle)
    return puzzle