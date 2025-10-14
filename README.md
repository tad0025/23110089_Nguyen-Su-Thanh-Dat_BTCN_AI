# ♟️ BÁO CÁO BÀI TẬP CÁ NHÂN MÔN TRÍ TUỆ NHÂN TẠO 💡

---

## 1. THÔNG TIN CÁ NHÂN

* **Họ và tên:** Nguyễn Sư Thành Đạt
* **Mã số sinh viên:** 23110089
* **Môn học:** Trí tuệ Nhân tạo
* **Lớp:** ARIN330585_05CLC Buổi: Sáng thứ 2 - thứ 6, tiết 1 - 4

---

## 2. TỔNG QUAN VỀ BÀI TOÁN: N QUÂN XE (N-Rooks Problem)

### 2.1. Mô tả Bài toán

Bài toán đặt **N quân Xe** (Rooks) lên một bàn cờ **$N \times N$** (0 < N < 9)sao cho không có quân Xe nào có thể tấn công quân Xe khác.

* **Mục tiêu (Goal State):** Đặt N quân Xe sao cho mỗi hàng và mỗi cột chỉ có **đúng một** quân Xe. Điều này đảm bảo không có hai quân Xe nào nằm trên cùng một hàng hoặc cùng một cột.

### 2.2. Biểu diễn Trạng thái

Trạng thái của bài toán được biểu diễn dưới dạng một danh sách các bộ `(hàng, cột)` cho biết vị trí của các quân Xe đã được đặt.

* **Trạng thái Ban đầu:** Một danh sách rỗng `[]`, tương ứng với một bàn cờ trống.
* **Trạng thái Đích:** Một danh sách gồm N bộ `(hàng, cột)`, trong đó tất cả các giá trị `hàng` và tất cả các giá trị `cột` là riêng biệt, ví dụ: `[(0, 0), (1, 1), ..., (N-1, N-1)]`.

---

## 3. CẤU TRÚC GIAO DIỆN VÀ CHỨC NĂNG

### 3.1. Cấu Trúc Và Chức Năng

Ứng dụng được xây dựng bằng thư viện `customtkinter` của ngôn ngữ lập trình Python với giao diện hiện đại và trực quan.

1.  **Khung bên Trái:**
    * **Bảng điều khiển:**
        * **Combobox:** Cho phép chọn một trong các thuật toán đã triển khai.
        * **Nút "Giải bài toán":** Bắt đầu thực thi thuật toán đã chọn.
        * **Nút "Xóa":** Xóa các quân Xe khỏi bàn cờ.
    * **Bàn cờ "Các bước thực hiện":** Trực quan hóa quá trình tìm kiếm hoặc các bước đi của thuật toán.
2.  **Khung bên Phải:**
    * **Tùy chọn bàn cờ:** Cho phép người dùng nhập kích thước bàn cờ N x N (từ 1 đến 8).
    * **Bảng ghi log:** Hiển thị chi tiết các bước, trạng thái đã duyệt, và kết quả của thuật toán dưới dạng văn bản.
    * **Bàn cờ "Kết quả cuối cùng":** Hiển thị lời giải cuối cùng mà thuật toán tìm được.

### 3.2. Lưu ý về Mã nguồn và Hiển thị

* **Logic Sinh Trạng thái:** Các thuật toán tìm kiếm truyền thống (Uninformed, Informed, CSP) sinh trạng thái bằng cách đặt quân Xe theo thứ tự từng hàng, giúp giảm không gian tìm kiếm một cách hiệu quả.
* **Trực quan hóa:** Giao diện cập nhật từng bước đi của thuật toán trên bàn cờ bên trái và hiển thị kết quả cuối cùng ở bàn cờ bên phải, giúp người dùng dễ dàng theo dõi và so sánh.
* **Logging:** Mọi hành động, từ việc thử một trạng thái mới, quay lui, đến cắt tỉa (pruning), đều được ghi lại chi tiết trong ô log, cung cấp cái nhìn sâu sắc về cách hoạt động của từng thuật toán.
* **Chương trình có thể nhập bàn cờ $N \times N$ với N từ 1 -> 8. Vì nhanh và trực quan hơn thì em xin phép chèn ảnh động GIF ở bàn cờ $5 \times 5$, nếu thuật toán cho phép em sẽ quay ở bàn cờ $8 \times 8$**

---

## 4. CÁC THUẬT TOÁN ĐÃ TRIỂN KHAI

Mã nguồn đã triển khai một dải rộng các thuật toán, được phân loại rõ ràng và lựa chọn thông qua giao diện người dùng.

### 4.1. Nhóm Thuật Toán Tìm kiếm Không Có Thông Tin (Uninformed Search)

1.  **Breadth First Search (BFS):**
Thuật toán BFS thực hiện tìm kiếm theo chiều rộng, tức là nó sẽ duyệt qua tất cả các trạng thái (cách đặt quân xe) ở cùng một "cấp độ" trước khi đi xuống cấp độ sâu hơn. Trong bài toán này, "cấp độ" có thể hiểu là số lượng quân xe đã được đặt lên bàn cờ.
  * **Cấp 0:** Bàn cờ trống `[]`.
  * **Cấp 1:** Tất cả các trạng thái có 1 quân xe, ví dụ: `[(0, 0)]`, `[(0, 1)]`,...
  * **Cấp 2:** Tất cả các trạng thái có 2 quân xe, ví dụ: `[(0, 0), (1, 1)]`, `[(0, 0), (1, 2)]`,...
  * ... và cứ thế tiếp tục.
