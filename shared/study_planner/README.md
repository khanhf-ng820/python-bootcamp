# Study Planner CLI (`shared.study_planner`)

`shared.study_planner` là gói CLI và thư viện Python phục vụ việc quản lý, sắp xếp thứ tự ưu tiên và phân bổ quỹ thời gian học tập tự động cho sinh viên. 

Dự án được phát triển và tích hợp bởi **Team T-W3** (CSC10014 — Python Bootcamp).

---

## 1. Tổng quan & Kiến trúc Pipeline

Công cụ kết nối các module độc lập do các thành viên trong nhóm xây dựng thành một pipeline xử lý dữ liệu hoàn chỉnh từ đầu vào CSV đến kết quả trực quan:

```text
               ┌───────────────────────────────┐
               │    Input CSV (tasks.csv)      │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │  parse_csv & validate_tasks   │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │          prioritise           │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │           allocate            │
               └──────────────┬────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  render (stdout) │ │  export (--output│ │  stats (--stats) │
│  Bảng ASCII trực │ │  Xuất file JSON  │ │  Thống kê Counter│
│  quan trên CLI   │ │  hoặc Markdown   │ │  & defaultdict   │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Các bước trong pipeline:
1. **`parse_csv(path)`**: Đọc file CSV, chuyển đổi từng dòng thành đối tượng `Task`.
2. **`validate_tasks(tasks)`**: Kiểm tra tính hợp lệ của dữ liệu (điểm quan trọng `1-5`, thời lượng học `> 0`).
3. **`prioritise(tasks, today=None)`**: Tính điểm ưu tiên dựa trên `importance` và số ngày còn lại đến `deadline`.
4. **`allocate(tasks, available_hours)`**: Thuật toán tham lam (Greedy) phân bổ thời gian học thành các `Block` theo thứ tự ưu tiên.
5. **Đầu ra**:
   - Mặc định: `render(blocks)` in bảng lịch học ra terminal.
   - Khi có cờ `--output`: `export_plan(blocks, path, ...)` lưu file `.json` hoặc `.md`.
   - Khi có cờ `--stats`: `format_stats(blocks)` hiển thị thống kê chi tiết theo cấp độ quan trọng và công việc chiếm nhiều giờ nhất.

---

## 2. Cài đặt & Yêu cầu môi trường

- **Python**: Phiên bản 3.10 trở lên.
- **Thư viện phụ thuộc**: Sử dụng hoàn toàn thư viện chuẩn của Python (`argparse`, `csv`, `datetime`, `json`, `collections`, `dataclasses`, `pathlib`).
- Kiểm tra môi trường:
  ```bash
  python --version
  ```

---

## 3. Cấu trúc dữ liệu đầu vào (Input CSV Format)

File CSV chứa danh sách công việc cần học phải tuân theo cấu trúc gồm 4 cột bắt buộc:

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `title` | `str` | Không được rỗng | Tên môn học hoặc nhiệm vụ |
| `importance` | `int` | Giá trị nguyên từ `1` đến `5` | Mức độ quan trọng (5 là cao nhất) |
| `effort_h` | `float` | Số thực `> 0` | Số giờ học dự kiến cần thiết |
| `deadline` | `str` | Định dạng chuẩn `YYYY-MM-DD` | Hạn chót hoàn thành nhiệm vụ |

### Ví dụ file mẫu (`samples/tasks.csv`):
```csv
title,importance,effort_h,deadline
DS exam,5,6.0,2026-10-30
Assignment,4,1.5,2026-10-27
Linear Algebra Quiz,3,2.0,2026-11-02
```

---

## 4. Hướng dẫn sử dụng CLI

Module được thực thi trực tiếp từ thư mục gốc của repository bằng câu lệnh:

```bash
python -m shared.study_planner <csv_path> --hours <HOURS> [options]
```

### Bảng tham số & cờ tùy chọn (CLI Arguments & Flags)

| Tham số / Flag | Bắt buộc | Mặc định | Mô tả |
| :--- | :---: | :---: | :--- |
| `csv_path` | Có | *(Không)* | Đường dẫn tới file CSV chứa danh sách tasks (ví dụ: `samples/tasks.csv`). |
| `--hours <float>` | **Có** | *(Không)* | Tổng số giờ học có thể phân bổ (phải là số thực dương). |
| `--today <YYYY-MM-DD>` | Không | Ngày hiện tại | Ngày mốc để tính độ khẩn cấp của deadline. |
| `--output <path>` | Không | `None` | Đường dẫn file để xuất kế hoạch. Định dạng tự động nhận diện theo đuôi `.json`, `.md` hoặc `.markdown`. |
| `--stats` | Không | `False` | Bật thống kê tổng hợp (tổng giờ, số block, tỷ lệ theo importance, top task). |

---

## 5. Các kịch bản sử dụng phổ biến

### 5.1. Phân bổ cơ bản hiển thị ra màn hình
Phân bổ 8 giờ học cho danh sách tasks:
```bash
python -m shared.study_planner samples/tasks.csv --hours 8
```
**Kết quả mẫu trên terminal:**
```text
=== Study Plan ===
Available hours: 8.00 h
Total allocated: 7.50 h

