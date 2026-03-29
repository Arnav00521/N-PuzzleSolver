import heapq
import time
import os
import sys
from collections import deque

# --- 1. Environment & State Setup ---
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

# --- 2. Heuristic Functions ---
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

# --- 3. Search Algorithms ---
def bfs(start_state):
    queue = deque([(start_state, [])])
    visited = {start_state}
    nodes = 0
    while queue:
        state, path = queue.popleft()
        if state == GOAL_STATE: return path, nodes
        nodes += 1
        for next_state, action in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [action]))
    return None, nodes

def iddfs(start_state, max_depth=50):
    def dls(state, path, depth_limit, visited):
        nonlocal nodes
        if state == GOAL_STATE: return path
        if depth_limit == 0: return "CUTOFF"
        nodes += 1
        cutoff_occurred = False
        for next_state, action in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                result = dls(next_state, path + [action], depth_limit - 1, visited)
                visited.remove(next_state)
                if result == "CUTOFF": cutoff_occurred = True
                elif result is not None: return result
        return "CUTOFF" if cutoff_occurred else None

    nodes = 0
    for depth in range(max_depth):
        visited = {start_state}
        result = dls(start_state, [], depth, visited)
        if result not in ("CUTOFF", None): return result, nodes
    return None, nodes

def a_star(start_state, heuristic_func):
    tie_breaker = 0
    pq = [(heuristic_func(start_state), tie_breaker, 0, start_state, [])]
    visited = {start_state: 0}
    nodes = 0
    while pq:
        f, _, g, state, path = heapq.heappop(pq)
        if state == GOAL_STATE: return path, nodes
        nodes += 1
        for next_state, action in get_neighbors(state):
            new_g = g + 1
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                heapq.heappush(pq, (new_g + heuristic_func(next_state), tie_breaker + 1, new_g, next_state, path + [action]))
    return None, nodes

def ida_star(start_state, heuristic_func):
    def search(path, g, threshold):
        nonlocal nodes
        state = path[-1][0]
        f = g + heuristic_func(state)
        if f > threshold: return f
        if state == GOAL_STATE: return "FOUND"
        nodes += 1
        min_threshold = float('inf')
        for next_state, action in get_neighbors(state):
            if next_state not in [p[0] for p in path]:
                path.append((next_state, action))
                temp = search(path, g + 1, threshold)
                if temp == "FOUND": return "FOUND"
                if temp < min_threshold: min_threshold = temp
                path.pop()
        return min_threshold

    threshold = heuristic_func(start_state)
    path = [(start_state, "")]
    nodes = 0
    while True:
        temp = search(path, 0, threshold)
        if temp == "FOUND": return [p[1] for p in path[1:]], nodes
        if temp == float('inf'): return None, nodes
        threshold = temp

# --- 4. File I/O & Visualization Engine ---
def read_board_from_file(filename):
    """Reads a 3x3 grid from a text file and converts it to a 1D tuple."""
    try:
        with open(filename, 'r') as f:
            # Read all numbers, ignoring newlines and extra spaces
            numbers = [int(x) for line in f.readlines() for x in line.split()]
            if len(numbers) != 9:
                print(f"Error: {filename} must contain exactly 9 numbers.")
                return None
            return tuple(numbers)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Make sure it is in the same folder.")
        return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def apply_action(state, action):
    for neighbor, act in get_neighbors(state):
        if act == action:
            return neighbor
    return state

def print_side_by_side(states, titles, info_lines):
    print("".join(f"{title:^17}" for title in titles))
    print("┌───┬───┬───┐    " * len(states))
    for row in range(3):
        line = ""
        for state in states:
            r = state[row*3 : row*3+3]
            f_r = [str(x) if x != 0 else ' ' for x in r]
            line += f"│ {f_r[0]} │ {f_r[1]} │ {f_r[2]} │    "
        print(line)
        if row < 2:
            print("├───┼───┼───┤    " * len(states))
    print("└───┴───┴───┘    " * len(states))
    print("".join(f"{info:^17}" for info in info_lines))
    print("-" * (17 * len(states)))

def visualize_simultaneous(start_state, results):
    names = [res['name'] for res in results]
    paths = [res['path'] if res['path'] else [] for res in results]
    nodes = [res['nodes'] for res in results]
    
    max_steps = max(len(p) for p in paths)
    current_states = [start_state] * len(results)
    
    for step in range(max_steps + 1):
        clear_screen()
        print(f"=== L1: Simultaneous Path Execution (Step {step}/{max_steps}) ===\n")
        
        info_lines = [f"Nodes: {n}" for n in nodes]
        print_side_by_side(current_states, names, info_lines)
        
        time.sleep(0.6)
        
        if step < max_steps:
            for i in range(len(results)):
                if step < len(paths[i]):
                    action = paths[i][step]
                    current_states[i] = apply_action(current_states[i], action)

# --- 5. Demo Runner ---
if __name__ == "__main__":
    clear_screen()
    print("=== 8-Puzzle Solver (L1) ===")
    print("Select puzzle difficulty to load:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    choice = input("\nEnter 1, 2, or 3: ").strip()
    
    file_map = {'1': 'input1.txt', '2': 'input2.txt', '3': 'input3.txt'}
    
    if choice not in file_map:
        print("Invalid choice. Exiting.")
        sys.exit()
        
    filename = file_map[choice]
    start_board = read_board_from_file(filename)
    
    if not start_board:
        sys.exit()
    
    print(f"\nLoaded starting board from {filename}: {start_board}")
    
    algorithms = [
        ("BFS", lambda s: bfs(s)),
        ("IDDFS", lambda s: iddfs(s)),
        ("A*(Misplaced)", lambda s: a_star(s, h1_misplaced_tiles)),
        ("A*(Manhattan)", lambda s: a_star(s, h2_manhattan_distance)),
        ("IDA*(Misplaced)", lambda s: ida_star(s, h1_misplaced_tiles)),
        ("IDA*(Manhtn)", lambda s: ida_star(s, h2_manhattan_distance))
    ]

    print("\nComputing optimal paths... Please wait.")
    results = []
    
    for name, algo in algorithms:
        path, nodes = algo(start_board)
        results.append({
            'name': name,
            'path': path,
            'nodes': nodes
        })
        
    visualize_simultaneous(start_board, results)
