# heuristics.py

def h1_misplaced_tiles(state):
    misplaced = 0
    # The goal state has tile 'val' at index 'val - 1'
    for i, val in enumerate(state):
        if val != 0 and val != i + 1:
            misplaced += 1
    return misplaced

def h2_manhattan_distance(state):
    N = int(len(state) ** 0.5)
    distance = 0
    for i, val in enumerate(state):
        if val != 0:
            # Where the tile SHOULD be
            target_r = (val - 1) // N
            target_c = (val - 1) % N
            # Where the tile IS currently
            current_r = i // N
            current_c = i % N
            
            distance += abs(target_r - current_r) + abs(target_c - current_c)
    return distance

def h3_linear_conflict(state):
    N = int(len(state) ** 0.5)
    conflict = 0
    
    # Check for Row Conflicts
    for row in range(N):
        current_row = [state[row * N + c] for c in range(N)]
        for i in range(N):
            val_i = current_row[i]
            # Check if val_i belongs in this row
            if val_i != 0 and (val_i - 1) // N == row:
                for j in range(i + 1, N):
                    val_j = current_row[j]
                    # Check if val_j ALSO belongs in this row
                    if val_j != 0 and (val_j - 1) // N == row:
                        # If a bigger number is to the left of a smaller number, they must step over each other
                        if val_i > val_j:
                            conflict += 2

    # Check for Column Conflicts
    for col in range(N):
        current_col = [state[r * N + col] for r in range(N)]
        for i in range(N):
            val_i = current_col[i]
            # Check if val_i belongs in this column
            if val_i != 0 and (val_i - 1) % N == col:
                for j in range(i + 1, N):
                    val_j = current_col[j]
                    # Check if val_j ALSO belongs in this column
                    if val_j != 0 and (val_j - 1) % N == col:
                        if val_i > val_j:
                            conflict += 2

    # Linear Conflict is always added to the base Manhattan Distance
    return h2_manhattan_distance(state) + conflict