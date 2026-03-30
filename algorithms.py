# algorithms.py

import heapq
from collections import deque
from utils import is_goal, get_neighbors

def bfs(start_state):
    queue = deque([(start_state, [])])
    visited = {start_state}
    nodes = 0
    max_memory = 0
    
    while queue:
        # Track peak memory (queue size + visited set size)
        max_memory = max(max_memory, len(queue) + len(visited))
        
        state, path = queue.popleft()
        if is_goal(state): return path, nodes, max_memory
        nodes += 1
        for next_state, action in get_neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [action]))
    return None, nodes, max_memory

def iddfs(start_state, max_depth=50):
    def dls(state, path, depth_limit, visited):
        nonlocal nodes, max_memory
        # Track peak memory (current recursion depth / path length)
        max_memory = max(max_memory, len(path))
        
        if is_goal(state): return path
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
    max_memory = 0
    for depth in range(max_depth):
        visited = {start_state}
        result = dls(start_state, [], depth, visited)
        if result not in ("CUTOFF", None): return result, nodes, max_memory
    return None, nodes, max_memory

def a_star(start_state, heuristic_func):
    tie_breaker = 0
    pq = [(heuristic_func(start_state), tie_breaker, 0, start_state, [])]
    visited = {start_state: 0}
    nodes = 0
    max_memory = 0
    
    while pq:
        # Track peak memory (priority queue size + visited dictionary size)
        max_memory = max(max_memory, len(pq) + len(visited))
        
        f, _, g, state, path = heapq.heappop(pq)
        if is_goal(state): return path, nodes, max_memory
        nodes += 1
        for next_state, action in get_neighbors(state):
            new_g = g + 1
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                heapq.heappush(pq, (new_g + heuristic_func(next_state), tie_breaker + 1, new_g, next_state, path + [action]))
    return None, nodes, max_memory

def ida_star(start_state, heuristic_func):
    def search(path, g, threshold):
        nonlocal nodes, max_memory
        # Track peak memory (current recursion depth)
        max_memory = max(max_memory, len(path))
        
        state = path[-1][0]
        f = g + heuristic_func(state)
        if f > threshold: return f
        if is_goal(state): return "FOUND"
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
    max_memory = 0
    while True:
        temp = search(path, 0, threshold)
        if temp == "FOUND": return [p[1] for p in path[1:]], nodes, max_memory
        if temp == float('inf'): return None, nodes, max_memory
        threshold = temp