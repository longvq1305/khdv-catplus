# Hướng dẫn Nhóm 20: Bộ Dự án Bản Làm Trước (Draft 1) & Cách Cập nhật Dữ liệu Thật

Thư mục này chứa trọn bộ sản phẩm **Bản làm trước (Draft 1)** cho đồ án môn học **INT3501 — Khoa học dịch vụ**, bám sát góp ý của giảng viên (*"Tỷ lệ ghép thành công, độ phù hợp lịch, thời gian chờ học viên"*), toàn bộ slide bài giảng L1–L7 và [INT3501_Huong_dan_du_an_Rubric.pdf](../INT3501_Huong_dan_du_an_Rubric.pdf).

## 1. Danh sách các tệp đã chuẩn bị

1. [Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md](./Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md) — **Báo cáo chính hoàn chỉnh 8 mục** theo cấu trúc khuyến nghị của Rubric (kèm Phụ lục Minh bạch sử dụng AI).
2. [catplus_matching_as_is.bpmn](./catplus_matching_as_is.bpmn) & [catplus_matching_to_be.bpmn](./catplus_matching_to_be.bpmn) — **2 file sơ đồ BPMN 2.0 chuẩn chỉnh** (3 Pool, 3 Lane, Message Flow / Sequence Flow tách bạch, Timer Boundary Event, nhánh ngoại lệ/Rework, và Annotation trực tiếp). Có thể mở trực tiếp tại `https://demo.bpmn.io/new` để kiểm tra hoặc xuất ảnh SVG/PNG độ phân giải cao.
3. [CatPlus_Sim_Opt_Model.py](./CatPlus_Sim_Opt_Model.py) — **Mã nguồn Python tái lập được** chạy mô hình Tối ưu hóa Quy hoạch nguyên hỗn hợp (MILP - Bài L5) + Mô phỏng Hàng đợi sự kiện rời rạc SimPy (Bài L4) + Phân tích độ nhạy (Sensitivity Analysis).
4. [draw_resource_map.py](./draw_resource_map.py) & [fig0_resource_map.png](./fig0_resource_map.png) — Bản đồ nguồn lực (Resource Map) chuẩn 5 tiêu chí Rubric, có ranh giới hệ thống và chú giải ký hiệu.
5. `fig1_as_is_vs_to_be_kpi.png`, `fig2_waiting_time_breakdown.png`, `fig3_sensitivity_analysis.png`, `simulation_results.json` — Các biểu đồ và kết quả thực nghiệm tự động sinh ra từ `CatPlus_Sim_Opt_Model.py`.
6. [export_real_data_template.py](./export_real_data_template.py) — Script mẫu (chỉ đọc & ẩn danh hóa) để bạn tự chạy trên môi trường server/local của CatPlus nhằm xuất dữ liệu thật thành file CSV mà không lộ thông tin cá nhân học sinh/phụ huynh.

---

## 2. Quy trình 3 bước để thay thế bằng Dữ liệu Thật khi bạn hoàn tất

1. **Bước 1 — Trích xuất số liệu thật ẩn danh:**
   * Dùng [export_real_data_template.py](./export_real_data_template.py) chạy trên DB `academic` và `customer-operations` để xuất 4 file CSV: `students_intake.csv`, `class_schedule_rules.csv`, `trial_sessions.csv`, `journey_events.csv`.
2. **Bước 2 — Tính toán chỉ số AS-IS thực tế:**
   * Từ `students_intake.csv`: tính trực tiếp tỷ lệ `ENROLLED / (ENROLLED + CLOSED_LOST)`, đếm số ca `SCHEDULE_MISMATCH` / `CENTER_CANNOT_SERVE`, và tính phân vị thời gian chờ (`enrolled_at - created_at`).
   * Từ `journey_events.csv`: tính thời gian trung bình học viên dừng ở từng chặng `CHUA_LIEN_HE` $\rightarrow$ `CHO_TEST` $\rightarrow$ `CHO_HOC_THU` $\rightarrow$ `CHO_LOP` $\rightarrow$ `DA_THAM_GIA`.
   * Hiệu chỉnh (calibrate) lại các tham số đầu vào trong `CatPlus_Sim_Opt_Model.py` (số học viên/tháng `n_students`, số gia sư `n_tutors`, phân phối khung giờ trong `SLOT_WEIGHTS`, thời gian xử lý thực tế của CSKH & Quản lý) khớp với số liệu vừa đo, rồi chạy lại lệnh:
     ```bash
     uv run --with simpy --with scipy --with matplotlib python CatPlus_Sim_Opt_Model.py
     ```
3. **Bước 3 — Cập nhật vào báo cáo:**
   * Trong file `Bao_cao_Du_an_Nhom20_CatPlus_Draft1.md`, tìm các vị trí được đánh dấu `[MÔ PHỎNG / CHỜ DỮ LIỆU THẬT]` để điền các số liệu thực nghiệm vừa đo được và cập nhật mục "Nguồn dữ liệu" trong Phụ lục AI.
