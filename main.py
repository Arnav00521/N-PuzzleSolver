# main.py

import sys
from utils import read_board_from_file, is_solvable
from heuristics import h1_misplaced_tiles, h2_manhattan_distance, h3_linear_conflict
from algorithms import bfs, iddfs, a_star, ida_star
from visualizer import clear_screen, visualize_simultaneous

if __name__ == "__main__":
    clear_screen()
    print("=== 8-Puzzle Solver (L1 & L2) ===")
    print("Select puzzle difficulty to load:")
    print("1. Easy   (input1.txt)")
    print("2. Medium (input2.txt)")
    print("3. Hard   (input3.txt)")
    print("4. Unsolvable")
    print("5. 15-Puzzle")
    
    choice = input("\nEnter 1, 2, 3, 4, or 5: ").strip()
    
    file_map = {'1': 'input1.txt', '2': 'input2.txt', '3': 'input3.txt', '4': 'input4.txt', '5': 'input_15.txt'}
    
    if choice not in file_map:
        print("Invalid choice. Exiting.")
        sys.exit()
        
    filename = file_map[choice]
    start_board = read_board_from_file(filename)
    
    if not start_board:
        sys.exit()
    
    print(f"\nLoaded starting board from {filename}: {start_board}")
    
    # --- LEVEL 2: SOLVABILITY CHECK ---
    if not is_solvable(start_board):
        print("\n❌ L2 CHECK: This board is mathematically UNSOLVABLE (Odd number of inversions).")
        print("Exiting to save your computer from an infinite loop.")
        sys.exit()
    else:
        print("✅ L2 CHECK: Board is solvable! Proceeding to algorithms...")
    
    # List of all algorithms and heuristics to compare
    algorithms = [
        ("BFS", lambda s: bfs(s)),
        ("IDDFS", lambda s: iddfs(s)),
        ("A*(Misplaced)", lambda s: a_star(s, h1_misplaced_tiles)),
        ("A*(Manhattan)", lambda s: a_star(s, h2_manhattan_distance)),
        ("A*(Lin.Conf)", lambda s: a_star(s, h3_linear_conflict)), 
        ("IDA*(Misplaced)", lambda s: ida_star(s, h1_misplaced_tiles)),
        ("IDA*(Manhtn)", lambda s: ida_star(s, h2_manhattan_distance)),
        ("IDA*(Lin.Conf)", lambda s: ida_star(s, h3_linear_conflict)) # <- NEW IDA* Linear Conflict
    ]

    print("\nComputing optimal paths... Please wait.")
    results = []
    
    for name, algo in algorithms:
        # Unpacking the 3 variables: path, time complexity, space complexity
        path, nodes, max_memory = algo(start_board)
        
        results.append({
            'name': name,
            'path': path,
            'nodes': nodes,
            'max_mem': max_memory
        })
        
    # Launch the terminal animation
    visualize_simultaneous(start_board, results)
    
    print("\nSearch complete.")
    print("Notice how Node counts validate Time Complexity, and Mem counts validate Space Complexity!")