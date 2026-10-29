# Kịch bản Demo & Báo cáo Thuyết trình: Study Planner CLI (Team T-W3)

- **Đề tài**: Tích hợp công cụ quản lý lịch học Study Planner CLI
- **Nhóm thực hiện**: Team T-W3 (Team 07)
- **Người thuyết trình (Presenter)**: Lý Tuấn Kiệt (MSSV: 25125022 — GitHub: `@kiethm07`)
- **Tài liệu tham chiếu**: [shared/study_planner/README.md](../shared/study_planner/README.md)

---

## 1. Mục tiêu bài thuyết trình

1. Trình bày kiến trúc phần mềm hướng module hóa và quy trình tích hợp liên tục (CI/CD) của nhóm.
2. Minh họa trực tiếp (Live Demo) hoạt động của CLI `shared.study_planner` trên terminal.
3. Làm nổi bật các tính năng mở rộng:
   - Phân bổ lịch học theo thuật toán tham lam (Greedy).
   - Thống kê phân tích dữ liệu chuyên sâu với `Counter` và `defaultdict` (`--stats`).
   - Khả năng xuất dữ liệu đa định dạng Markdown và JSON (`--output`).
   - Xử lý lỗi an toàn không làm crash chương trình hoặc in stack trace ra người dùng.

---

## 2. Kế hoạch Slides & Cấu trúc thời gian (15 phút)

| Phần | Thời lượng | Nội dung chính | Người phụ trách / Slide |
| :---: | :---: | :--- | :--- |
| **Phần 1** | 2 phút | Giới thiệu thành viên, bảng phân công nhiệm vụ và mục tiêu sản phẩm. | Slide 1 – 2 |
| **Phần 2** | 3 phút | Kiến trúc Pipeline dữ liệu, hợp đồng dữ liệu (`Task`, `Block`) và cơ chế tích hợp. | Slide 3 – 4 |
| **Phần 3** | 6 phút | **Live Demo CLI**: Thực thi 5 kịch bản thực tế trên terminal. | Live Terminal |
| **Phần 4** | 2 phút | Đảm bảo chất lượng (QA/QC): Kết quả kiểm thử E2E và linter tự động trên CI. | Slide 5 |
| **Phần 5** | 2 phút | Tổng kết và giải đáp thắc mắc (Q&A). | Slide 6 |

---

## 3. Kịch bản Live Demo chi tiết từng bước (Step-by-Step Script)

> **Lưu ý cho Presenter**: Đảm bảo mở terminal tại thư mục gốc của repository `python-bootcamp`.

### Bước chuẩn bị
```bash
# Kiểm tra môi trường và file mẫu
git status
ls samples/
```

---

### Kịch bản 1: Thực thi cơ bản & thuật toán phân bổ (Basic Allocation)
- **Mục đích**: Chứng minh khả năng đọc dữ liệu CSV, xếp thứ tự ưu tiên và phân bổ giờ học theo thuật toán tham lam.
- **Lời dẫn Presenter**: *"Đầu tiên, chúng em chạy chương trình với file `samples/tasks.csv` và quỹ thời gian học là 8 giờ."*
- **Lệnh thực thi**:
  ```bash
  python -m shared.study_planner samples/tasks.csv --hours 8
  ```
- **Điểm nhấn cần giải thích**:
  - Task `DS exam` có `importance=5` được ưu tiên xếp trước và phân bổ đủ 6.0 giờ.
  - Task `Assignment` nhận 1.5 giờ còn lại.
  - Tổng số giờ phân bổ là 7.5h / 8.0h khả dụng.

---

### Kịch bản 2: Dữ liệu thực tế và tham số ngày mốc (`--today`)
- **Mục đích**: Kiểm tra với bộ dữ liệu mở rộng (`samples/tasks_extended.csv`) gồm nhiều môn học, độ ưu tiên từ 1-5 và các hạn nộp khác nhau.
- **Lời dẫn Presenter**: *"Với bộ dữ liệu thực tế gồm 7 môn học, chúng ta có thể truyền tham số `--today` để hệ thống tính toán số ngày còn lại đến deadline so với ngày chỉ định."*
- **Lệnh thực thi**:
  ```bash
  python -m shared.study_planner samples/tasks_extended.csv --hours 12 --today 2026-10-28
  ```
- **Điểm nhấn cần giải thích**:
  - Những môn thi gần ngày 2026-10-28 và có `importance=5` được xếp lên đầu bảng.
  - Các môn có deadline xa hoặc độ quan trọng thấp hơn sẽ được xếp sau và cắt giảm nếu hết giờ.

---