#1 | DS exam             | 6.00 h | Imp: 5 | Due: 2026-10-30
#2 | Assignment          | 1.50 h | Imp: 4 | Due: 2026-10-27
```

### 5.2. Chỉ định ngày mốc (`--today`)
Đánh giá độ ưu tiên với ngày mốc cố định:
```bash
python -m shared.study_planner samples/tasks_extended.csv --hours 10 --today 2026-10-28
```

### 5.3. Xem thống kê phân bổ (`--stats`)
Hiển thị phân tích cơ cấu giờ học theo từng mức độ quan trọng:
```bash
python -m shared.study_planner samples/tasks_extended.csv --hours 12 --stats
```
**Đoạn thống kê bổ sung:**
```text
Study Plan Statistics:
  - Total Allocated: 12.0 h across 4 block(s)
  - Top Task: Data Structures Final Exam (6.0 h)
  - Breakdown by Importance:
    * Level 5: 10.0 h (83.3%) - 2 block(s)
    * Level 4: 2.0 h (16.7%) - 2 block(s)
```

### 5.4. Xuất kế hoạch ra file Markdown (`--output plan.md`)
```bash
python -m shared.study_planner samples/tasks.csv --hours 6 --output output/my_plan.md
```
Tự động tạo thư mục `output/` nếu chưa có và xuất bảng Markdown:
```markdown
# Study Plan

Total allocated: **6 h** across **2** block(s).

| # | Task | Importance | Deadline | Effort (h) | Allocated (h) |
|---:|:---|---:|:---|---:|---:|
| 1 | DS exam | 5 | 2026-10-30 | 6 | 6 |
```

### 5.5. Xuất kế hoạch ra file JSON (`--output plan.json`)
```bash
python -m shared.study_planner samples/tasks.csv --hours 6 --output output/my_plan.json
```
Nội dung file JSON:
```json
{
  "total_hours": 6.0,
  "blocks": [
    {
      "index": 1,
      "title": "DS exam",
      "importance": 5,
      "effort_h": 6.0,
      "deadline": "2026-10-30",
      "hours": 6.0
    }
  ],
  "summary": null
}
```

---

## 6. Xử lý lỗi & Mã thoát (Exit Codes)

Hệ thống được thiết kế bắt lỗi chặt chẽ, không in traceback ra màn hình người dùng cuối, trả về exit code sạch:

| Mã thoát (Exit Code) | Nguyên nhân | Thông báo mẫu |
| :---: | :--- | :--- |
| `0` | Chạy thành công | Bảng lịch học hoặc thông báo xuất file thành công. |
| `1` | Không tìm thấy file đầu vào | `Error: File not found: samples/missing.csv` |
| `1` | File CSV rỗng | `Error: Input CSV file is empty` |
| `1` | Dữ liệu CSV không đúng định dạng | `Error: Invalid task row: invalid literal for int() ...` |
| `1` | Giá trị `--hours` không hợp lệ | `Error: Study hours must be positive, got: -2` |
| `1` | Kế hoạch bất khả thi (`InfeasiblePlan`) | `Error: Infeasible study plan: total mandatory effort exceeds available hours` |

---

## 7. Sử dụng như thư viện Python (Library API)

Các module trong `shared.study_planner` có thể được import độc lập trong code Python:

```python
from datetime import date
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.allocate import allocate
from shared.study_planner.render import render
from shared.study_planner.export import export_plan
from shared.study_planner.stats import calculate_stats

# 1. Đọc và lọc tasks
tasks = parse_csv("samples/tasks.csv")

# 2. Sắp xếp thứ tự ưu tiên
ranked_tasks = prioritise(tasks, today=date(2026, 10, 26))

# 3. Phân bổ giờ học
blocks = allocate(ranked_tasks, available_hours=8.0)

# 4. In trực quan
print(render(blocks))

# 5. Xuất file
export_plan(blocks, "output/plan.json")

# 6. Thống kê
stats = calculate_stats(blocks)
print(f"Top task: {stats['top_task']}")
```

---

## 8. Bảng phân công thành viên Team T-W3

| STT | Họ và tên | MSSV | Vai trò | Module đảm nhận | Nhiệm vụ chính |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | Nguyễn Phúc Khánh | 25125086 | Tech Lead | `shared/study_planner/__main__.py` | CLI argparse, xâu chuỗi pipeline, điều phối merge và gắn tag `py-w3-done`. |
| 2 | Trần Thành Lợi | 25125059 | Developer | `shared/study_planner/export.py` | Hàm `export_plan` xuất kết quả ra file JSON/Markdown qua cờ `--output`. |
| 3 | Lý Tuấn Kiệt | 25125022 | Presenter, Dev | `shared/study_planner/README.md`, `docs/demo.md` | Hướng dẫn sử dụng CLI, chuẩn hóa dataset mẫu `samples/`, tài liệu demo. |
| 4 | Nguyễn Minh Khang | 25125018 | QA/QC, Presenter | `tests/test_study_planner_e2e.py` | Bộ kiểm thử End-to-End với sample CSV, kiểm thử CI. |
| 5 | Trần Phúc Khánh | 25125020 | Security & Data | `shared/study_planner/errors.py` | Bắt lỗi file thiếu/rỗng, xử lý `InfeasiblePlan`, trả exit code 1 sạch. |
| 6 | Đặng Xuân Phát | 25125062 | UI/UX, QA/QC | `shared/study_planner/stats.py` | Thống kê phân bổ giờ học bằng `Counter`/`defaultdict` qua cờ `--stats`. |

