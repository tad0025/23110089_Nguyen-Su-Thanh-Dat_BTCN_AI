import math

def Minimax(self, start_node):
    path = [] # Biến này lưu lại toàn bộ quá trình duyệt cây
    self.add_log("---Path---")

    def actions(state):
        next_row = len(state)
        if next_row >= self.n:
            return []
        
        valid_moves = []
        occupied_cols = {col for _, col in state}
        for col in range(self.n):
            if col not in occupied_cols:
                valid_moves.append(state + [(next_row, col)])
        return valid_moves

    def is_terminal(state):
        return len(state) == self.n or not actions(state)

    def utility(state):
        if self.is_goal(state):
            return 1
        return -1

    def max_value(state):
        path.append(state) # Thêm trạng thái vào path để ghi lại quá trình
        self.add_log(f"MAX evaluating: {state}")
        if is_terminal(state):
            return utility(state)
        
        v = -math.inf
        for move in actions(state):
            v = max(v, min_value(move))
        return v

    def min_value(state):
        path.append(state) # Thêm trạng thái vào path để ghi lại quá trình
        self.add_log(f"MIN evaluating: {state}")
        if is_terminal(state):
            return utility(state)
        
        v = math.inf
        for move in actions(state):
            v = min(v, max_value(move))
        return v

    # Tìm đường đi tối ưu
    solution_path = []
    current_state = start_node
    final_solution = None

    while not self.is_goal(current_state):
        solution_path.append(current_state)
        player_is_max = (len(current_state) % 2 == 0)
        
        moves = actions(current_state)
        if not moves:
            best_move = None
            break

        if player_is_max:
            scores = [min_value(move) for move in moves]
            best_score = max(scores)
            best_move = moves[scores.index(best_score)]
        else:
            scores = [max_value(move) for move in moves]
            best_score = min(scores)
            best_move = moves[scores.index(best_score)]
        
        current_state = best_move
    
    if self.is_goal(current_state):
        final_solution = current_state

    if final_solution:
        self.add_log("---Result---\n" + str(final_solution))
        self.place_rook(self.right_board_cells, self.change_state(final_solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="State: No solution found!")

    for step in path:
        self.place_rook(self.left_board_cells, self.change_state(step))
        self.update()
        self.after(50)

def Alpha_Beta(self, start_node):
    path = [] # Biến này lưu lại toàn bộ quá trình duyệt cây
    self.add_log("---Path---")

    def actions(state):
        next_row = len(state)
        if next_row >= self.n: return []
        valid_moves = []
        occupied_cols = {col for _, col in state}
        for col in range(self.n):
            if col not in occupied_cols:
                valid_moves.append(state + [(next_row, col)])
        return valid_moves

    def is_terminal(state):
        return len(state) == self.n or not actions(state)

    def utility(state):
        if self.is_goal(state): return 1
        return -1

    def max_value(state, alpha, beta):
        path.append(state) # Thêm trạng thái vào path để ghi lại quá trình
        self.add_log(f"MAX: {state}, alpha: {alpha}, beta: {beta}")
        if is_terminal(state): return utility(state)
        
        v = -math.inf
        for move in actions(state):
            v = max(v, min_value(move, alpha, beta))
            if v >= beta:
                self.add_log(f"  -> Pruning at MAX (v={v} >= beta={beta})")
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        path.append(state) # Thêm trạng thái vào path để ghi lại quá trình
        self.add_log(f"MIN: {state}, alpha: {alpha}, beta: {beta}")
        if is_terminal(state): return utility(state)
        
        v = math.inf
        for move in actions(state):
            v = min(v, max_value(move, alpha, beta))
            if v <= alpha:
                self.add_log(f"  -> Pruning at MIN (v={v} <= alpha={alpha})")
                return v
            beta = min(beta, v)
        return v

    # Tìm đường đi tối ưu
    current_state = start_node
    final_solution = None

    while not self.is_goal(current_state):
        moves = actions(current_state)
        if not moves:
            break
        
        scores = [min_value(move, -math.inf, math.inf) for move in moves]
        best_score = max(scores)
        current_state = moves[scores.index(best_score)]
        
    if self.is_goal(current_state):
        final_solution = current_state

    if final_solution:
        self.add_log("---Result---\n" + str(final_solution))
        self.place_rook(self.right_board_cells, self.change_state(final_solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="State: No solution found!")

    for step in path:
        self.place_rook(self.left_board_cells, self.change_state(step))
        self.update()
        self.after(50)