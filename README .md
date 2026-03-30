# N-Puzzle Solver

A Python-based AI solver for the classic sliding tile puzzle (8-puzzle and 15-puzzle). This project implements both uninformed and informed search algorithms, comparing their time and space complexity.

##  Algorithms & Heuristics Implemented

### Uninformed Search
* **Breadth-First Search (BFS):** Guarantees the shortest path but struggles with $O(b^d)$ space complexity.
* **Iterative Deepening DFS (IDDFS):** Solves the memory limitations of BFS by using depth limits, maintaining linear space complexity at the cost of time.

### Informed Search
* **A* Search:** Uses a priority queue to evaluate paths based on $f(n) = g(n) + h(n)$. 
* **Iterative Deepening A* (IDA*):** Combines the space-efficiency of IDDFS with the directed heuristic search of A*.

### Heuristics
1. **Misplaced Tiles:** A weak admissible heuristic counting tiles out of their goal position.
2. **Manhattan Distance:** A stronger heuristic calculating the grid distance of each tile from its goal.
3. **Linear Conflict:** An advanced tie-breaking heuristic that adds cost when two tiles are in their correct row/column but must step over each other to reach their target.

## Project Structure

* `main.py`: The entry point and interactive terminal menu.
* `algorithms.py`: Contains the logic for BFS, IDDFS, A*, and IDA*.
* `heuristics.py`: Contains the math for Misplaced Tiles, Manhattan Distance, and Linear Conflict.
* `visualizer.py`: Handles the simultaneous side-by-side terminal animation.
* `utils.py`: Helper functions for reading files, generating neighbors, and checking solvability.
* `input*.txt`: Text files containing the starting board states.

## Installation & Prerequisites

This project requires standard Python 3. No external libraries are needed.

1. Clone or download the repository.
2. Ensure you have Python 3.7+ installed.
3. Open a terminal and navigate to the project directory.

## How to Run

Run the main script from your terminal:

```bash
python main.py

## You will be prompted with an interactive menu to select a puzzle file:

=== Complete 8/15-Puzzle Comparative Suite (L1-L3) ===
Select puzzle difficulty to load:
1. Easy       (input1.txt)
2. Medium     (input2.txt)
3. Hard       (input3.txt)
4. Unsolvable (input4.txt)
5. 15-Puzzle  (input_15.txt)

Custom Inputs

You can easily test your own puzzle states! Simply open any of the `input*.txt` files and paste your custom board state. 

* Numbers must be separated by spaces.
* Use `0` to represent the blank tile.
* The system will automatically detect if it is a 3x3 (9 numbers) or 4x4 (16 numbers) grid based on how many numbers you provide.

**Example of a valid custom 3x3 input:**
# `1 2 3 4 5 6 7 0 8`

**Example of a valid custom 4x4 input:**
# `1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15`

