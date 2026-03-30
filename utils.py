# utils.py

def read_board_from_file(filename):
    with open(filename, 'r') as f:
        # Reads all numbers, ignoring line breaks, so it works for 3x3 or 4x4
        numbers = []
        for line in f:
            numbers.extend([int(x) for x in line.split() if x.strip()])
    return tuple(numbers)

def is_goal(state):
    # Dynamically generates the goal based on board length
    # e.g., (1, 2, ..., 8, 0) or (1, 2, ..., 15, 0)
    goal = tuple(range(1, len(state))) + (0,)
    return state == goal

def get_neighbors(state):
    # Dynamically calculates grid width (N)
    N = int(len(state) ** 0.5) 
    empty_idx = state.index(0)
    row, col = divmod(empty_idx, N)
    
    neighbors = []
    directions = {
        'Up': (row - 1, col),
        'Down': (row + 1, col),
        'Left': (row, col - 1),
        'Right': (row, col + 1)
    }
    
    for action, (r, c) in directions.items():
        if 0 <= r < N and 0 <= c < N:
            new_idx = r * N + c
            new_state = list(state)
            # Swap the empty tile with the target tile
            new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
            neighbors.append((tuple(new_state), action))
            
    return neighbors

def is_solvable(state):
    N = int(len(state) ** 0.5)
    state_no_zero = [x for x in state if x != 0]
    inversions = 0
    
    # Count inversions
    for i in range(len(state_no_zero)):
        for j in range(i + 1, len(state_no_zero)):
            if state_no_zero[i] > state_no_zero[j]:
                inversions += 1
                
    # Level 2: Odd grid (3x3 8-puzzle) rule
    if N % 2 != 0:
        return inversions % 2 == 0
        
    # Level 3: Even grid (4x4 15-puzzle) rule
    else:
        empty_idx = state.index(0)
        blank_row_from_top = empty_idx // N
        blank_row_from_bottom = N - blank_row_from_top
        
        # If blank is on an even row from bottom, inversions must be odd
        if blank_row_from_bottom % 2 == 0:
            return inversions % 2 != 0
        # If blank is on an odd row from bottom, inversions must be even
        else:
            return inversions % 2 == 0