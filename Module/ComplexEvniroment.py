from collections import deque

def And_Or(self, start_node):
    path = []
    self.add_log("---Path---")

    def or_search(state, goals):
        if not goals:
            return state if self.is_goal(state) else None

        if tuple(map(tuple, state)) in explored:
            return None
        explored.add(tuple(map(tuple, state)))
        
        current_goal = goals[0]
        remaining_goals = goals[1:]
        
        row_to_place = len(state)
        
        # OR nodes: try placing a rook in any available column for the current row
        for col in range(self.n):
            if col not in [y for x, y in state]:
                new_state = state + [(row_to_place, col)]
                path.append(new_state)
                self.add_log(f"Trying state: {new_state}")
                
                # AND node: the new state must lead to a solution for all remaining goals
                solution = and_search(new_state, remaining_goals)
                if solution is not None:
                    return solution
        return None

    def and_search(state, goals):
        if not goals:
            return state if self.is_goal(state) else None
        
        # All subproblems (goals) must be solved
        solution = or_search(state, goals)
        if solution is not None:
            return solution
        return None

    # The goal is to place a rook in each row from 0 to n-1
    goals = [f'place_in_row_{i}' for i in range(self.n)]
    explored = set()
    
    solution = or_search(start_node, goals)

    if solution:
        self.add_log("---Result---\n" + str(solution))
        self.place_rook(self.right_board_cells, self.change_state(solution))
        self.right_label.configure(text="State: Solution Found!")
    else:
        self.add_log("No solution found.")
        self.right_label.configure(text="State: No solution found!")

    for i in path:
        self.place_rook(self.left_board_cells, self.change_state(i))
        self.update()
        self.after(50)

def Partially_Observable(self, start_node):
    """
    Tìm kiếm trong môi trường quan sát không đầy đủ.
    Agent không biết trạng thái thật — chỉ quan sát được một phần môi trường.
    Giải pháp: duy trì và cập nhật belief state (tập hợp trạng thái có thể có).
    """
    self.add_log("---Path---")
    self.add_log("Khởi tạo tìm kiếm trong môi trường quan sát không đầy đủ...")

    # Khởi tạo belief state ban đầu: chỉ biết rằng trạng thái ban đầu có thể là rỗng
    initial_belief = frozenset([frozenset(start_node)])
    frontier = deque([(initial_belief, [start_node])])
    explored = {initial_belief}
    path_log = []

    def get_possible_observations(state):
        """
        Sinh ra các quan sát có thể có — ví dụ: vị trí có thể đặt quân xe
        Ở đây ta giả định agent chỉ quan sát được hàng hiện tại (row) mình đang đặt.
        """
        row = len(state)
        if row >= self.n:
            return []
        available_cols = [j for j in range(self.n) if all(y != j for (_, y) in state)]
        return [(row, col) for col in available_cols]

    while frontier:
        belief_state, path = frontier.popleft()
        representative = list(list(belief_state)[0]) if belief_state else []
        path_log.append(representative)
        self.add_log(f"Đang xét Belief State gồm {len(belief_state)} trạng thái khả dĩ.")

        # Kiểm tra xem có trạng thái nào trong belief là trạng thái đích không
        for s in belief_state:
            state = list(s)
            if self.is_goal(state):
                self.add_log("---Result---\n" + str(state))
                self.place_rook(self.right_board_cells, self.change_state(state))
                self.right_label.configure(text="State: Solution Found!")
                for i in path_log:
                    self.place_rook(self.left_board_cells, self.change_state(i))
                    self.update()
                    self.after(50)
                return

        # Sinh ra các belief state kế tiếp dựa trên các quan sát khả dĩ
        possible_next_beliefs = set()
        for s in belief_state:
            state = list(s)
            for obs in get_possible_observations(state):
                new_state = state + [obs]
                possible_next_beliefs.add(frozenset(new_state))

        if not possible_next_beliefs:
            continue

        successor_belief = frozenset(possible_next_beliefs)
        if successor_belief not in explored:
            explored.add(successor_belief)
            new_path = path + [list(list(successor_belief)[0])]
            frontier.append((successor_belief, new_path))
            self.add_log(f"Tạo Belief State mới với {len(successor_belief)} trạng thái khả dĩ.")

    self.add_log("Không tìm thấy giải pháp.")
    self.right_label.configure(text="State: No solution found.")
    for i in path_log:
        self.place_rook(self.left_board_cells, self.change_state(i))
        self.update()
        self.after(50)


def Belief_State(self, start_node):
    """
    Belief-State Search: tìm kiếm trên không gian các belief states.
    Mỗi belief state là một tập hợp các trạng thái có thể có.
    """
    self.add_log("---Path---")
    self.add_log("Khởi tạo tìm kiếm theo trạng thái niềm tin (Belief-State Search)...")

    # Khởi tạo belief state ban đầu: chỉ có trạng thái rỗng
    initial_belief = frozenset([frozenset(start_node)])
    frontier = deque([(initial_belief, [start_node])])
    explored = {initial_belief}
    path_log = []

    def successor_beliefs(belief_state):
        """
        Sinh ra các belief states kế tiếp bằng cách thêm 1 quân xe hợp lệ
        vào tất cả các trạng thái có thể trong belief hiện tại.
        """
        next_beliefs = set()
        for s in belief_state:
            state = list(s)
            row = len(state)
            if row >= self.n:
                continue
            occupied_cols = {y for _, y in state}
            for col in range(self.n):
                if col not in occupied_cols:
                    new_state = state + [(row, col)]
                    next_beliefs.add(frozenset(new_state))
        return [frozenset(next_beliefs)] if next_beliefs else []

    while frontier:
        belief_state, path = frontier.popleft()
        representative = list(list(belief_state)[0]) if belief_state else []
        path_log.append(representative)
        self.add_log(f"Đang xét Belief State gồm {len(belief_state)} trạng thái khả dĩ.")

        # Kiểm tra xem có trạng thái nào trong belief là trạng thái đích
        for s in belief_state:
            state = list(s)
            if self.is_goal(state):
                self.add_log("---Result---\n" + str(state))
                self.place_rook(self.right_board_cells, self.change_state(state))
                self.right_label.configure(text="State: Solution Found!")
                for i in path_log:
                    self.place_rook(self.left_board_cells, self.change_state(i))
                    self.update()
                    self.after(50)
                return

        # Mở rộng các belief state kế tiếp
        for next_belief in successor_beliefs(belief_state):
            if next_belief not in explored:
                explored.add(next_belief)
                new_path = path + [list(list(next_belief)[0])]
                frontier.append((next_belief, new_path))
                self.add_log(f"Tạo Belief State mới với {len(next_belief)} trạng thái khả dĩ.")

    self.add_log("Không tìm thấy giải pháp.")
    self.right_label.configure(text="State: No solution found.")
    for i in path_log:
        self.place_rook(self.left_board_cells, self.change_state(i))
        self.update()
        self.after(50)