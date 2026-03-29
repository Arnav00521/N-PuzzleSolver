# heuristics.py

from utils import GOAL_STATE, GRID_SIZE

def h1_misplaced_tiles(state):
    return sum(1 for i in range(8) if state[i] != GOAL_STATE[i] and state[i] != 0)

def h2_manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] == 0: continue
        curr_row, curr_col = divmod(i, GRID_SIZE)
        goal_row, goal_col = divmod(state[i] - 1, GRID_SIZE)
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def h3_linear_conflict(state):
    conflict_count = 0
    
    # 1. Check Rows for conflicts
    for row in range(3):
        row_tiles = [state[row*3 + col] for col in range(3)]
        for i in range(3):
            for j in range(i + 1, 3):
                t1, t2 = row_tiles[i], row_tiles[j]
                if t1 != 0 and t2 != 0:
                    # Are they both supposed to be in this specific row?
                    if (t1 - 1) // 3 == row and (t2 - 1) // 3 == row:
                        # Are they in the wrong order?
                        if t1 > t2:
                            conflict_count += 1

    # 2. Check Columns for conflicts
    for col in range(3):
        col_tiles = [state[row*3 + col] for row in range(3)]
        for i in range(3):
            for j in range(i + 1, 3):
                t1, t2 = col_tiles[i], col_tiles[j]
                if t1 != 0 and t2 != 0:
                    # Are they both supposed to be in this specific column?
                    if (t1 - 1) % 3 == col and (t2 - 1) % 3 == col:
                        # Are they in the wrong order?
                        if t1 > t2:
                            conflict_count += 1

    # Total = Base Manhattan + (2 * Number of conflicts)
    return h2_manhattan_distance(state) + (2 * conflict_count)