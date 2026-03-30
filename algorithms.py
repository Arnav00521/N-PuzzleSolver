from collections import deque
import heapq
import itertools
from utils import is_goal, get_neighbors

def bfs(start_state):
    queue = deque([(start_state, [])])
    visited = {start_state}
    nodes_evaluated = 0
    max_mem = 1
    search_history = []
    while queue:
        max_mem =max(max_mem, len(queue) + len(visited))
        current_state, path = queue.popleft()
        search_history.append(current_state)
        nodes_evaluated += 1
        if is_goal(current_state):
            return {'name':'BFS','path': path,'nodes': nodes_evaluated,'max_mem': max_mem,'search_history': search_history}
        for neighbor, action in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [action]))
    return None

def iddfs(start_state):
    nodes_evaluated = 0
    max_mem = 0
    search_history = []
    def dls(state, path, states_in_path, depth):
        nonlocal nodes_evaluated, max_mem
        max_mem = max(max_mem, len(states_in_path))
        search_history.append(state)
        nodes_evaluated += 1
        if is_goal(state):
            return path
        if depth <= 0:
            return None
        for neighbor, action in get_neighbors(state):
            if neighbor not in states_in_path:
                states_in_path.add(neighbor)
                result= dls(neighbor, path + [action], states_in_path, depth - 1)
                states_in_path.remove(neighbor)
                if result is not None:
                    return result
        return None

    depth = 0
    while True:
        states_in_path = {start_state}
        result =dls(start_state, [], states_in_path, depth)
        if result is not None:
            return {'name':'IDDFS','path':result,'nodes':nodes_evaluated,'max_mem': max_mem, 'search_history': search_history}
        depth+= 1

def astar(start_state, heuristic_func, name):
    pq=[]
    counter = itertools.count()
    heapq.heappush(pq, (0, 0, next(counter), start_state, []))
    visited ={}
    nodes_evaluated = 0
    max_mem = 1
    search_history = []

    while pq:
        max_mem = max(max_mem,len(pq)+len(visited))
        f, g, _, current_state, path = heapq.heappop(pq)
        if current_state in visited and visited[current_state]<= g:
            continue
        visited[current_state]= g
        search_history.append(current_state)
        nodes_evaluated += 1
        if is_goal(current_state):
            return {'name': name, 'path': path, 'nodes': nodes_evaluated, 'max_mem': max_mem, 'search_history': search_history}
        for neighbor, action in get_neighbors(current_state):
            new_g=g + 1
            if neighbor not in visited or new_g < visited.get(neighbor, float('inf')):
                f_new=new_g + heuristic_func(neighbor)
                heapq.heappush(pq, (f_new, new_g, next(counter), neighbor, path + [action]))
    return None

def idastar(start_state, heuristic_func, name):
    nodes_evaluated = 0
    max_mem = 0
    search_history = []
    def search(state, g, bound, path, states_in_path):
        nonlocal nodes_evaluated, max_mem
        max_mem = max(max_mem, len(states_in_path))
        search_history.append(state)
        nodes_evaluated += 1
        f=g+ heuristic_func(state)
        if f>bound:
            return f, None
        if is_goal(state):
            return True,path
            
        min_bound = float('inf')
        for neighbor, action in get_neighbors(state):
            if neighbor not in states_in_path:
                states_in_path.add(neighbor)
                t, found_path=search(neighbor, g + 1, bound, path + [action], states_in_path)
                if found_path is not None:
                    return t,found_path
                if t<min_bound:
                    min_bound=t
                states_in_path.remove(neighbor)
        return min_bound, None

    bound = heuristic_func(start_state)
    while True:
        states_in_path={start_state}
        t, path=search(start_state, 0, bound, [], states_in_path)
        if path is not None:
            return {'name': name, 'path': path, 'nodes': nodes_evaluated, 'max_mem': max_mem, 'search_history': search_history}
        if t==float('inf'):
            return None
        bound = t
