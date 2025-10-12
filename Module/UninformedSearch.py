from collections import deque
from heapq import heapify
from queue import PriorityQueue

def BFS(self, start_node):
    class Node:
        def __init__(self, state, parent=None):
            self.state = state
            self.parent = parent
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                actions.append(new_state)
        
        return actions
    
    def run(start_node):
        start_node = Node([])
        path = [[]]; self.add_log("---Path---\n[]")
        if self.is_goal(start_node.state):
            return self.solution(start_node), start_node.state, path
        frontier = deque([start_node])
        explored = {tuple(map(tuple, start_node.state))}
        while True:
            if not frontier:
                return None, None, path
            current_node = frontier.popleft()
            explored.add(tuple(map(tuple, current_node.state)))
            for action in actions(current_node.state):
                child_node = Node(action, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))
                path.append(child_node.state); self.add_log(str(child_node.state))
                if self.is_goal(child_node.state):
                    return self.solution(child_node), child_node.state, path
                if child_state_tuple not in explored and all(child_node.state != n.state for n in frontier):
                    frontier.append(child_node)
    
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result))
        self.place_rook(self.right_board_cells, self.change_state(result))
        self.right_label.configure(text="Trạng thái: Đã tìm thấy giải pháp!")

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def DFS(self, start_node):
    class Node:
        def __init__(self, state, parent=None):
            self.state = state
            self.parent = parent
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                actions.append(new_state)
        
        return actions
    
    def run(start_node):
        start_node = Node([])
        path = [[]]; self.add_log("---Path---\n[]")
        if self.is_goal(start_node.state):
            return self.solution(start_node), start_node.state, path
        frontier = deque([start_node])
        explored = {tuple(map(tuple, start_node.state))}
        while True:
            if not frontier:
                return None, None, path
            current_node = frontier.pop()
            explored.add(tuple(map(tuple, current_node.state)))
            for action in actions(current_node.state):
                child_node = Node(action, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))
                path.append(child_node.state); self.add_log(str(child_node.state))
                if self.is_goal(child_node.state):
                    return self.solution(child_node), child_node.state, path
                if child_state_tuple not in explored and all(child_node.state != n.state for n in frontier):
                    frontier.append(child_node)
    
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result))
        self.place_rook(self.right_board_cells, self.change_state(result))
        self.right_label.configure(text="Trạng thái: Đã tìm thấy giải pháp!")

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def UCS(self, start_node):
    class Node:
        def __init__(self, state, cost=0, parent=None):
            self.state = state
            self.cost = cost
            self.parent = parent
        def __lt__(self, other):
            return self.cost < other.cost
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                new_cost = self.cost((i, j))
                actions.append((new_state, new_cost))
        
        return actions
    
    def run(start_node):
        start_node = Node([])
        path = [([], 0)]; self.add_log("---Path---\n[] , Cost: 0")
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node.state)): 0}
        while True:
            if frontier.empty():
                return None, None, path
            current_node = frontier.get()
            path.append((current_node.state, current_node.cost))
            self.add_log(str(current_node.state) + " Cost: " + str(current_node.cost))
            if self.is_goal(current_node.state):
                return self.solution(current_node), current_node, path
            for action, cost in actions(current_node.state):
                child_cost = current_node.cost + cost
                child_node = Node(action, child_cost, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))

                if (all(child_node.state != n.state for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                elif (any(child_node.state == n.state for n in frontier.queue) and child_cost < explored[child_state_tuple]):
                    explored[child_state_tuple] = child_cost
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n.state == child_node.state:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break
    
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result.state) + " Cost: " + str(result.cost))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="Cost: " + str(result.cost))

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Cost: " + str(i[1]))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def DLS(self, start_node):
    class Node:
        def __init__(self, state, limit, parent=None):
            self.state = state
            self.limit = limit
            self.parent = parent
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []
        
        possible_actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                possible_actions.append(new_state)
        return possible_actions
    
    def recursive_dls(node, limit):
        path.append((node.state, node.limit))
        self.add_log(f"{node.state} , Limit: {node.limit}")

        if self.is_goal(node.state): return node
        if limit == 0: return 'cutoff'
        
        cutoff_occurred = False
        for action in actions(node.state):
            child_node = Node(action, limit-1, node)
            result = recursive_dls(child_node, limit - 1)

            if result == 'cutoff': cutoff_occurred = True
            elif result != 'failure': return result
            
        if cutoff_occurred: return 'cutoff'
        else: return 'failure'

    limit = self.n
    start_node = Node([], limit)
    path = []
    self.add_log("---Path---")

    result = recursive_dls(start_node, limit)

    if result != 'failure' and result != 'cutoff':
        self.add_log("---Result---\n" + str(result.state) + ", Limit: "+ str(result.limit))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text=f"Limit: {result.limit}")

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text=f"Limit: {i[1]}")
            self.update()
            self.after(50)
    else:
        if result == 'cutoff':
            self.add_log("No solution found within depth limit (cutoff).")
            self.right_label.configure(text=f"Trạng thái: Bị cắt ở độ sâu {limit}!")
        else:
            self.add_log("No solution found.")
            self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def IDS(self, start_node):
    class Node:
        def __init__(self, state, depth, parent=None):
            self.state = state
            self.depth = depth
            self.parent = parent
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []
        
        possible_actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                possible_actions.append(new_state)
        return possible_actions
    
    def recursive_dls(node, depth):
        path.append((node.state, node.depth))
        self.add_log(f"{node.state} , Depth: {node.depth}")

        if self.is_goal(node.state): return node
        if depth == 0: return 'cutoff'
        
        cutoff_occurred = False
        for action in actions(node.state):
            child_node = Node(action, depth-1, node)
            result = recursive_dls(child_node, depth - 1)

            if result == 'cutoff': cutoff_occurred = True
            elif result != 'failure': return result
            
        if cutoff_occurred: return 'cutoff'
        else: return 'failure'
    
    depth = -1
    path = []
    self.add_log("---Path---")

    while True:
        depth += 1
        start_node = Node([], depth)
        result = recursive_dls(start_node, depth)
        if result != 'cutoff': break
    
    if result != 'failure':
        self.add_log("---Result---\n" + str(result.state) + ", Depth: "+ str(result.depth))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text=f"Depth: {result.depth}")

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text=f"Deth: {i[1]}")
            self.update()
            self.after(50)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")
