import sys
import time
from utils import read_board_from_file, is_solvable
from algorithms import bfs, iddfs, astar, idastar
from heuristics import h1_misplaced_tiles, h2_manhattan_distance, h3_linear_conflict
from visualizer import visualize_simultaneous, clear_screen

if __name__ == "__main__":
    clear_screen()
    print("Complete 8/15-Puzzle Comparative Suite (L1-L3)")
    print("Select puzzle difficulty to load:")
    print("1. Easy       (input1.txt)")
    print("2. Medium     (input2.txt)")
    print("3. Hard       (input3.txt)")
    print("4. Unsolvable (input4.txt)")
    print("5. 15-Puzzle  (input_15.txt)")
    
    choice = input("\nEnter 1, 2, 3, 4, or 5: ").strip()
    
    file_map = {
        '1': 'input1.txt', '2': 'input2.txt', 
        '3': 'input3.txt', '4': 'input4.txt',
        '5': 'input_15.txt'
    }
    
    if choice not in file_map:
        print("Invalid choice. Exiting.")
        sys.exit()

    filename = file_map[choice]
    try:
        start_board = read_board_from_file(filename)
    except FileNotFoundError:
        print(f"File {filename} not found! Please create it.")
        sys.exit()

    print(f"\nLoaded starting board from {filename}: {start_board}")

    # Level 2 / Level 3 Solvability Check
    if not is_solvable(start_board):
        print("CHECK: This board is mathematically UNSOLVABLE.")
        print("Exiting to save your computer from an infinite loop.")
        sys.exit()
        
    print("CHECK: Board is solvable! Proceeding to algorithms...\n")
    print("Computing search histories... Please wait.")
    
    results = []
    
    print("Running BFS...")
    res_bfs = bfs(start_board)
    if res_bfs: results.append(res_bfs)

    print("Running IDDFS...")
    res_iddfs = iddfs(start_board)
    if res_iddfs: results.append(res_iddfs)

    print("Running A* (Misplaced)...")
    res_astar_mp = astar(start_board, h1_misplaced_tiles, "A* (Misplaced)")
    if res_astar_mp: results.append(res_astar_mp)
    
    print("Running A* (Manhattan)...")
    res_astar_m = astar(start_board, h2_manhattan_distance, "A* (Manhattan)")
    if res_astar_m: results.append(res_astar_m)

    print("Running A* (Lin.Conf)...")
    res_astar_lc = astar(start_board, h3_linear_conflict, "A* (Lin.Conf)")
    if res_astar_lc: results.append(res_astar_lc)

    print("Running IDA* (Misplaced)...") 
    res_idastar_mp = idastar(start_board, h1_misplaced_tiles, "IDA* (Misplaced)")
    if res_idastar_mp: results.append(res_idastar_mp)
    
    print("Running IDA* (Manhattan)...")
    res_idastar_m = idastar(start_board, h2_manhattan_distance, "IDA* (Manhattan)")
    if res_idastar_m: results.append(res_idastar_m)
    
    print("Running IDA* (Lin.Conf)...") 
    res_idastar_lc = idastar(start_board, h3_linear_conflict, "IDA* (Lin.Conf)")
    if res_idastar_lc: results.append(res_idastar_lc)

    if results:
        print("\nDone!")
        time.sleep(2)
        visualize_simultaneous(start_board, results)
    else:
        print("No solutions found.")