Cách tiếp cận này đảm bảo rằng nếu có lời giải, BFS sẽ tìm ra lời giải có số bước đi (số quân xe) ít nhất.
   ![BFS](./GIF/BFS.gif)
3.  **Depth First Search (DFS)** | Tìm lời giải nhanh (không đảm bảo tối ưu) | Ưu tiên đi sâu vào một nhánh của cây tìm kiếm. |
| **Uniform Cost Search (UCS)** | Tìm đường đi có **tổng chi phí thấp nhất** | Mở rộng nút có chi phí đường đi `g(n)` thấp nhất từ điểm xuất phát. |
| **Depth Limited Search (DLS)** | DFS với giới hạn độ sâu | Ngăn chặn việc đi vào các nhánh vô hạn. |
| **Iterative Deepening Search (IDS)** | Kết hợp DLS với giới hạn độ sâu tăng dần | Hoàn chỉnh và tối ưu về số bước như BFS nhưng tiết kiệm không gian hơn. |

### 4.2. Nhóm Thuật toán Tìm kiếm có Thông tin (Informed Search)

| Thuật toán | Hàm Heuristic (`h(n)`) | Hàm Đánh giá |
| :--- | :--- | :--- |
| **Greedy Search** | Ước tính chi phí từ trạng thái hiện tại đến đích. | `f(n) = h(n)` |
| **A\* Search** | Ước tính chi phí từ trạng thái hiện tại đến đích. | `f(n) = g(n) + h(n)` (với `g(n)` là chi phí từ đầu đến hiện tại) |

### 4.3. Nhóm Thuật toán Tìm kiếm Cục bộ (Local Search)

Các thuật toán này hoạt động trên một trạng thái hoàn chỉnh và cố gắng cải thiện nó.

| Thuật toán | Mô tả |
| :--- | :--- |
| **Hill Climbing** | Luôn di chuyển đến trạng thái lân cận tốt hơn (heuristic thấp hơn). Dễ bị kẹt ở cực tiểu cục bộ. |
| **Simulated Annealing** | Cải tiến Hill Climbing, cho phép chấp nhận các bước đi tồi hơn với một xác suất nhất định để thoát khỏi cực tiểu cục bộ. |
| **Genetic Algorithm** | Thuật toán tiến hóa: sử dụng các phép lai (crossover) và đột biến (mutation) để tiến hóa một quần thể các lời giải. |
| **Beam Search** | Biến thể của BFS, chỉ giữ lại `k` trạng thái tốt nhất ở mỗi bước để khám phá tiếp. |

### 4.4. Nhóm Bài toán Thỏa mãn Ràng buộc (CSP)

| Thuật toán | Kỹ thuật áp dụng | Ràng buộc chính |
| :--- | :--- | :--- |
| **Backtracking Search** | Gán giá trị lần lượt cho từng biến (hàng) và quay lui nếu vi phạm ràng buộc. | Mỗi quân Xe phải ở một cột khác nhau. |
| **Forward Checking** | Cải tiến Backtracking: Sau khi gán biến, loại bỏ các giá trị không tương thích khỏi miền của các biến chưa được gán. | Mỗi quân Xe phải ở một cột khác nhau. |
| **AC-3 (Arc Consistency 3)** | Áp dụng kỹ thuật nhất quán cung để lọc miền giá trị của các biến trước và trong khi tìm kiếm để giảm không gian tìm kiếm. | Mỗi quân Xe phải ở một cột khác nhau. |

### 4.5. Nhóm Môi trường Phức tạp (Complex Environment Search)

| Thuật toán | Loại môi trường | Mục tiêu |
| :--- | :--- | :--- |
| **And-Or Search** | Môi trường không tất định (Non-deterministic) | Tìm một kế hoạch (một cây con của không gian trạng thái) đảm bảo đến được đích dù kết quả hành động là gì. |
| **Belief State Search** | Môi trường không quan sát được hoàn toàn (Partially Observable) | Duy trì một tập hợp các trạng thái có thể (belief state) và tìm kiếm trên không gian của các belief state này. |
| **Partially Observable Search** | Tương tự Belief State, tập trung vào việc cập nhật belief state dựa trên các quan sát. | Tìm kiếm một chuỗi hành động dẫn đến trạng thái đích. |

### 4.6. Nhóm Môi trường Đối kháng (Game Search)

| Thuật toán | Loại môi trường | Mục tiêu |
| :--- | :--- | :--- |
| **Minimax** | Môi trường đối kháng (2 người chơi, zero-sum) | Lựa chọn nước đi để **tối đa hóa** giá trị ở trạng thái cuối cùng, giả định đối thủ sẽ **tối thiểu hóa** giá trị đó. |
| **Alpha-Beta Pruning** | Cải tiến Minimax | Cắt tỉa các nhánh của cây tìm kiếm mà chắc chắn sẽ không được chọn, giúp tăng tốc độ đáng kể. |
