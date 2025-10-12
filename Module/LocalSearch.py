import random, math, time

def calculate_total_heuristic(state):
    # Tính tổng heuristic của một trạng thái (tổng số cặp quân xe tấn công nhau)
    attacks = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i][0] == state[j][0] or state[i][1] == state[j][1]:
                attacks += 1
    return attacks

def Hill_Climbing(self, start_node):
    class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.heuristic = heuristic

    def get_neighbors(state):
        neighbors = []
        for i, (row, col) in enumerate(state):
            for new_col in range(self.n):
                if new_col != col:
                    neighbor_state = state[:]
                    neighbor_state[i] = (row, new_col)
                    # Sắp xếp để đảm bảo trạng thái là duy nhất và nhất quán
                    neighbor_state.sort(key=lambda x: x[0])
                    neighbors.append(neighbor_state)
        return neighbors
        
    def run(start_node):
        initial_state = []
        cols = list(range(self.n))
        for row in range(self.n):
            initial_state.append((row, random.randint(0, self.n - 1)))
        
        current_node = Node(initial_state, calculate_total_heuristic(initial_state))
        
        path = [(current_node.state, current_node.heuristic)]
        self.add_log("---Path---")
        self.add_log(f"{current_node.state}, Heuristic: {current_node.heuristic}")

        if self.is_goal(current_node.state):
            return current_node, path
        while True:
            neighbors_states = get_neighbors(current_node.state)
            if not neighbors_states:
                return None, path

            best_neighbor = None
            best_heuristic = current_node.heuristic

            for neighbor_state in neighbors_states:
                h = calculate_total_heuristic(neighbor_state)
                if h < best_heuristic:
                    best_heuristic = h
                    best_neighbor = Node(neighbor_state, h)
            if best_neighbor is None:
                return current_node, path 

            current_node = best_neighbor
            path.append((current_node.state, current_node.heuristic))
            self.add_log(f"{current_node.state}, Heuristic: {current_node.heuristic}")

    result, path = run(start_node)
    
    if result:
        self.add_log("---Result---\n"+str(result.state) + " Heuristic: " + str(result.heuristic))
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text="Heuristic: " + str(result.heuristic))

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Heuristic: " + str(i[1]))
            self.update()
            self.after(200)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def Simulated_Annealing(self, start_node):
    class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.heuristic = heuristic

    def get_neighbors(state):
        neighbors = []
        for i, (row, col) in enumerate(state):
            for new_col in range(self.n):
                if new_col != col:
                    neighbor_state = state[:]
                    neighbor_state[i] = (row, new_col)
                    # Sắp xếp để đảm bảo trạng thái là duy nhất và nhất quán
                    neighbor_state.sort(key=lambda x: x[0])
                    neighbors.append(neighbor_state)
        return neighbors

    def acceptance_probability(current_heuristic, neighbor_heuristic, temperature):
        if neighbor_heuristic < current_heuristic:
            return 1.0
        else:
            return math.exp((current_heuristic - neighbor_heuristic) / temperature)

    def run(start_node):
        initial_state = []
        cols = list(range(self.n))
        for row in range(self.n):
            initial_state.append((row, random.randint(0, self.n - 1)))
        
        current_node = Node(initial_state, calculate_total_heuristic(initial_state))
        
        path = [(current_node.state, current_node.heuristic)]
        self.add_log("---Path---")
        self.add_log(f"{current_node.state}, Heuristic: {current_node.heuristic}")

        if self.is_goal(current_node.state):
            return current_node, path

        temperature = 100.0
        alpha = 0.99
        min_temperature = 0.1

        while temperature > min_temperature:
            neighbors_states = get_neighbors(current_node.state)
            if not neighbors_states:
                return None, path

            next_state = random.choice(neighbors_states)
            next_heuristic = calculate_total_heuristic(next_state)
            ap = acceptance_probability(current_node.heuristic, next_heuristic, temperature)
            if ap > random.random():
                current_node = Node(next_state, next_heuristic)
                path.append((current_node.state, current_node.heuristic))
                self.add_log(f"{current_node.state}, Heuristic: {current_node.heuristic}")
                if self.is_goal(current_node.state):
                    return current_node, path
            temperature *= alpha
        return current_node, path
    
    result, path = run(start_node)
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
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def Genetic_Algorithm(self, start_node):
    class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.heuristic = heuristic # Đóng vai trò là Fitness-FN (heuristic càng thấp, fitness càng cao)

    def create_individual():
        individual = []
        cols = list(range(self.n))
        for row in range(self.n):
            individual.append((row, random.randint(0, self.n - 1)))
        return individual
    
    def tournament_selection(pop, k=5):
        # Đây là một cách triển khai RANDOM-SELECTION(population, FITNESS-FN)
        # Chọn k cá thể ngẫu nhiên và trả về cá thể tốt nhất trong số đó
        selection = random.sample(pop, k)
        selection.sort(key=lambda x: x.heuristic)
        return selection[0]

    def crossover(parent1, parent2):
        # Hàm REPRODUCE(x, y) trong giả mã
        n = len(parent1)
        crossover_point = random.randint(1, n - 1)
        # Sắp xếp cha mẹ theo hàng để đảm bảo tính nhất quán khi lai ghép
        p1_sorted = sorted(parent1, key=lambda x: x[0])
        p2_sorted = sorted(parent2, key=lambda x: x[0])
        child_state = p1_sorted[:crossover_point] + p2_sorted[crossover_point:]
        return child_state

    def mutate(individual, mutation_rate=0.1):
        # Hàm MUTATE(child) trong giả mã
        mutated_individual = list(individual)
        for i in range(len(mutated_individual)):
            if random.random() < mutation_rate:
                # Đổi vị trí cột của một quân xe ngẫu nhiên
                mutated_individual[i] = (mutated_individual[i][0], random.randint(0, self.n - 1))
        return mutated_individual

    def run(start_node):
        population_size = 100
        generations = 500
        mutation_rate = 0.1

        # Khởi tạo quần thể ban đầu
        population = [create_individual() for _ in range(population_size)]
        population_nodes = [Node(ind, calculate_total_heuristic(ind)) for ind in population]

        path = []
        self.add_log("---Path---")

        for generation in range(generations):
            # Sắp xếp để tìm cá thể tốt nhất trong thế hệ hiện tại để ghi log
            population_nodes.sort(key=lambda x: x.heuristic)
            best_individual = population_nodes[0]

            path.append((best_individual.state, best_individual.heuristic))
            self.add_log(f"{best_individual.state}")
            self.add_log(f"Generation {generation}: Best Heuristic = {best_individual.heuristic}")
            
            if self.is_goal(best_individual.state):
                return best_individual, path

            # Bắt đầu vòng lặp tạo thế hệ mới
            new_population_nodes = []

            for _ in range(population_size): # Lặp để tạo ra một quần thể mới có cùng kích thước
                # 1. Chọn lọc (Selection)
                parent1 = tournament_selection(population_nodes)
                parent2 = tournament_selection(population_nodes)

                # 2. Lai ghép (Crossover/Reproduce)
                child_state = crossover(parent1.state, parent2.state)

                # 3. Đột biến (Mutation) với một xác suất nhỏ
                if random.random() < mutation_rate:
                    child_state = mutate(child_state)
                
                child_node = Node(child_state, calculate_total_heuristic(child_state))
                new_population_nodes.append(child_node)

            population_nodes = new_population_nodes
        
        # Nếu hết số thế hệ mà chưa tìm ra giải pháp, trả về cá thể tốt nhất tìm được
        population_nodes.sort(key=lambda x: x.heuristic)
        return population_nodes[0], path
    
    result, path = run(start_node)
    
    if result:
        self.add_log("---Result---")
        final_message = f"Heuristic: {result.heuristic}"
        if result.heuristic == 0:
            final_message = "Giải pháp đã được tìm thấy!"

        self.add_log(f"Trạng thái: {result.state} với Heuristic: {result.heuristic}")
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text=final_message)

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Heuristic: " + str(i[1]))
            self.update()
            self.after(200)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")

