from collections import deque
from heapq import heapify
from queue import PriorityQueue

def BFS(self, start_node):
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
        path = [[]]; self.add_log("---Path---\n[]")
        if self.is_goal(start_node):
            return start_node.state, path
        frontier = deque([start_node])
        explored = {tuple(map(tuple, start_node))}
        while True:
            if not frontier: return None, path
            current_node = frontier.popleft()
            explored.add(tuple(map(tuple, current_node)))
            for child_node in actions(current_node):
                child_state_tuple = tuple(map(tuple, child_node))
                path.append(child_node); self.add_log(str(child_node))
                if self.is_goal(child_node):
                    return child_node, path
                if child_state_tuple not in explored:
                    frontier.append(child_node)
    
    result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result))
        self.place_rook(self.right_board_cells, self.change_state(result))
        self.right_label.configure(text="Trạng thái: Đã tìm thấy giải pháp!")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")
    
    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i))
        self.update()
        self.after(50)

def DFS(self, start_node):
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
        path = [[]]; self.add_log("---Path---\n[]")
        if self.is_goal(start_node):
            return start_node.state, path
        frontier = deque([start_node])
        explored = {tuple(map(tuple, start_node))}
        while True:
            if not frontier: return None, path
            current_node = frontier.pop()
            explored.add(tuple(map(tuple, current_node)))
            for child_node in actions(current_node):
                child_state_tuple = tuple(map(tuple, child_node))
                path.append(child_node); self.add_log(str(child_node))
                if self.is_goal(child_node):
                    return child_node, path
                if child_state_tuple not in explored:
                    frontier.append(child_node)
    
    result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result))
        self.place_rook(self.right_board_cells, self.change_state(result))
        self.right_label.configure(text="Trạng thái: Đã tìm thấy giải pháp!")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")
    
    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i))
        self.update()
        self.after(50)

def UCS(self, start_node):
    def cost(positions):
        return 2 * (self.n - len(positions)) + 1 # cost = số ô ko thể đặt sau khi đạt tại ô i,j trên bàn cờ

    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                new_cost = cost((i, j))
                actions.append((new_state, new_cost))
        
        return actions
    
    def run(start_node):
        start_node = (0, start_node)
        path = [(0, [])]; self.add_log("---Path---\n[] , Cost: 0")
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node[1])): 0}
        while True:
            if frontier.empty(): return None, path
            current_node = frontier.get()
            path.append(current_node)
            self.add_log(str(current_node[1]) + " Cost: " + str(current_node[0]))
            if self.is_goal(current_node[1]):
                return current_node, path
            for action, cost in actions(current_node[1]):
                child_cost = current_node[0] + cost
                child_node = (child_cost, action)
                child_state_tuple = tuple(map(tuple, child_node[1]))

                if (all(child_node[1] != n[1] for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                    explored[child_state_tuple] = child_cost
                elif (any(child_node[1] == n[1] for n in frontier.queue) and child_cost < explored[child_state_tuple]):
                    explored[child_state_tuple] = child_cost
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n[1] == child_node[1]:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break
    
    result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result[1]) + " Cost: " + str(result[0]))
        self.place_rook(self.right_board_cells, self.change_state(result[1]))
        self.right_label.configure(text="Cost: " + str(result[0]))
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i[1]))
        self.left_label.configure(text="Cost: " + str(i[0]))
        self.update()
        self.after(50)

def DLS(self, start_node):
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
        path.append(node)
        self.add_log(f"{node[0]} , Limit: {node[1]}")

        if self.is_goal(node[0]): return node
        if limit == 0: return 'cutoff'
        
        cutoff_occurred = False
        for action in actions(node[0]):
            child_node = (action, limit-1)
            result = recursive_dls(child_node, limit - 1)

            if result == 'cutoff': cutoff_occurred = True
            elif result != 'failure': return result
            
        if cutoff_occurred: return 'cutoff'
        else: return 'failure'

    limit = self.n
    start_node = ([], limit)
    path = []
    self.add_log("---Path---")

    result = recursive_dls(start_node, limit)

    if result != 'failure' and result != 'cutoff':
        self.add_log("---Result---\n" + str(result[0]) + ", Limit: "+ str(result[1]))
        self.place_rook(self.right_board_cells, self.change_state(result[0]))
        self.right_label.configure(text=f"Limit: {result[1]}")
    else:
        if result == 'cutoff':
            self.add_log("No solution found within depth limit (cutoff).")
            self.right_label.configure(text=f"Trạng thái: Bị cắt ở độ sâu {limit}!")
        else:
            self.add_log("No solution found.")
            self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")
    
    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i[0]))
        self.left_label.configure(text=f"Limit: {i[1]}")
        self.update()
        self.after(50)

def IDS(self, start_node):
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
        path.append(node)
        self.add_log(f"{node[0]} , Depth: {node[1]}")

        if self.is_goal(node[0]): return node
        if depth == 0: return 'cutoff'
        
        cutoff_occurred = False
        for action in actions(node[0]):
            child_node = (action, depth-1)
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
        start_node = ([], depth)
        result = recursive_dls(start_node, depth)
        if result != 'cutoff': break
    
    if result != 'failure':
        self.add_log("---Result---\n" + str(result[0]) + ", Depth: "+ str(result[1]))
        self.place_rook(self.right_board_cells, self.change_state(result[0]))
        self.right_label.configure(text=f"Depth: {result[1]}")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i[0]))
        self.left_label.configure(text=f"Depth: {i[1]}")
        self.update()
        self.after(50)