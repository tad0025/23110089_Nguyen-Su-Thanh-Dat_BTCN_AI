from heapq import heapify
from queue import PriorityQueue

def cost(self, positions):
    return 2 * (self.n - len(positions)) + 1 # cost = số ô ko thể đặt sau khi đạt tại ô i,j trên bàn cờ
def heuristic(self, positions):
    x, y = positions
    return abs(self.n - x - 1) + abs(self.n - y - 1)

def Greedy(self, start_node):
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                new_heuristic = heuristic(self, (i, j))
                actions.append((new_state, new_heuristic))
        
        return actions
    
    def run(start_node):
        start_node = (heuristic(self, (0, 0)), [])
        path = [(heuristic(self, (0, 0)), [])]; self.add_log("---Path---\n[], Heuristic: " + str(start_node[0]))
        
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node[1])): start_node[0]}
        while True:
            if frontier.empty():
                return None, path
            current_node = frontier.get()
            path.append(current_node)
            self.add_log(str(current_node[1]) + " Heuristic: " + str(current_node[0]))
            if self.is_goal(current_node[1]):
                return current_node, path
            for action, child_heuristic in actions(current_node[1]):
                child_node = (child_heuristic, action)
                child_state_tuple = tuple(map(tuple, child_node[1]))

                if (all(child_node[1] != n[1] for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                    explored[child_state_tuple] = child_heuristic
                elif (any(child_node[1] == n[1] for n in frontier.queue) and child_heuristic < explored[child_state_tuple]):
                    explored[child_state_tuple] = child_heuristic
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n[1] == child_node[1]:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break

    result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result[1]) + " Heuristic: " + str(result[0]))
        self.place_rook(self.right_board_cells, self.change_state(result[1]))
        self.right_label.configure(text="Heuristic: " + str(result[0]))
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")
    
    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i[1]))
        self.left_label.configure(text="Heuristic: " + str(i[0]))
        self.update()
        self.after(50)

def A_Star(self, start_node):
    class Node:
        def __init__(self, state, cost=0, heuristic=0, parent=None):
            self.state = state
            self.cost = cost
            self.heuristic = heuristic
            self.parent = parent
        def __lt__(self, other):
            return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                new_cost = cost(self, (i, j))
                new_heuristic = heuristic(self, (i, j))
                actions.append((new_state, new_cost, new_heuristic))

        return actions
    
    def run(start_node):
        start_node = Node([], heuristic(self, (0, 0)))
        path = [([], (start_node.cost, start_node.heuristic))]; self.add_log("---Path---\n[], Heuristic: " + str(start_node.heuristic))
        
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node.state)): (start_node.cost, start_node.heuristic)}
        while True:
            if frontier.empty():
                return None, None, path
            current_node = frontier.get()
            path.append((current_node.state, (current_node.cost, current_node.heuristic)))
            self.add_log(str(current_node.state) + " F(n): " + str(current_node.cost+current_node.heuristic))
            if self.is_goal(current_node.state):
                return self.solution(current_node), current_node, path
            for action, cost, h in actions(current_node.state):
                child_cost = current_node.cost + cost
                child_heuristic = h
                child_node = Node(action, child_cost, child_heuristic, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))

                if (all(child_node.state != n.state for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                elif (any(child_node.state == n.state for n in frontier.queue) and child_cost+child_heuristic < sum(explored[child_state_tuple])):
                    explored[child_state_tuple] = (child_cost, child_heuristic)
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n.state == child_node.state:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break

    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result.state) + " F(n): " + str(result.cost+result.heuristic))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="F(n): " + str(result.cost+result.heuristic))

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="F(n): " + str(i[1][0]+i[1][1]))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")