def Beam(self, start_node):
    class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.heuristic = heuristic

    def create_individual():
        individual = []
        cols = list(range(self.n))
        for row in range(self.n):
            individual.append((row, random.randint(0, self.n - 1)))
        return individual

    def get_neighbors(state):
        neighbors = []
        for i, (row, col) in enumerate(state):
            for new_col in range(self.n):
                if new_col != col:
                    neighbor_state = state[:]
                    neighbor_state[i] = (row, new_col)
                    # Sắp xếp để đảm bảo trạng thái là duy nhất và nhất quán
                    neighbor_state.sort(key=lambda x: x[0])
                    neighbors.append(neighbor_state)
        return neighbors

    def run(start_node):
        beam_width = 5
        generations = 100

        # Khởi tạo quần thể ban đầu
        population = [create_individual() for _ in range(beam_width)]
        population_nodes = [Node(ind, calculate_total_heuristic(ind)) for ind in population]

        path = []
        self.add_log("---Path---")

        for generation in range(generations):
            # Sắp xếp để tìm cá thể tốt nhất trong thế hệ hiện tại để ghi log
            population_nodes.sort(key=lambda x: x.heuristic)
            best_individual = population_nodes[0]

            path.append((best_individual.state, best_individual.heuristic))
            self.add_log(f"{best_individual.state}")
            self.add_log(f"Generation {generation}: Best Heuristic = {best_individual.heuristic}")
            
            if self.is_goal(best_individual.state):
                return best_individual, path

            # Tạo danh sách các láng giềng của tất cả các cá thể trong quần thể hiện tại
            all_neighbors = []
            for node in population_nodes:
                neighbors_states = get_neighbors(node.state)
                for state in neighbors_states:
                    all_neighbors.append(Node(state, calculate_total_heuristic(state)))

            # Chọn beam_width cá thể tốt nhất từ tất cả các láng giềng
            all_neighbors.sort(key=lambda x: x.heuristic)
            population_nodes = all_neighbors[:beam_width]
        
        # Nếu hết số thế hệ mà chưa tìm ra giải pháp, trả về cá thể tốt nhất tìm được
        population_nodes.sort(key=lambda x: x.heuristic)
        return population_nodes[0], path
    
    result, path = run(start_node)
    if result:
        self.add_log("---Result---")
        final_message = f"Heuristic: {result.heuristic}"
        if result.heuristic == 0:
            final_message = "Giải pháp đã được tìm thấy!"

        self.add_log(f"Trạng thái: {result.state} với Heuristic: {result.heuristic}")
        self.place_rook(self.right_board_cells, self.change_state(result.state))
        self.right_label.configure(text=final_message)

        for i in path:
            self.place_rook(self.left_board_cells, self.change_state(i[0]))
            self.left_label.configure(text="Heuristic: " + str(i[1]))
            self.update()
            self.after(200)
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="Trạng thái: Không tìm thấy giải pháp!")
