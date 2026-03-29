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
    
    # Print Nodes (Time Complexity)
    print("".join(f"{info:^17}" for info in info_lines))
    # Print Max Memory (Space Complexity) right beneath
    print("".join(f"{mem:^17}" for mem in mem_lines))
    print("-" * (17 * len(states)))

def visualize_simultaneous(start_state, results):
    names = [res['name'] for res in results]
    paths = [res['path'] if res['path'] else [] for res in results]
    
    # Find the longest path to know how many animation frames to draw
    max_steps = max(len(p) for p in paths) if paths else 0
    current_states = [start_state] * len(results)
    
    for step in range(max_steps + 1):
        clear_screen()
        print(f"=== L1 & L2: Simultaneous Path Execution (Step {step}/{max_steps}) ===\n")
        
        node_lines = [f"Nodes: {res['nodes']}" for res in results]
        mem_lines = [f"Mem: {res['max_mem']}" for res in results]
        
        print_side_by_side(current_states, names, node_lines, mem_lines)
        
        time.sleep(0.6)
        
        if step < max_steps:
            for i in range(len(results)):
                # Only advance the state if this specific algorithm hasn't reached the goal yet
                if step < len(paths[i]):
                    action = paths[i][step]
                    current_states[i] = apply_action(current_states[i], action)