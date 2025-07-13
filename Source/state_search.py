from collections import deque
import heapq
import state_logic as sl

def reconstruct_path(came_from, state):
    path = [state]
    while state in came_from:
        state = came_from[state]
        path.append(state)
    path.reverse()
    return path

# bfs zone
def bfs(start):
    frontier = deque([start])
    came_from = {}
    visited = set()

    while frontier:
        state = frontier.popleft()
        if state in visited:
            continue
        visited.add(state)

        if sl.is_goal(state):
            path = reconstruct_path(came_from, state)
            return path, len(path) - 1
        
        succs, _ = sl.expand(state)
        for succ in succs:
            if succ not in visited and succ not in frontier:
                frontier.append(succ)
                came_from[succ] = state
        
    return [], float('inf')

# ids zone
def dls(state, depth, came_from, visited):
    if sl.is_goal(state):
        return reconstruct_path(came_from, state), len(came_from)
    
    if depth == 0:
        return [], float('inf')
    
    visited.add(state)
    succs, _ = sl.expand(state)
    for succ in succs:
        if succ not in visited:
            came_from[succ] = state
            path, _ = dls(succ, depth - 1, came_from, visited)
            if path:
                return path, len(path) - 1
    visited.remove(state)
    return [], float('inf')

def ids(start, max_depth = 34):
    for depth in range(max_depth):
        came_from = {}
        visited = set()
        path, cost = dls(start, depth, came_from, visited)
        if path:
            return path, cost
    return [], float('inf')

# ucs zone
def ucs(start):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        cost, state = heapq.heappop(frontier)

        if sl.is_goal(state):
            path = reconstruct_path(came_from, state)
            return path, cost
        succs, costs = sl.expand(state)

        for succ, move_cost in zip(succs, costs):
            new_cost = cost + move_cost
            if succ not in cost_so_far or new_cost < cost_so_far[succ]:
                cost_so_far[succ] = new_cost
                heapq.heappush(frontier, (new_cost, succ))
                came_from[succ] = state

    return [], float('inf')

# a* zone
def h(state):
    if len(state) != 36 or not sl.is_legit(state):
        return 0

    board = [0] * 36
    a_location = 17

    for i in range(36):
        ch = state[i]
        if ch == 'a':
            if 12 <= i <= 17:
                a_location = i
            for k in range(i - 1, i + 1):
                if 0 <= k < 36:
                    board[k] = 2
        elif ch == 'b':
            for k in range(i - 1, i + 1):
                if 0 <= k < 36:
                    board[k] = 2
        elif ch == 'c':
            for k in range(i - 6, i + 1, 6):
                if 0 <= k < 36:
                    board[k] = 2
        elif ch == 'm':
            for k in range(i - 2, i + 1):
                if 0 <= k < 36:
                    board[k] = 3
        elif ch == 'n':
            for k in range(i - 12, i + 1, 6):
                if 0 <= k < 36:
                    board[k] = 3

    distance = 17 - a_location
    blockers = sum(board[k] for k in range(a_location + 1, 18))

    return distance * 2 + blockers

def a_star(start):
    frontier = [(h(start), 0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, cost, state = heapq.heappop(frontier)
    
        if sl.is_goal(state):
            path = reconstruct_path(came_from, state)
            return path, cost
    
        succs, costs = sl.expand(state)
    
        for succ, move_cost in zip(succs, costs):
            new_cost = cost + move_cost
            if succ not in cost_so_far or new_cost < cost_so_far[succ]:
                cost_so_far[succ] = new_cost
                priority = new_cost + h(succ)
                heapq.heappush(frontier, (priority, new_cost, succ))
                came_from[succ] = state
    
    return [], float('inf')
