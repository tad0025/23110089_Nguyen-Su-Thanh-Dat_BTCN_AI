import customtkinter as ctk
from Module.UninformedSearch import *
from Module.InformedSearch import *
from Module.LocalSearch import *
from Module.ComplexEvniroment import *
from Module.CSP import *

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

CELL_SIZE = 60
LIGHT_COLOR = "#FFFFFF"  # Trắng
DARK_COLOR = "#333333"   # Đen xám nhẹ
ROOK_SYMBOL = "♖"
BACKGROUND_COLOR = "#E7D3B0"  # Màu nền chính
algorithms_func = {
    "Uninformed Search --- Breadth First Search": BFS,
    "Uninformed Search --- Depth First Search": DFS,
    "Uninformed Search --- Uniform Cost Search": UCS,
    "Uninformed Search --- Depth Limited Search": DLS,
    "Uninformed Search --- Iterative Deepening Search": IDS,
    "Informed Search --- Greedy Search": Greedy,
    "Informed Search --- A* Search": A_Star,
    "Local Search --- Hill Climbing": Hill_Climbing,
    "Local Search --- Simulated Annealing": Simulated_Annealing,
    "Local Search --- Genetic Algorithm": Genetic_Algorithm,
    "Local Search --- Beam Search": Beam,
    "Complex Environment Search --- And Or Search": And_Or,
    "Complex Environment Search --- Belief State Search": Belief_State,
    "Complex Environment Search --- Partially Observable Search": Partially_Observable,
    "CSP --- Backtracking Search": Backtracking,
    "CSP --- Forward Checking": Forward_Checking,
    "CSP --- AC-3": AC3
}
algorithms = list(algorithms_func.keys())

class EightRooksApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bài toán 8 quân xe (8-Rooks Problem)")
        self.geometry("1300x650")
        self.resizable(False, False)
        self.n = 8  # Kích thước mặc định của bàn cờ NxN

        # 🔹 Tạo layout chính gồm 2 cột: trái và phải (đều co giãn)
        self.grid_columnconfigure(0, weight=1)  # Cột trái co giãn
        self.grid_columnconfigure(1, weight=1)  # Cột phải co giãn
        self.grid_rowconfigure(0, weight=1)

        # 🔹 Frame bên trái
        left_main_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        left_main_frame.grid(row=0, column=0, sticky="nsew")

        # 🔹 Frame bên phải
        right_extra_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        right_extra_frame.grid(row=0, column=1, sticky="nsew")

        # --- Frame chứa các điều khiển (combobox, button) ---
        control_frame = ctk.CTkFrame(left_main_frame, fg_color=BACKGROUND_COLOR)
        control_frame.pack(pady=20, padx=10, fill="x")

        label = ctk.CTkLabel(control_frame, text="Chọn thuật toán:", font=("Arial", 16, "bold"))
        label.pack(side="left", padx=10)

        self.algorithm_combo = ctk.CTkComboBox(
            control_frame,
            values=algorithms,
            font=("Arial", 16, "bold"),
            dropdown_font=("Arial", 15),
            button_color="#C8A66A",        # màu nút xổ xuống
            button_hover_color="#B38B6D",  # màu khi hover vào nút
            dropdown_fg_color="#FFFFFF",   # 🌟 màu nền của danh sách xổ xuống
            dropdown_hover_color="#E6CFA8",# 🌟 màu nền khi rê chuột vào item
            dropdown_text_color="black"    # 🌟 màu chữ trong danh sách xổ xuống
        )
        self.algorithm_combo.pack(side="left", padx=10, fill="x", expand=True)
        self.algorithm_combo.set(algorithms[0]) # Mặc định chọn

        solve_button = ctk.CTkButton(
            control_frame, 
            text="Giải bài toán", 
            command=self.solve_and_display,
            font=("Arial", 16, "bold")
        )
        solve_button.pack(side="left", padx=10)

        clear_button = ctk.CTkButton(
            control_frame,
            text="Xóa",
            command=self.clear_board,
            font=("Arial", 16, "bold")
        )
        clear_button.pack(side="left", padx=10)

        # --- Frame chứa 2 bàn cờ ---
        boards_frame = ctk.CTkFrame(left_main_frame, fg_color=BACKGROUND_COLOR)
        boards_frame.pack(fill="both", expand=True)
        boards_frame.grid_columnconfigure((0, 1), weight=1)
        boards_frame.grid_rowconfigure(0, weight=1)

        # --- Tạo bàn cờ bên trái (Initial State) ---
        self.left_board_frame = ctk.CTkFrame(boards_frame, fg_color=BACKGROUND_COLOR)
        self.left_board_frame.grid(row=0, column=0, padx=10, sticky="nsew")
        left_title_label = ctk.CTkLabel(
            self.left_board_frame,
            text="Các bước thực hiện",
            font=("Arial", 16, "bold")
        )
        left_title_label.pack(pady=(5, 5))
        self.left_board_grid = ctk.CTkFrame(self.left_board_frame)
        self.left_board_grid.pack()
        self.left_board_cells = self.create_board_ui(self.left_board_grid)
        self.left_label = ctk.CTkLabel(self.left_board_frame, text="Trạng thái: -", font=("Arial", 16))
        self.left_label.pack(pady=5)

        # --- Tạo bàn cờ bên phải (Solution) ---
        self.right_board_frame = ctk.CTkFrame(boards_frame, fg_color=BACKGROUND_COLOR)
        self.right_board_frame.grid(row=0, column=1, padx=10, sticky="nsew")
        right_title_label = ctk.CTkLabel(
            self.right_board_frame,
            text="Kết quả cuối cùng",
            font=("Arial", 16, "bold")
        )
        right_title_label.pack(pady=(5, 5))
        self.right_board_grid = ctk.CTkFrame(self.right_board_frame)
        self.right_board_grid.pack()
        self.right_board_cells = self.create_board_ui(self.right_board_grid)
        self.right_label = ctk.CTkLabel(self.right_board_frame, text="Trạng thái: -", font=("Arial", 16))
        self.right_label.pack(pady=5)

        # Danh sách để lưu các widget quân xe đã vẽ để dễ dàng xóa đi
        self.rook_widgets = []

        # frame bên phải (Extra Information)
        choose_frame = ctk.CTkFrame(right_extra_frame, fg_color=BACKGROUND_COLOR)
        choose_frame.pack(pady=20, padx=10, fill="x")

        label = ctk.CTkLabel(
            choose_frame,
            text="Nhập số ô bàn cờ NxN (lưu ý: N từ 1-8)",
            font=("Arial", 16, "bold"),
            wraplength=250  # 👈 Giới hạn chiều rộng 250px, tự xuống dòng
        )
        label.pack(side="top", padx=10, fill="x", expand=True)

        self.entry_n = ctk.CTkEntry(
            choose_frame,
            width=120,
            height=35,
            font=("Arial", 14),
            corner_radius=10
        )
        self.entry_n.pack(pady=10)
        self.entry_n.insert(0, "8")
        self.entry_n.bind("<Return>", lambda event: self.solve_and_display())

        self.note_label = ctk.CTkLabel(
            choose_frame,
            text="Chưa chọn thuật toán",
            font=("Arial", 16, "bold"),
            wraplength=250  # 👈 Giới hạn chiều rộng 250px, tự xuống dòng
        )
        self.note_label.pack(side="top")

        # 🔹 Frame chứa log (đặt ở bên phải)
        log_frame = ctk.CTkFrame(right_extra_frame, fg_color=BACKGROUND_COLOR)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # 🔹 Textbox ghi log (có thanh cuộn)
        self.log_textbox = ctk.CTkTextbox(log_frame, wrap="word", font=("Consolas", 14))  # wrap="word" để xuống dòng tự nhiên
        self.log_textbox.pack(fill="both", expand=True, side="left")

    def create_board_ui(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        board_cells = []
        for row in range(self.n):
            row_cells = []
            for col in range(self.n):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                cell = ctk.CTkFrame(
                    parent_frame,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    fg_color=color,
                    corner_radius=0,
                    border_width=1,
                    border_color="black"
                )
                cell.grid(row=row, column=col)
                cell.grid_propagate(False) 
                row_cells.append(cell)
            board_cells.append(row_cells)
        return board_cells

    def place_rook(self, board_cells, state):
        for i in range(len(state)):
            for j in range(len(state)):
                cell = board_cells[i][j]
                if state[i][j] == 1:
                    if not cell.winfo_children():  
                        rook_label = ctk.CTkLabel(
                            board_cells[i][j],
                            text=ROOK_SYMBOL,
                            font=("Segoe UI Symbol", int(CELL_SIZE * 0.8)),
                            text_color="red"
                        )
                        rook_label.place(relx=0.5, rely=0.5, anchor="center")
                        self.rook_widgets.append(rook_label)
                else:
                    if cell.winfo_children():
                        self.rook_widgets.remove(cell.winfo_children()[0])
                        cell.winfo_children()[0].destroy()

    def clear_board(self):
        for widget in self.rook_widgets:
            widget.destroy()
        self.rook_widgets.clear()

    def solve_and_display(self):
        n_value = self.entry_n.get()
        if not n_value.isdigit() or not (1 <= int(n_value) <= 8):
            self.note_label.configure(text="Trạng thái: Vui lòng nhập N hợp lệ (1-8).")
            return
        self.n = int(n_value)
        self.clear_board()
        self.left_board_cells = self.create_board_ui(self.left_board_grid)
        self.right_board_cells = self.create_board_ui(self.right_board_grid)

        self.note_label.configure(text="Trạng thái: Đang xử lý...")
        self.log_textbox.delete("1.0", "end")
        self.add_log(f"Đang sử dụng thuật toán {self.algorithm_combo.get()}")
        self.update()

        initial_board = []
        solve_function = algorithms_func.get(self.algorithm_combo.get())
        solve_function(self, initial_board)
        self.note_label.configure(text="Trạng thái: Hoàn thành!")
    
    def is_goal(self, state):
        if len(state) != self.n: return False

        rows = set(); cols = set()
        for (x, y) in state:
            if x in rows or y in cols: return False
            rows.add(x); cols.add(y)
        
        return True
    
    def change_state(self, state):
        a = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for (x, y) in state: a[x][y] = 1
        return a
    
    def add_log(self, message: str):
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.update_idletasks()