from collections import deque

def Backtracking(self, start_node):
    path = []
    self.add_log("---Path---")
    self.add_log("Initial State: []")

    def backtrack_recursive(current_placement):
        path.append(current_placement)
        self.add_log(f"Trying: {current_placement}")
        if self.is_goal(current_placement):
            return current_placement
        next_row = len(current_placement)
        
        for col in range(self.n):
            if col not in [c for r, c in current_placement]:
                new_placement = current_placement + [(next_row, col)]
                result = backtrack_recursive(new_placement)
                if result is not None:
                    return result
        
        self.add_log(f"Backtracking from: {current_placement}")
        path.append(current_placement) # <-- DÒNG BỊ LỖI ĐÃ ĐƯỢC XÓA BỎ
        return None
    
    solution = backtrack_recursive(start_node)
    if solution:
        self.add_log("---Result---")
        self.add_log(f"Solution Found: {solution}")
        self.place_rook(self.right_board_cells, self.change_state(solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("---Result---")
        self.add_log("No solution found.")
        self.right_label.configure(text="State: No solution found!")

    for step in path:
        self.place_rook(self.left_board_cells, self.change_state(step))
        self.update()
        self.after(50)

def Forward_Checking(self, start_node):
    path = []
    self.add_log("---Path---")
    initial_domains = {row: list(range(self.n)) for row in range(self.n)}
    self.add_log(f"Initial Domains: {initial_domains}")

    def forward_check_recursive(current_placement, domains):
        path.append(current_placement)
        self.add_log(f"Current Placement: {current_placement}")
        if self.is_goal(current_placement):
            return current_placement

        next_row = len(current_placement)
        for col in domains[next_row]:
            new_placement = current_placement + [(next_row, col)]
            new_domains = {r: list(d) for r, d in domains.items()}
            for future_row in range(next_row + 1, self.n):
                if col in new_domains[future_row]:
                    new_domains[future_row].remove(col)

            self.add_log(f"-> Trying ({next_row},{col}). Pruned domains: {new_domains}")
            is_valid = all(new_domains[r] for r in range(next_row + 1, self.n))

            if is_valid:
                result = forward_check_recursive(new_placement, new_domains)
                if result is not None:
                    return result

        self.add_log(f"Backtracking from: {current_placement}")
        return None
    
    solution = forward_check_recursive(start_node, initial_domains)
    if solution:
        self.add_log("---Result---")
        self.add_log(f"Solution Found: {solution}")
        self.place_rook(self.right_board_cells, self.change_state(solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("---Result---")
        self.add_log("No solution found.")
        self.right_label.configure(text="State: No solution found!")
        
    for step in path:
        self.place_rook(self.left_board_cells, self.change_state(step))
        self.update()
        self.after(100)
        
def AC3(self, start_node):
    self.add_log("---AC-3 Preprocessing---")
    variables = list(range(self.n))
    domains = {i: list(range(self.n)) for i in variables}
    self.add_log(f"Initial Domains: {domains}")
    arc_queue = deque([(i, j) for i in variables for j in variables if i != j])

    def revise(xi, xj):
        revised = False
        # Tạo một bản sao của domains[xi] để lặp qua, tránh lỗi khi xóa phần tử
        for x_val in list(domains[xi]):
            # Kiểm tra xem có giá trị y_val nào trong domains[xj] thỏa mãn ràng buộc (khác x_val) không
            if not any(x_val != y_val for y_val in domains[xj]):
                domains[xi].remove(x_val)
                revised = True
        return revised
        
    while arc_queue:
        (xi, xj) = arc_queue.popleft()
        self.add_log(f"Revising arc: ({xi}, {xj})")
        if revise(xi, xj):
            if not domains[xi]:
                self.add_log("---Result---")
                self.add_log("No solution found (domain wiped out by AC-3).")
                self.right_label.configure(text="State: No solution (AC-3 failure)!")
                return
            # Thêm lại các cung liên quan đến xi
            for xk in variables:
                if xk != xi and xk != xj:
                    arc_queue.append((xk, xi))
        self.add_log(f"Domains after revision: {domains}")

    self.add_log("---AC-3 Finished. Starting Backtracking Search---")
    
    path = []

    def backtrack_on_pruned_domains(current_placement):
        path.append(current_placement)
        
        if self.is_goal(current_placement):
            return current_placement

        next_row = len(current_placement)
        for col in domains[next_row]:
            if col not in [c for r, c in current_placement]:
                new_placement = current_placement + [(next_row, col)]
                result = backtrack_on_pruned_domains(new_placement)
                if result is not None:
                    return result
        
        return None

    solution = backtrack_on_pruned_domains(start_node)
    
    if solution:
        self.add_log("---Result---")
        self.add_log(f"Solution Found: {solution}")
        self.place_rook(self.right_board_cells, self.change_state(solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("---Result---")
        self.add_log("No solution found after AC-3.")
        self.right_label.configure(text="State: No solution found!")
        
    for step in path:
        self.place_rook(self.left_board_cells, self.change_state(step))
        self.update()
        self.after(50)