# utils.py

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GRID_SIZE = 3

def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, GRID_SIZE)
    moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    
    for action, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
            new_idx = new_row * GRID_SIZE + new_col
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append((tuple(new_state), action))
    return neighbors

def read_board_from_file(filename):
    try:
        with open(filename, 'r') as f:
            numbers = [int(x) for line in f.readlines() for x in line.split()]
            if len(numbers) != 9:
                print(f"Error: {filename} must contain exactly 9 numbers.")
                return None
            return tuple(numbers)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Make sure it is in the same folder.")
        return None
    
def is_solvable(state):
    """
    Checks if an 8-puzzle board is mathematically solvable by counting inversions.
    An odd number of inversions means it's impossible.
    """
    inversions = 0
    # Remove the 0 (blank tile) for the math
    tiles = [t for t in state if t != 0]
    
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
                
    return inversions % 2 == 0