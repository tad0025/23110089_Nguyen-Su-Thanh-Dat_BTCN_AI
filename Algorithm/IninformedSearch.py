from heapq import heapify
from queue import PriorityQueue

def Greedy(self, start_node):
    class Node:
        def __init__(self, state, heuristic=0, parent=None):
            self.state = state
            self.heuristic = heuristic
            self.parent = parent
        def __lt__(self, other):
            return self.heuristic < other.heuristic
    
    def actions(state):
        i = len(state)
        if i >= self.n: return []

        actions = []
        for j in range(self.n):
            if all(y != j for (_, y) in state):
                new_state = state[:] + [(i, j)]
                new_heuristic = self.heuristic(new_state)
                actions.append((new_state, new_heuristic))
        
        return actions
    
    def run(start_node):
        start_node = Node([], self.heuristic([]))
        path = [([], 0)]; self.add_log("---Path---\n([] , 0)")
        if self.is_goal(start_node.state):
            return self.solution(start_node), start_node, path
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node.state)): start_node.heuristic}
        while True:
            if frontier.empty():
                return None, None, path
            current_node = frontier.get()
            path.append((current_node.state, current_node.heuristic))
            self.add_log(str(current_node.state) + " Heuristic: " + str(current_node.heuristic))
            if self.is_goal(current_node.state):
                return self.solution(current_node), current_node, path
            for action, heuristic in actions(current_node.state):
                child_node = Node(action, heuristic, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))

                if (all(child_node.state != n.state for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                elif (child_state_tuple in explored and heuristic < explored[child_state_tuple]):
                    explored[child_state_tuple] = heuristic
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n.state == child_node.state:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result.state) + " Heuristic: " + str(result.heuristic))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="Heuristic: " + str(result.heuristic))

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Heuristic: " + str(i[1]))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")

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
                new_cost = i + 1
                new_heuristic = self.heuristic(new_state)
                actions.append((new_state, new_cost, new_heuristic))
        
        return actions
    
    def run(start_node):
        start_node = Node([], 0, self.heuristic([]))
        path = [([], 0, start_node.heuristic)]; self.add_log("---Path---\n([] , 0 , " + str(start_node.heuristic) + ")")
        if self.is_goal(start_node.state):
            return self.solution(start_node), start_node, path
        frontier = PriorityQueue()
        frontier.put(start_node)
        explored = {tuple(map(tuple, start_node.state)): start_node.cost}
        while True:
            if frontier.empty():
                return None, None, path
            current_node = frontier.get()
            path.append((current_node.state, current_node.cost, current_node.heuristic))
            self.add_log(str(current_node.state) + " Cost: " + str(current_node.cost) + " Heuristic: " + str(current_node.heuristic))
            if self.is_goal(current_node.state):
                return self.solution(current_node), current_node, path
            for action, cost, heuristic in actions(current_node.state):
                child_node = Node(action, cost + current_node.cost, heuristic, current_node)
                child_state_tuple = tuple(map(tuple, child_node.state))

                if (all(child_node.state != n.state for n in frontier.queue) and (child_state_tuple not in explored)):
                    frontier.put(child_node)
                elif (child_state_tuple in explored and child_node.cost < explored[child_state_tuple]):
                    explored[child_state_tuple] = child_node
                    # frontier.put(child_node)
                    for i, n in enumerate(frontier.queue):
                        if n.state == child_node.state:
                            frontier.queue[i] = child_node
                            heapify(frontier.queue)
                            break
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result.state) + " Cost: " + str(result.cost) + " Heuristic: " + str(result.heuristic))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="Cost: " + str(result.cost) + " Heuristic: " + str(result.heuristic))

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Cost: " + str(i[1]) + " Heuristic: " + str(i[2]))
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")