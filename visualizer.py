# visualizer.py

import os
import time
from utils import get_neighbors

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def apply_action(state, action):
    for neighbor, act in get_neighbors(state):
        if act == action:
            return neighbor
    return state

def print_side_by_side(states, titles, info_lines, mem_lines):
    N = int(len(states[0]) ** 0.5)
    # The exact width of the box is 1 char for the left border + 4 chars per column
    board_width = 1 + (4 * N)
    spacing = 4
    col_width = board_width + spacing

    # Print titles and stats dynamically centered over the correct board width
    print("".join(f"{title:^{col_width}}" for title in titles))
    
    # Dynamic top border
    top_border = "┌" + "───┬" * (N - 1) + "───┐"
    print((top_border + " " * spacing) * len(states))
    
    # Dynamic rows
    for row in range(N):
        line = ""
        for state in states:
            r = state[row * N : row * N + N]
            # Format to exactly 3 characters: right-aligned number + 1 space
            f_r = [f"{x:>2} " if x != 0 else '   ' for x in r]
            
            # Join with just the wall, no extra spaces
            row_str = "│" + "│".join(f_r) + "│"
            line += row_str + " " * spacing
        print(line)
        
        # Dynamic middle borders
        if row < N - 1:
            mid_border = "├" + "───┼" * (N - 1) + "───┤"
            print((mid_border + " " * spacing) * len(states))
            
    # Dynamic bottom border
    bot_border = "└" + "───┴" * (N - 1) + "───┘"
    print((bot_border + " " * spacing) * len(states))
    
    # Print Nodes and Mem dynamically centered
    print("".join(f"{info:^{col_width}}" for info in info_lines))
    print("".join(f"{mem:^{col_width}}" for mem in mem_lines))
    print("-" * (col_width * len(states)))

def visualize_simultaneous(start_state, results):
    names = [res['name'] for res in results]
    paths = [res['path'] if res['path'] else [] for res in results]
    
    max_steps = max(len(p) for p in paths) if paths else 0
    current_states = [start_state] * len(results)
    
    for step in range(max_steps + 1):
        clear_screen()
        grid_type = f"{int(len(start_state)**0.5)}x{int(len(start_state)**0.5)}"
        print(f"=== L3: Simultaneous {grid_type} Path Execution (Step {step}/{max_steps}) ===\n")
        
        node_lines = [f"Nodes: {res['nodes']}" for res in results]
        mem_lines = [f"Mem: {res['max_mem']}" for res in results]
        
        print_side_by_side(current_states, names, node_lines, mem_lines)
        
        time.sleep(0.6)
        
        if step < max_steps:
            for i in range(len(results)):
                if step < len(paths[i]):
                    action = paths[i][step]
                    current_states[i] = apply_action(current_states[i], action)