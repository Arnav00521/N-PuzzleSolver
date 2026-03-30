# visualizer.py

import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_side_by_side(states, titles, info_lines, mem_lines):
    N = int(len(states[0]) ** 0.5)
    # The exact width of the box is 1 char for the left border + 4 chars per column
    board_width = 1 + (4 * N)
    spacing = 4
    col_width = board_width + spacing

    # Print titles and stats dynamically centered
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
    # We now pull the SEARCH HISTORY instead of the PATH
    histories = [res.get('search_history', []) for res in results]
    
    # Find the longest search history
    max_steps = max(len(h) for h in histories) if histories else 0
    
    for step in range(max_steps):
        clear_screen()
        N = int(len(start_state)**0.5)
        grid_type = f"{N}x{N}"
        print(f"=== Simultaneous {grid_type} Search Process (Frame {step + 1}/{max_steps}) ===\n")
        
        node_lines = [f"Nodes: {res['nodes']}" for res in results]
        mem_lines = [f"Mem: {res['max_mem']}" for res in results]
        
        current_states = []
        for i in range(len(results)):
            # Show active searching if the algorithm hasn't finished
            if step < len(histories[i]):
                current_states.append(histories[i][step])
            # Freeze on the goal state if the algorithm finished early
            else:
                current_states.append(histories[i][-1])
                
        print_side_by_side(current_states, names, node_lines, mem_lines)
        
        # Fast animation speed (adjust this up or down to your liking)
        time.sleep(0.5)