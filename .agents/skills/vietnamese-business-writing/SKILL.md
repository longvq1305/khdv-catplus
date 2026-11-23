---
name: vietnamese-business-writing
description: Viết báo cáo, tài liệu phân tích vận hành và đề xuất giải pháp bằng tiếng Việt tự nhiên, gần gũi như trao đổi với khách hàng/đồng nghiệp cùng ngành không chuyên kỹ thuật; đồng thời đảm bảo công thức và phông chữ tiếng Việt hiển thị chuẩn xác trên Markdown, HTML và Word (.docx).
---

# Kỹ năng Viết Báo cáo Nghiệp vụ Tự nhiên & Chuẩn Phông chữ Tiếng Việt

Sử dụng skill này khi soạn thảo báo cáo dự án, tài liệu tư vấn vận hành hoặc bài thuyết trình cho người đọc trong ngành (quản lý, đối tác, giảng viên đánh giá nghiệp vụ) mà không muốn văn bản mang màu sắc máy móc của AI hay nặng thuật ngữ lập trình.

## 1. Nguyên tắc Văn phong ("Trình bày với người cùng ngành nhưng không chuyên Tech")

1. **Kể câu chuyện vận hành thực tế thay vì đọc tên bảng code:**
   - Không chèn tên biến, tên hàm, mã trạng thái tiếng Anh (`StudentJourney`, `Class.clean()`, `ONE_ON_ONE`, `CLOSED_LOST`, `SCHEDULE_MISMATCH`) vào giữa câu văn.
   - Dùng đúng ngôn ngữ đời thường của người làm nghề: *"lộ trình theo dõi học viên"*, *"lớp kèm 1–1"*, *"lớp nhóm 3–5 em"*, *"học viên bỏ cuộc vì không khớp được lịch"*, *"lớp nhóm chỉ gom được 1–2 em nên chưa đủ sĩ số mở lớp"*.
   - Nếu cần dẫn chứng hệ thống phần mềm để đảm bảo tính xác thực, hãy gom riêng vào một câu chú thích nhỏ hoặc một cột riêng trong bảng.

2. **Khử mùi văn mẫu AI (Anti-AI-Tone):**
   - Tránh lạm dụng cấu trúc liệt kê gạch đầu dòng mở đầu bằng cụm từ in đậm + dấu hai chấm (`- **Khái niệm A:** ...`) ở mọi đoạn văn. Hãy kết hợp các đoạn văn xuôi ngắn (2–4 câu) có câu chuyển ý tự nhiên (*"Thực tế khi vận hành..."*, *"Điểm vướng lớn nhất nằm ở chỗ..."*, *"Để giải quyết chuyện này mà không làm xáo trộn cách làm việc của đội ngũ..."*).
   - Thay các từ ngữ học thuật dịch thô cứng bằng cách diễn đạt sáng rõ:
     - Thay *"Tài nguyên toán tử (Operant) / Tài nguyên toán hạng (Operand)"* $\rightarrow$ *"Nguồn lực con người và kỹ năng chuyên môn"* / *"Dữ liệu, công cụ và quỹ thời gian sẵn có"*.
     - Thay *"Hiệu ứng phân mảnh lớp nhóm dưới ngưỡng quorum"* $\rightarrow$ *"Tình trạng học viên đăng ký lớp nhóm bị rải lẻ ra quá nhiều khung giờ nên không gom đủ 3 em/lớp"*.
     - Thay *"Độ trễ bàn giao bất đồng bộ đa chặng"* $\rightarrow$ *"Thời gian chờ nhắn tin hỏi qua lại nhiều vòng giữa CSKH, Quản lý, Gia sư và Phụ huynh"*.

## 2. Nguyên tắc Sửa Lỗi Phông chữ & Công thức Toán học (Zero Font Glitch)

1. **Tuyệt đối không đặt chữ tiếng Việt có dấu vào trong `\text{...}` của LaTeX/KaTeX:**
   - Phông chữ toán học mặc định (`KaTeX_Main`, `Computer Modern`) không có bộ ký tự dấu tiếng Việt (`ă, ắ, ệ, ỷ, đ, ơ, ư`). Khi đặt tiếng Việt vào trong `$...$`, các chữ có dấu sẽ bị nhảy phông, lệch nét hoặc vỡ chữ.
2. **Cách trình bày công thức dễ hiểu và không bao giờ lỗi phông:**
   - Với các công thức chỉ số nghiệp vụ (KPI, tỷ lệ %, thời gian chờ, Định luật Little): trình bày trong **khung công thức định dạng bằng phông chữ tiếng Việt chuẩn (`Segoe UI` / `Arial`)** kèm ký hiệu toán học Unicode rõ ràng (`×`, `÷`, `≤`, `≥`, `→`, `±`, chỉ số dưới `₁, ₂`), hoặc chỉ dùng chữ cái viết tắt ngắn gọn (`N`, `W`, `L`, `λ`) rồi giải thích bằng tiếng Việt ở dòng bên dưới.
   - Khi xuất sang HTML và Word (`.docx`), không được để sót mã LaTeX thô (`\frac`, `\sum`, `\le`, `\rightarrow`, `\text`) hay để trình biên dịch Markdown biến dấu gạch dưới `_` thành thẻ in nghiêng `<em>`.
