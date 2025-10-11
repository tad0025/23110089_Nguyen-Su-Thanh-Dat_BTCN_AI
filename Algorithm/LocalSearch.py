def Hill_Climbing(self, start_node):
    def random_restart():
        current = start_node
        path = [(current, self.heuristic(current))]; self.add_log("---Path---\n(" + str(current) + " , " + str(self.heuristic(current)) + ")")
        while True:
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return None, path
            next_node = min(neighbors, key=lambda x: self.heuristic(x))
            path.append((next_node, self.heuristic(next_node)))
            self.add_log(str(next_node) + " Heuristic: " + str(self.heuristic(next_node)))
            if self.heuristic(next_node) >= self.heuristic(current):
                return current, path
            current = next_node

    def run():
        max_restarts = 100
        for _ in range(max_restarts):
            solution, path = random_restart()
            if solution and self.is_goal(solution):
                return self.solution_path(solution), path
        return None, path

    solution, path = run()
    if solution:
        self.add_log("Solution found: " + str(solution))
        self.right_label.configure(text="Solution found: " + str(solution))
        for state, heuristic in path:
            self.draw_board(state)
            self.left_label.configure(text=f"State: {state}\nHeuristic: {heuristic}")
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")

def Simulated_Annealing(self, start_node):
    import math, random

    def run():
        current = start_node
        current_heuristic = self.heuristic(current)
        path = [(current, current_heuristic)]; self.add_log("---Path---\n(" + str(current) + " , " + str(current_heuristic) + ")")
        T = 1.0
        T_min = 0.0001
        alpha = 0.99

        while T > T_min:
            neighbors = self.get_neighbors(current)
            if not neighbors:
                break
            next_node = random.choice(neighbors)
            next_heuristic = self.heuristic(next_node)
            delta_e = next_heuristic - current_heuristic
            if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / T):
                current, current_heuristic = next_node, next_heuristic
                path.append((current, current_heuristic))
                self.add_log(str(current) + " Heuristic: " + str(current_heuristic))
                if self.is_goal(current):
                    return self.solution_path(current), path
            T *= alpha
        return None, path

    solution, path = run()
    if solution:
        self.add_log("Solution found: " + str(solution))
        self.right_label.configure(text="Solution found: " + str(solution))
        for state, heuristic in path:
            self.draw_board(state)
            self.left_label.configure(text=f"State: {state}\nHeuristic: {heuristic}")
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")

def Genetic_Algorithm(self, start_node):
    import random

    def create_individual():
        individual = list(range(self.n))
        random.shuffle(individual)
        return individual

    def create_population(size):
        return [create_individual() for _ in range(size)]

    def fitness(individual):
        return self.n - self.heuristic(individual)

    def select(population):
        population.sort(key=fitness, reverse=True)
        return population[:len(population)//2]

    def crossover(parent1, parent2):
        point = random.randint(0, self.n - 1)
        child = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
        return child

    def mutate(individual):
        i, j = random.sample(range(self.n), 2)
        individual[i], individual[j] = individual[j], individual[i]

    def run():
        population_size = 100
        generations = 1000
        mutation_rate = 0.1

        population = create_population(population_size)
        path = []; self.add_log("---Path---")
        for gen in range(generations):
            population = select(population)
            next_generation = []
            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(population, 2)
                child = crossover(parent1, parent2)
                if random.random() < mutation_rate:
                    mutate(child)
                next_generation.append(child)
            population = next_generation
            best_individual = max(population, key=fitness)
            best_fitness = fitness(best_individual)
            path.append((best_individual, self.heuristic(best_individual)))
            self.add_log(str(best_individual) + " Heuristic: " + str(self.heuristic(best_individual)))
            if self.is_goal(best_individual):
                return self.solution_path(best_individual), path
        return None, path

    solution, path = run()
    if solution:
        self.add_log("Solution found: " + str(solution))
        self.right_label.configure(text="Solution found: " + str(solution))
        for state, heuristic in path:
            self.draw_board(state)
            self.left_label.configure(text=f"State: {state}\nHeuristic: {heuristic}")
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")

def Beam_Search(self, start_node):
    from queue import PriorityQueue
    from heapq import heapify

    class Node:
        def __init__(self, state, cost=0, heuristic=0, parent=None):
            self.state = state
            self.cost = cost
            self.heuristic = heuristic
            self.parent = parent

        def __lt__(self, other):
            return self.heuristic < other.heuristic

    def change_state(state):
        board_state = [-1] * self.n
        for (x, y) in state:
            board_state[x] = y
        return board_state

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
        beam_width = 5
        frontier = PriorityQueue()
        frontier.put(start_node)
        while True:
            if frontier.empty():
                return None, None, path
            current_level_nodes = []
            while not frontier.empty():
                current_level_nodes.append(frontier.get())
            next_level_nodes = []
            for current_node in current_level_nodes:
                path.append((current_node.state, current_node.cost, current_node.heuristic))
                self.add_log(str(current_node.state) + " Cost: " + str(current_node.cost) + " Heuristic: " + str(current_node.heuristic))
                if self.is_goal(current_node.state):
                    return self.solution(current_node), current_node, path
                for action, cost, heuristic in actions(current_node.state):
                    child_node = Node(action, cost + current_node.cost, heuristic, current_node)
                    next_level_nodes.append(child_node)
            next_level_nodes.sort(key=lambda x: x.heuristic)
            for node in next_level_nodes[:beam_width]:
                frontier.put(node)
    slt, result, path = run(start_node)
    if result:
        self.add_log("---Result---\n"+str(result.state) + " Cost: " + str(result.cost) + " Heuristic: " + str(result.heuristic))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="Cost: " + str(result.cost) + " Heuristic: " + str(result.heuristic))

        for i in path:
            self.draw_board(i[0], board='right')
            self.right_label.configure(text=f"State: {i[0]}\nCost: {i[1]}\nHeuristic: {i[2]}")
            self.update()
            self.after(50)
    else:
        self.add_log("No solution")
        self.right_label.configure(text="No solution")