### Kịch bản 3: Phân tích thống kê chuyên sâu (`--stats`)
- **Mục đích**: Trình diễn tính năng thống kê phân bổ được xây dựng bằng `collections.Counter` và `collections.defaultdict`.
- **Lời dẫn Presenter**: *"Khi người dùng muốn nắm tổng quan cơ cấu thời gian học tập, cờ `--stats` sẽ tổng hợp tỷ lệ phần trăm theo từng mức độ quan trọng."*
- **Lệnh thực thi**:
  ```bash
  python -m shared.study_planner samples/tasks_extended.csv --hours 10 --stats
  ```
- **Kết quả quan sát**:
  - Hiển thị môn học chiếm nhiều thời gian nhất (Top Task).
  - Tỷ trọng thời gian phân bổ cho Level 5, Level 4... kèm phần trăm tương ứng.

---

### Kịch bản 4: Xuất kế hoạch ra Markdown & JSON (`--output`)
- **Mục đích**: Minh họa khả năng tương thích của kết quả đầu ra với các hệ thống khác hoặc ghi chú cá nhân.
- **Lời dẫn Presenter**: *"Kết quả học tập có thể được xuất trực tiếp ra Markdown để đưa vào Obsidian/Notion hoặc file JSON để truyền vào API khác."*
- **Lệnh thực thi**:
  ```bash
  # 1. Xuất ra Markdown
  python -m shared.study_planner samples/tasks_extended.csv --hours 8 --output output/demo_plan.md

  # 2. Xuất ra JSON
  python -m shared.study_planner samples/tasks_extended.csv --hours 8 --output output/demo_plan.json
  ```
- **Kiểm tra file xuất**:
  ```bash
  head -n 20 output/demo_plan.md
  head -n 25 output/demo_plan.json
  ```

---

### Kịch bản 5: Xử lý ngoại lệ an toàn (Graceful Error Handling)
- **Mục đích**: Chứng minh hệ thống xử lý lỗi sạch, trả về exit code `1` và không làm lộ Python traceback khó chịu cho người dùng.
- **Lời dẫn Presenter**: *"Tính năng bảo vệ dữ liệu và xử lý lỗi được thiết kế để bắt mọi tình huống đầu vào sai lệch."*

1. **Trường hợp file không tồn tại**:
   ```bash
   python -m shared.study_planner samples/nonexistent.csv --hours 4
   # Kỳ vọng: Thông báo lỗi rõ ràng, exit code 1
   ```
2. **Trường hợp dữ liệu CSV bị lỗi định dạng (`tasks_bad.csv`)**:
   ```bash
   python -m shared.study_planner samples/tasks_bad.csv --hours 4
   # Kỳ vọng: Báo lỗi định dạng dòng dữ liệu mà không văng traceback
   ```
3. **Trường hợp tham số số giờ không hợp lệ**:
   ```bash
   python -m shared.study_planner samples/tasks.csv --hours -5
   # Kỳ vọng: Báo lỗi số giờ phải lớn hơn 0
   ```

---

### Kịch bản 6: Xác thực kiểm thử End-to-End & Code Style
- **Mục đích**: Khẳng định độ tin cậy của phần mềm thông qua bộ kiểm thử tự động.
- **Lệnh thực thi**:
  ```bash
  # Chạy bộ test tích hợp E2E
  pytest -q tests/test_study_planner_e2e.py

  # Kiểm tra chuẩn linter
  ruff check shared/study_planner
  ```

---

## 4. Chuẩn bị câu hỏi phản biện & Giải đáp (Q&A Preparation)

### Câu hỏi 1: Vì sao nhóm sử dụng thuật toán Tham lam (Greedy) cho `allocate`?
- **Trả lời**: Bài toán phân bổ giờ học theo độ ưu tiên giảm dần tương tự bài toán Fractional Knapsack. Thuật toán tham lam cho độ phức tạp thời gian tối ưu $\mathcal{O}(N \log N)$ (do bước sắp xếp), dễ kiểm thử và rất trực quan với người dùng thực tế: luôn dồn toàn lực cho việc khẩn cấp/quan trọng nhất trước.

### Câu hỏi 2: Cơ chế chia tách module giúp ích gì cho làm việc nhóm?
- **Trả lời**: Mỗi thành viên phụ trách một module với giao diện hợp đồng (`shared.contract.Task`, `Block`) được xác định trước. Do đó, các thành viên có thể viết code và unit test độc lập mà không xảy ra xung đột (merge conflicts), trước khi Lead xâu chuỗi tại `__main__.py`.

### Câu hỏi 3: Nếu deadline của một công việc đã qua so với `--today` thì sao?
- **Trả lời**: Module `prioritise` tính toán `days_left`. Nếu deadline đã qua (`days_left < 0`), công việc vẫn được ghi nhận nhưng chuyển vào danh sách cảnh báo `overdue_tasks` trong module `summary` để người học nắm bắt và xử lý gấp.

