# BÁO CÁO DỰ ÁN CUỐI KỲ — HỌC PHẦN KHOA HỌC DỊCH VỤ (INT3501)

**ĐẠI HỌC QUỐC GIA HÀ NỘI — TRƯỜNG ĐẠI HỌC CÔNG NGHỆ**

## TỐI ƯU HÓA QUY TRÌNH GHÉP ĐÔI GIA SƯ – HỌC VIÊN VÀ XẾP LỊCH HỌC TRÊN NỀN TẢNG CATPLUS

*So sánh phương án xếp lịch thủ công cơ sở (AS-IS) và quy hoạch nguyên gom nhóm (MILP), kết hợp mô phỏng hàng đợi SimPy, trên hệ thống dịch vụ đào tạo lập trình CatPlus*

- **Nhóm 20** — Sinh viên thực hiện:
  - `23021941` — Phoutthavong Xayavong
  - `[Điền MSV]` — Vũ Quốc Long
- **Địa điểm, thời gian:** Hà Nội, 2026

---

## Mục lục

<!-- TOC_START -->
- **1 Bối cảnh và câu hỏi phân tích** *(trang 1)*
  - 1.1 Vấn đề dịch vụ *(trang 1)*
  - 1.2 Phạm vi và câu hỏi phân tích *(trang 1)*
  - 1.3 Dữ liệu và chỉ số *(trang 2)*
  - 1.4 Cách tiếp cận *(trang 2)*
- **2 Hệ thống dịch vụ đào tạo lập trình CatPlus** *(trang 3)*
  - 2.1 Mô tả hệ thống bằng Work System Framework *(trang 3)*
  - 2.2 Bản đồ nguồn lực và đồng tạo giá trị *(trang 4)*
- **3 Quy trình hiện tại và chẩn đoán** *(trang 5)*
  - 3.1 Quy trình AS-IS *(trang 5)*
  - 3.2 Phân tích thời gian theo từng chặng *(trang 5)*
  - 3.3 Phân tích hàng đợi và tình trạng tồn đọng *(trang 7)*
- **4 Mô hình tối ưu ghép lớp và xếp lịch** *(trang 7)*
  - 4.1 Quy mô học viên, gia sư và dữ liệu nhu cầu *(trang 7)*
  - 4.2 Khung giờ học và hàm điểm phù hợp lịch *(trang 8)*
  - 4.3 Mô hình phân công ghép đôi và gom nhóm (MILP) *(trang 8)*
  - 4.4 Giả định và cách kiểm tra *(trang 9)*
- **5 Triển khai tính toán và kết quả chạy** *(trang 10)*
  - 5.1 Chuỗi xử lý *(trang 10)*
  - 5.2 Trích mã nguồn và nhật ký chạy *(trang 11)*
- **6 Kết quả so sánh các phương án** *(trang 11)*
  - 6.1 So sánh AS-IS và TO-BE *(trang 11)*
  - 6.2 Đánh đổi đa mục tiêu và đường biên Pareto *(trang 13)*
  - 6.3 Độ ổn định và phân tích độ nhạy *(trang 14)*
- **7 Đề xuất cải tiến (TO-BE)** *(trang 15)*
  - 7.1 Thay đổi trong quy trình *(trang 15)*
  - 7.2 Lựa chọn cấu hình và lộ trình triển khai *(trang 16)*
  - 7.3 Vai trò, nguồn lực và chỉ số theo dõi *(trang 16)*
  - 7.4 Đánh đổi *(trang 17)*
- **8 Kết luận** *(trang 17)*
  - 8.1 Trả lời câu hỏi phân tích *(trang 17)*
  - 8.2 Giới hạn *(trang 18)*
  - 8.3 Hướng phát triển *(trang 18)*
- **Tài liệu tham khảo** *(trang 19)*
- **Phụ lục: Khai báo minh bạch sử dụng AI** *(trang 20)*
<!-- TOC_END -->

---

## 1 Bối cảnh và câu hỏi phân tích

### 1.1 Vấn đề dịch vụ

Trong đào tạo lập trình có gia sư kèm trực tiếp, việc tư vấn được một học sinh đăng ký mới chỉ là nửa chặng đường; xếp được lịch học khớp giữa học sinh, phụ huynh và gia sư để lớp thực sự khai giảng mới là bước quyết định. Tại nền tảng **CatPlus** (`https://learn.catplus.site/`), học sinh cấp hai (THCS) và cấp ba (THPT) theo học dưới hai hình thức: lớp kèm riêng 1–1 (đúng 1 học viên) và lớp nhóm nhỏ (bắt buộc đủ từ 3 đến 5 học viên cùng cấp học thì mới mở lớp). Hiện nay, dù phần mềm đã lưu trữ hồ sơ học viên và danh sách lớp, toàn bộ khâu hỏi lịch, tìm gia sư và gom nhóm vẫn do nhân sự xử lý thủ công qua điện thoại và Zalo rồi mới nhập kết quả lên hệ thống.

Tương tự các dịch vụ trực tiếp khác trong khung IHIP, năng lực giảng dạy của gia sư không thể lưu trữ: một ca trống của gia sư vào tối thứ Ba không thể để dành bù cho sự quá tải vào tối Chủ nhật, và hai học sinh rảnh lệch giờ nhau cũng không thể gộp chung vào một lớp nhóm. Ở quy trình hiện tại, nhân viên Chăm sóc khách hàng (CSKH) thường chỉ hỏi phụ huynh một khung giờ mong muốn nhất rồi chuyển cho Quản lý học vụ dò lịch theo thứ tự hồ sơ nào đến trước xếp trước. Khi lượng đăng ký đạt khoảng 60 học viên/tháng, học sinh chọn học nhóm bị rải mỏng ra 28 tổ hợp cấp học – khung giờ trong tuần (14 ca/tuần × 2 cấp học), khiến nhiều lớp dự kiến chỉ gom được 1–2 em, không đủ ngưỡng tối thiểu 3 học viên để khai giảng. Đồng thời, mỗi lần lệch lịch là hồ sơ phải quay vòng hỏi lại giữa Quản lý, Gia sư, CSKH và Phụ huynh, làm thời gian chờ kéo dài gần 3 ngày làm việc.

### 1.2 Phạm vi và câu hỏi phân tích

Nhóm tập trung vào học viên mới đăng ký và phụ huynh trong giai đoạn từ lúc gửi thông tin đăng ký (trạng thái *Chưa liên hệ*) đến khi nhận được lịch học thử/nhập học chính thức (*Đã tham gia*) hoặc dừng hồ sơ (*Đóng thất bại*). Nếu tăng được tỷ lệ ghép lớp và rút ngắn thời gian chờ trên cùng đội ngũ hiện có, cả gia đình người học, nhân viên CSKH, Quản lý học vụ và trung tâm đều hưởng lợi.

Phân tích giữ cố định quy mô vận hành tiêu chuẩn gồm *M* = 10 gia sư đang hoạt động, 2 nhân viên CSKH, 1 Quản lý học vụ và 14 khung giờ học phổ biến mỗi tuần. Nhóm không xét hoạt động chấm bài lập trình tự động sau khi học viên đã vào lớp, biên soạn đề thi hay đối soát học phí, bảng lương.

Nhóm so sánh phương án cơ sở **AS-IS** (CSKH hỏi 1 khung giờ đầu tiên, Quản lý dò tay tuần tự từng ca, hỏi đổi giờ tối đa 2 vòng) với phương án cải tiến **TO-BE** (CSKH thu thập tối đa 1–3 khung giờ khả dụng theo thứ tự ưu tiên, hệ thống chạy quy hoạch nguyên hỗn hợp MILP gom nhóm và gợi ý cặp ghép để Quản lý duyệt trong 1 vòng). Từ góp ý định hướng của giảng viên, nhóm đặt ra ba câu hỏi phân tích:

**Q1.** Trên cùng đội ngũ 10 gia sư và quy định lớp nhóm 3–5 học viên, phương án TO-BE tăng tỷ lệ ghép lớp thành công thêm bao nhiêu điểm phần trăm so với xếp tay AS-IS, và cần thu thập tối thiểu mấy khung giờ rảnh từ phụ huynh?

**Q2.** Việc gom nhóm để cứu các hồ sơ khó xếp lịch tạo ra sự đánh đổi như thế nào đối với điểm độ phù hợp lịch trên tập học viên vào lớp và trên toàn bộ học viên đăng ký?

**Q3.** Quy trình TO-BE rút ngắn thời gian chờ trung bình, phân vị P90 và giảm tải dò lịch thủ công cho Quản lý học vụ ra sao khi xét đến dòng hồ sơ đến ngẫu nhiên theo thời gian?

### 1.3 Dữ liệu và chỉ số

Trong giai đoạn hoàn thiện dữ liệu lịch sử trên máy chủ, nhóm xây dựng bộ dữ liệu mô phỏng tái lập (hạt giống ngẫu nhiên cố định `seed = 42`, gồm 20 chu kỳ tháng độc lập, tương đương 1.200 lượt hồ sơ học viên) bám sát cấu trúc cơ sở dữ liệu thực tế của dự án CatPlus (ràng buộc sĩ số lớp 1–1 bằng 1, lớp nhóm từ 3 đến 5 học viên, phân cấp THCS/THPT và lộ trình 5 chặng chăm sóc khách hàng). Toàn bộ mã nguồn được thiết kế tách biệt đầu vào để nạp trực tiếp tệp CSV ẩn danh trích xuất từ máy chủ sản xuất qua công cụ `export_real_data_template.py`. Bảng 1.1 định nghĩa các chỉ số đo lường xuyên suốt báo cáo.

**Bảng 1.1.** Các chỉ số dùng trong báo cáo

| Chỉ số | Định nghĩa và cách tính | Loại |
| :--- | :--- | :--- |
| *R*<sub>ghép</sub> | Tỷ lệ học viên được xếp lớp hợp lệ (1–1 hoặc nhóm 3–5 người) trên tổng số đăng ký (%) | KPI trọng tâm 1 |
| *N*<sub>rớt</sub> | Số hồ sơ không xếp được lớp mỗi tháng (do lệch lịch hoặc nhóm dưới 3 học viên) | Kết quả mô hình |
| Fit<sub>ghép</sub> | Điểm phù hợp lịch trung bình tính riêng trên các học viên đã xếp được lớp (thang 100) | KPI trọng tâm 2a |
| Fit<sub>chung</sub> | Điểm phù hợp lịch trung bình tính trên toàn bộ học viên đăng ký (rớt tính 0 điểm) | KPI trọng tâm 2b |
| *W*, P90 | Thời gian chờ trung bình và phân vị 90 từ lúc đăng ký tới lúc chốt lịch (giờ làm việc; 8h = 1 ngày) | KPI trọng tâm 3 |
| SLA<sub>16h</sub> | Tỷ lệ hồ sơ hoàn tất chốt lịch trong vòng 2 ngày làm việc (*W* ≤ 16 giờ, %) | Mức dịch vụ hàng đợi |
| *L*, *ρ*<sub>QL</sub> | Số hồ sơ tồn đọng trung bình trong hệ thống (*L* = *λW*) và tỷ lệ bận của Quản lý (%) | Chỉ số hàng đợi |

### 1.4 Cách tiếp cận

Nhóm mô tả hệ thống bằng khung Work System, logic hướng dịch vụ và bản đồ nguồn lực (Mục 2), sau đó dùng sơ đồ BPMN 2.0 để lần theo quy trình thủ công hiện tại (Mục 3.1). Phân tích thời gian từng chặng và mô phỏng hàng đợi giúp chỉ ra hai điểm nghẽn chính là tình trạng xé lẻ lớp nhóm dưới 3 người và vòng lặp chờ tin nhắn Zalo (Mục 3.2 và 3.3). Từ đó, nhóm xây dựng mô hình quy hoạch nguyên hỗn hợp (MILP) để gom cụm lớp nhóm kết hợp ghép đôi 1–1 (Mục 4), triển khai chuỗi xử lý tự động bằng Python (Mục 5), đối chiếu kết quả qua 20 lần lặp độc lập kèm đường biên Pareto và ba kịch bản độ nhạy (Mục 6), trước khi lập bảng quyết định và lộ trình áp dụng thực tế cho trung tâm (Mục 7).

---

## 2 Hệ thống dịch vụ đào tạo lập trình CatPlus

### 2.1 Mô tả hệ thống bằng Work System Framework

Nhóm chọn Work System Framework (WSF) của Alter [1] làm khung phân tích chủ đạo để mô tả cách đội ngũ CSKH, Quản lý học vụ và Gia sư sử dụng thông tin lịch rảnh cùng phần mềm quản trị nhằm đưa học viên vào lớp phù hợp. Khung WSF giúp tách bạch giữa năng lực chuyên môn của gia sư với cách thức thu thập thông tin và quy tắc điều phối lịch học. Nhờ đó, nhóm có thể cải thiện tỷ lệ mở lớp bằng cách thay đổi quy trình thu thập khung giờ và công cụ gợi ý ghép nhóm mà không cần quy lỗi cho nhân sự hay đòi hỏi tuyển thêm gia sư ngay lập tức. Bảng 2.1 trình bày chín thành phần của hệ thống tại CatPlus.

**Bảng 2.1.** Chín thành phần Work System của dịch vụ ghép đôi và xếp lịch tại CatPlus

| Thành phần | Trong hệ thống CatPlus | Vai trò trong đề tài |
| :--- | :--- | :--- |
| Khách hàng | Học sinh (THCS, THPT) và phụ huynh trực tiếp trao đổi lịch học, học phí | Nguồn phát sinh nhu cầu và cung cấp khung giờ rảnh đầu vào |
| Sản phẩm, dịch vụ | Tư vấn lộ trình, buổi học thử và lớp học chính thức (kèm 1–1 hoặc nhóm 3–5 em) | Đánh giá bằng tỷ lệ ghép thành công, độ hợp lịch và thời gian chờ |
| Quy trình | Tiếp nhận hồ sơ, gọi tư vấn, dò lịch gia sư, gom nhóm, xác nhận và chốt lớp | Đối tượng mô hình hóa BPMN (AS-IS → TO-BE) và đo thời gian chặng |
| Người tham gia | Nhân viên CSKH (2 người), Quản lý học vụ (1 người), đội ngũ Gia sư (10 người) | Giữ vai trò tư vấn con người và phê duyệt cuối cùng ở cả AS-IS và TO-BE |
| Thông tin | Cấp học, loại lớp đăng ký, khung giờ rảnh của trò, ca trống và trần số lớp của thầy | Đầu vào quyết định khả năng gom đủ sĩ số nhóm từ 3 đến 5 học viên |
| Công nghệ | Phần mềm web nội bộ (quản lý học vụ, chăm sóc khách hàng) và kênh Zalo, điện thoại | Hiện mới dùng ghi nhận hậu kiểm; đề xuất bổ sung module gợi ý MILP |
| Môi trường | Lịch học văn hóa dày đặc của học sinh (dồn vào tối và cuối tuần); cạnh tranh giữ khách | Nguyên nhân làm trùng khung giờ cao điểm và rớt khách nếu chờ lâu |
| Hạ tầng | Phòng học trực tuyến (Google Meet/Zoom) và phòng học trực tiếp, máy chủ dữ liệu | Nền tảng vận hành lớp học sau khi lịch đã được chốt |
| Chiến lược | Kết hợp tư vấn sát sao của con người với hiệu quả gom nhóm để tối ưu chi phí gia sư | Biến điều chỉnh qua trọng số đánh đổi giữa số ca mở và tỷ lệ nhận lớp |

### 2.2 Bản đồ nguồn lực và đồng tạo giá trị

Hình 2.1 thể hiện ranh giới hệ thống, bốn nhóm nguồn lực nội tại và các luồng tương tác giữa năm chủ thể tham gia. Hạ tầng mạng, công cụ liên lạc bên ngoài (Zalo, điện thoại) và các kỳ thi học sinh giỏi nằm ngoài đường bao ranh giới vì đề xuất cải tiến không can thiệp vào các yếu tố này.

![Bản đồ nguồn lực hệ thống CatPlus](./fig0_resource_map.png)
*Hình 2.1. Bản đồ nguồn lực và cơ chế đồng tạo giá trị của hệ thống ghép đôi – xếp lịch CatPlus; thể hiện ranh giới phân tích, bốn nhóm nguồn lực, lợi ích, chi phí/rủi ro và bảng chú giải ký hiệu (nhóm thiết kế cấu trúc; AI hỗ trợ mã vẽ Matplotlib; nhóm tự kiểm chứng).*

Theo logic hướng dịch vụ (SDL) của Vargo và Lusch [2], cơ sở dữ liệu hồ sơ, danh sách lớp và các khung giờ trống là nguồn lực bị tác động (operand resources). Chúng chỉ chuyển thành kết quả thực tế khi CSKH, Quản lý và Gia sư vận dụng kỹ năng tư vấn, kinh nghiệm sư phạm và quy tắc điều phối — tức nguồn lực tác động (operant resources) — để tích hợp lịch của thầy và trò. Dưới góc nhìn Lý thuyết dịch vụ thống nhất (UST) của Sampson [3], phụ huynh và học viên tham gia trực tiếp vào quá trình đồng tạo giá trị ngay từ bước cung cấp thông tin lịch rảnh: nếu gia đình chỉ đưa ra đúng 1 khung giờ cứng nhắc, không gian ghép nhóm bị thu hẹp mạnh; ngược lại, khi CSKH khai thác được 2–3 khung giờ có thể thu xếp, khả năng gom đủ nhóm 3–5 học viên tăng vọt.

Bản đồ cũng chỉ rõ lợi ích, chi phí và rủi ro của từng bên. Học viên được vào học sớm và đúng trình độ nhưng có rủi ro bỏ cuộc nếu phải chờ đổi lịch nhiều lần. CSKH và Quản lý kiểm soát được chất lượng tư vấn nhưng chịu tải lớn khi phải nhắn tin hỏi lịch thủ công qua nhiều vòng. Gia sư có thêm thu nhập và lịch dạy ổn định song có thể từ chối ca đột xuất nếu lịch rảnh trên hệ thống không được cập nhật định kỳ.

---

## 3 Quy trình hiện tại và chẩn đoán

### 3.1 Quy trình AS-IS

Hình 3.1 mô tả quy trình hiện tại bằng chuẩn BPMN 2.0 từ lúc phụ huynh gửi đăng ký đến khi học viên nhập học thành công (hoặc đóng hồ sơ thất bại). Sơ đồ gồm ba pool độc lập: *Phụ huynh & Học viên*, *Vận hành CatPlus* (chia thành ba lane nội bộ cho *CSKH*, *Quản lý học vụ* và *Hệ thống phần mềm*) và *Gia sư*. Mọi giao tiếp giữa ba pool đều đi qua luồng thông điệp nét đứt; luồng trình tự nét liền chỉ nối các bước trong cùng một pool và sử dụng cổng rẽ nhánh loại trừ XOR (`×`).

![Sơ đồ BPMN 2.0 quy trình AS-IS](./fig_bpmn_as_is.png)
*Hình 3.1. BPMN AS-IS của quy trình tiếp nhận, ghép gia sư và xếp lịch học cho một hồ sơ học viên mới (tệp chuẩn mở trên bpmn.io: `catplus_matching_as_is.bpmn`; nhóm xây dựng logic; AI hỗ trợ kết xuất đồ họa; nhóm kiểm tra 10 quy tắc BPMN).*

Khi nhận hồ sơ mới, hệ thống ghi nhận trạng thái chờ xử lý và chuyển cho CSKH gọi tư vấn để lấy mục tiêu học tập cùng 1 khung giờ ưu tiên đầu tiên (nếu quá 24 giờ không liên hệ được, sự kiện biên đồng hồ sẽ chuyển hồ sơ sang đóng thất bại). Tiếp theo, hồ sơ được bàn giao sang Quản lý học vụ để dò lịch bằng mắt theo thứ tự đến trước phục vụ trước và nhắn Zalo hỏi gia sư. Tại sự kiện chờ gia sư phản hồi (giới hạn 8 giờ), nếu gia sư báo bận hoặc lớp nhóm dự kiến chưa gom đủ tối thiểu 3 học viên cùng cấp học, quy trình rẽ sang kiểm tra số vòng thử: nếu dưới 2 vòng, hồ sơ bị trả ngược về CSKH để gọi thuyết phục phụ huynh chọn khung giờ khác (*Rework*). Nếu sau 2 vòng vẫn không khớp hoặc phụ huynh xin hủy chờ, hệ thống ghi nhận đóng hồ sơ thất bại.

### 3.2 Phân tích thời gian theo từng chặng

Trên 1.200 lượt hồ sơ mô phỏng từ 20 tháng vận hành hiện trạng AS-IS (Bảng 3.1 và Hình 3.2), tổng thời gian trung bình từ lúc đăng ký tới lúc kết thúc quy trình là **22,56 giờ làm việc** (tương đương **2,82 ngày làm việc**, quy ước 8 giờ làm việc/ngày), với phân vị P90 lên tới **31,29 giờ** (3,91 ngày). Tỷ lệ hồ sơ hoàn tất trong vòng 2 ngày làm việc (*W* ≤ 16 giờ) chỉ đạt **18,0%**.

**Bảng 3.1.** Thời gian từng chặng (giờ làm việc) của một hồ sơ trong quy trình hiện tại AS-IS (20 chu kỳ tháng, *N* = 60 hồ sơ/tháng)

| Chặng xử lý trong hành trình học viên | Thời gian TB (giờ) | Tỷ trọng (%) | Nguyên nhân gây trễ chủ yếu tại chặng |
| :--- | :---: | :---: | :--- |
| 1. Tiếp nhận và CSKH gọi tư vấn lần đầu | 1,95 | 8,6% | Khoảng 30% phụ huynh bận máy lần đầu, phải chờ 2–5,5 giờ gọi lại |
| 2. Quản lý dò lịch, hỏi gia sư và lặp lại đổi giờ | 15,66 | 69,4% | Chờ gia sư trả lời Zalo (2,5–7,5h/vòng), hỏi lại phụ huynh và chờ gom đủ nhóm 3 em |
| 3. Chốt lịch học thử và xác nhận nhập học | 4,96 | 22,0% | Xác nhận chéo lần cuối giữa phụ huynh và gia sư trước buổi đầu tiên |
| **Tổng chu trình toàn quy trình (*W*)** | **22,56** | **100,0%** | **Phân vị P90 = 31,29 giờ (3,91 ngày); tỷ lệ đạt SLA ≤ 16h = 18,0%** |

Kết quả phân rã trên Hình 3.2 cho thấy chặng 2 (*Dò lịch, gom nhóm và chốt gia sư*) chiếm tới **69,4%** tổng thời gian chờ của học viên (15,66 giờ trên 22,56 giờ), trong khi chặng 1 của CSKH chỉ chiếm 8,6%. Điều này bác bỏ nhận định cảm tính rằng học viên chờ lâu là do CSKH gọi điện chậm; điểm nghẽn thực sự nằm ở vòng lặp nhắn tin chờ xác nhận thủ công và thời gian treo hồ sơ chờ gom đủ sĩ số nhóm.

![Phân rã thời gian chờ theo từng chặng](./fig2_waiting_time_breakdown.png)
*Hình 3.2. Phân rã thời gian chu trình trung bình (giờ làm việc) qua ba chặng của quy trình AS-IS so với TO-BE.*

### 3.3 Phân tích hàng đợi và tình trạng tồn đọng

Để kiểm tra tải công việc của nhân sự và mức độ ứ đọng hồ sơ, nhóm áp dụng lý thuyết hàng đợi trên khung thời gian 240 giờ làm việc mỗi tháng (30 ngày × 8 giờ/ngày). Với nhu cầu trung bình 60 học viên/tháng, cường độ dòng hồ sơ đến là *λ* = 60 / 240 = 0,25 hồ sơ/giờ làm việc. Theo định luật Little [4], số lượng hồ sơ trung bình đang nằm chờ xử lý trong hệ thống tại một thời điểm bất kỳ (*L*) liên hệ trực tiếp với thời gian chu trình trung bình (*W*) qua công thức:

{{EQ:<i>L</i> = <i>λ</i> · <i>W</i> = 0,25 × 22,56 = 5,64 hồ sơ,&emsp;&emsp;<i>ρ</i><sub>QL</sub> = <span class="frac"><span class="num"><i>B</i><sub>QL</sub></span><span class="den"><i>s</i><sub>QL</sub> · <i>H</i></span></span> = 49,7%.|(3.1)}}

Trong đó *B*<sub>QL</sub> là tổng số giờ Quản lý trực tiếp thao tác dò lịch và nhắn tin trong tháng, *s*<sub>QL</sub> = 1 là số Quản lý học vụ, và *H* = 240 giờ. Kết quả cho thấy ở hiện trạng AS-IS, luôn có trung bình **5,64 hồ sơ** bị treo đồng thời trên bàn làm việc, và riêng việc dò lịch thủ công đã ngốn **49,7%** quỹ giờ làm việc của Quản lý học vụ (trong khi 2 nhân viên CSKH chỉ bận trung bình *ρ*<sub>CSKH</sub> = 13,7%). Đáng chú ý, nếu áp dụng công thức hàng đợi độc lập M/M/1 chỉ tính thời gian Quản lý ngồi thao tác (khoảng 1,3 giờ/lượt), thời gian chờ ước tính sẽ thấp hơn nhiều so với thực tế 22,56 giờ, bởi phần lớn độ trễ sinh ra từ thời gian chờ phản hồi bất đồng bộ trên Zalo và vòng lặp trả hồ sơ về CSKH khi lệch lịch.

:::summary-box
**Tóm tắt chẩn đoán**
- Điểm nghẽn thời gian nằm ở **chặng dò lịch và thương lượng lại** (chiếm 69,4% tổng thời gian 22,56 giờ), khiến chỉ có 18,0% hồ sơ chốt xong trong 2 ngày làm việc và Quản lý mất 49,7% giờ làm cho thao tác thủ công.
- Điểm nghẽn chất lượng nằm ở **hiệu ứng xé lẻ lớp nhóm**: khi chỉ hỏi 1 khung giờ và xếp tuần tự, trung bình **23,75 / 60 học viên (39,6%) bị rớt mỗi tháng**, trong đó tới 17,50 ca rớt vì lớp nhóm nháp chỉ gom được 1–2 em (dưới ngưỡng tối thiểu 3 học viên) và 6,25 ca rớt do lệch lịch gia sư.
- Vì vậy, giải pháp can thiệp đúng trọng tâm là **mở rộng thông tin đầu vào lên 2–3 khung giờ ngay từ bước CSKH** kết hợp **mô hình tối ưu hóa gom cụm lớp nhóm theo đợt**.
:::

---

## 4 Mô hình tối ưu ghép lớp và xếp lịch

### 4.1 Quy mô học viên, gia sư và dữ liệu nhu cầu

Nhóm thiết lập bài toán cho một chu kỳ tuyển sinh tiêu chuẩn gồm *N* = 60 học viên đăng ký và *M* = 10 gia sư trên lưới 14 khung giờ học cố định hàng tuần (10 ca buổi tối từ thứ Hai đến thứ Sáu lúc 18h00 và 19h45; 4 ca sáng, chiều, tối thứ Bảy và Chủ nhật). Phân bố nhu cầu phản ánh đặc thù thực tế của học sinh phổ thông: các ca buổi tối cuối tuần và ca 19h45 có xác suất được chọn cao hơn ca 18h00 đầu tuần.

Trong 60 học viên, 55% thuộc cấp THCS và 45% thuộc cấp THPT; 40% đăng ký học kèm 1–1 (sĩ số bắt buộc bằng 1) và 60% đăng ký học nhóm (sĩ số bắt buộc từ 3 đến 5 học viên cùng cấp học). Về độ linh hoạt thời gian, 20% học viên có lịch rất hẹp (chỉ thu xếp được đúng 1 khung giờ trong tuần), 45% thu xếp được 2 khung giờ và 35% linh hoạt được 3 khung giờ. Về phía nguồn cung, 50% gia sư dạy được cả hai cấp THCS và THPT, 30% chuyên THCS và 20% chuyên THPT; mỗi gia sư có từ 5 đến 7 khung giờ trống mỗi tuần và nhận dạy tối đa *K*<sub>*t*</sub> ∈ {3, 4, 5} lớp để bảo đảm chất lượng giảng dạy.

### 4.2 Khung giờ học và hàm điểm phù hợp lịch

Mỗi học viên *i* ∈ *I* = {1, ..., *N*} cung cấp danh sách tối đa *m* khung giờ khả dụng *S*<sub>*i*</sub> ⊂ {1, ..., 14} (*m* = 1 ở lần hỏi đầu của AS-IS; *m* ≤ 3 ở TO-BE). Để lượng hóa mức độ thuận tiện cho gia đình người học, nhóm gán điểm phù hợp *w*<sub>*i*,*s*</sub> = 100 nếu học viên *i* được xếp đúng khung giờ ưu tiên số 1, *w*<sub>*i*,*s*</sub> = 80 cho khung giờ ưu tiên số 2, *w*<sub>*i*,*s*</sub> = 60 cho khung giờ ưu tiên số 3 và 0 điểm nếu không xếp được lớp. Gọi *I*<sub>ghép</sub> ⊆ *I* là tập học viên được xếp lớp thành công và *s*(*i*) là khung giờ được gán, hai chỉ số độ phù hợp lịch được tính tường minh theo công thức:

{{EQ:Fit<sub>ghép</sub> = <span class="frac"><span class="num">1</span><span class="den">|<i>I</i><sub>ghép</sub>|</span></span> ∑<sub><i>i</i> ∈ <i>I</i><sub>ghép</sub></sub> <i>w</i><sub><i>i</i>, <i>s</i>(<i>i</i>)</sub>,&emsp;&emsp;Fit<sub>chung</sub> = <span class="frac"><span class="num">1</span><span class="den"><i>N</i></span></span> ∑<sub><i>i</i> = 1</sub><sup><i>N</i></sup> <i>w</i><sub><i>i</i>, <i>s</i>(<i>i</i>)</sub>.|(4.1)}}

Việc tách đôi Fit<sub>ghép</sub> và Fit<sub>chung</sub> giúp tránh ngộ nhận khi so sánh: một phương án loại bỏ hết các học viên khó xếp lịch có thể đạt Fit<sub>ghép</sub> rất cao trên số ít học viên còn lại, nhưng lại làm Fit<sub>chung</sub> của toàn trung tâm tụt thấp.

### 4.3 Mô hình phân công ghép đôi và gom nhóm (MILP)

Bảng 4.1 tóm tắt năm yếu tố cấu thành bài toán tối ưu hóa theo phương pháp luận của Daskin [5]. Gọi *K* là tập tất cả các cặp `(gia sư t, khung giờ s)` mà gia sư *t* còn trống lịch, được đánh chỉ số *k* ∈ *K*, và *C* = {(THCS, 1–1), (THPT, 1–1), (THCS, Nhóm), (THPT, Nhóm)} là tập 4 cấu hình lớp học hợp lệ. Với mỗi cấu hình *c* ∈ *C*, ngưỡng sĩ số tối thiểu và tối đa được ký hiệu là (*L*<sub>*c*</sub>, *U*<sub>*c*</sub>), nhận giá trị (1, 1) đối với lớp 1–1 và (3, 5) đối với lớp nhóm.

**Bảng 4.1.** Năm yếu tố của bài toán tối ưu ghép đôi và xếp lịch học

| Yếu tố | Trong đề tài CatPlus |
| :--- | :--- |
| Dữ liệu đầu vào | Tập *N* = 60 học viên (cấp học, hình thức 1–1/Nhóm, 1–3 khung giờ rảnh kèm điểm *w*<sub>*i*,*k*</sub> ∈ {100, 80, 60}); *M* = 10 gia sư (cấp dạy được, 5–7 ca trống, trần số lớp *K*<sub>*t*</sub>) |
| Biến quyết định | *x*<sub>*i*,*k*</sub> ∈ {0, 1} gán học viên *i* vào ca *k*; *y*<sub>*k*,*c*</sub> ∈ {0, 1} mở lớp cấu hình *c* tại ca *k*; *u*<sub>*i*</sub> ∈ {0, 1} đưa học viên *i* vào "lớp ảo" chưa ghép được |
| Hàm mục tiêu | Cực tiểu hóa tổng điểm phạt học viên rớt (*P* · *u*<sub>*i*</sub>) trừ tổng điểm phù hợp lịch (*w*<sub>*i*,*k*</sub> · *x*<sub>*i*,*k*</sub>) cộng chi phí mở lớp (*γ* · *y*<sub>*k*,*c*</sub>) |
| Ràng buộc cứng | Mỗi học viên nhận tối đa 1 ca; mỗi ca gia sư mở tối đa 1 lớp; lớp nhóm phải đủ từ 3 đến 5 học viên; không vượt số lớp tối đa *K*<sub>*t*</sub> của từng gia sư |
| Phân tích độ nhạy | Lượng học viên *N* ∈ {45, 60, 75, 90}; số gia sư *M* ∈ {6, 8, 10, 12}; số khung giờ thu thập *m* ∈ {1, 2, 3}; chi phí mở lớp *γ* ∈ [10, 1105] |

Để mô hình luôn có nghiệm khả thi ngay cả khi nhu cầu vượt quá năng lực phục vụ, nhóm bổ sung biến nhị phân "lớp ảo" *u*<sub>*i*</sub> ∈ {0, 1} với mức phạt lớn *P* = 1.000 cho mỗi học viên chưa xếp được lớp (theo kỹ thuật xử lý ràng buộc mềm bằng chi phí phạt ở Bài L5). Bài toán quy hoạch nguyên hỗn hợp (MILP) tìm nghiệm cực tiểu của hàm mục tiêu đa mục tiêu có trọng số:

{{EQ:min <i>Z</i> = ∑<sub><i>i</i> ∈ <i>I</i></sub> <i>P</i> · <i>u<sub>i</sub></i> − ∑<sub><i>i</i> ∈ <i>I</i></sub> ∑<sub><i>k</i> ∈ <i>K<sub>i</sub></i></sub> <i>w<sub>i,k</sub></i> · <i>x<sub>i,k</sub></i> + <i>γ</i> ∑<sub><i>k</i> ∈ <i>K</i></sub> ∑<sub><i>c</i> ∈ <i>C</i></sub> <i>y<sub>k,c</sub></i>|(4.2)}}

thỏa mãn bốn hệ ràng buộc tuyến tính nguyên sau:

{{EQ:∑<sub><i>k</i> ∈ <i>K<sub>i</sub></i></sub> <i>x<sub>i,k</sub></i> + <i>u<sub>i</sub></i> = 1,&emsp;&emsp;∀<i>i</i> ∈ <i>I</i>,|(4.3)}}

{{EQ:∑<sub><i>c</i> ∈ <i>C</i></sub> <i>y<sub>k,c</sub></i> ≤ 1,&emsp;&emsp;∀<i>k</i> ∈ <i>K</i>,&emsp;&emsp;&emsp;∑<sub><i>k</i> ∈ <i>K</i>(<i>t</i>)</sub> ∑<sub><i>c</i> ∈ <i>C</i></sub> <i>y<sub>k,c</sub></i> ≤ <i>K<sub>t</sub></i>,&emsp;&emsp;∀<i>t</i> ∈ <i>T</i>,|(4.4)}}

{{EQ:<i>L<sub>c</sub></i> · <i>y<sub>k,c</sub></i> ≤ ∑<sub><i>i</i> ∈ <i>I</i>(<i>k,c</i>)</sub> <i>x<sub>i,k</sub></i> ≤ <i>U<sub>c</sub></i> · <i>y<sub>k,c</sub></i>,&emsp;&emsp;∀<i>k</i> ∈ <i>K</i>, ∀<i>c</i> ∈ <i>C</i>,&emsp;&emsp;<i>x<sub>i,k</sub></i>, <i>y<sub>k,c</sub></i>, <i>u<sub>i</sub></i> ∈ {0, 1}.|(4.5)}}

Ràng buộc (4.3) bảo đảm mỗi học viên hoặc được xếp vào đúng một ca dạy tương thích, hoặc được đánh dấu *u*<sub>*i*</sub> = 1 để Quản lý chủ động xử lý ngoại lệ. Ràng buộc (4.4) ngăn một gia sư dạy hai lớp trùng giờ và giữ tổng số lớp của gia sư *t* không vượt trần *K*<sub>*t*</sub>. Đặc biệt, bất đẳng thức hai đầu (4.5) thể hiện chính xác quy định mở lớp của trung tâm: với lớp nhóm (*L*<sub>*c*</sub> = 3, *U*<sub>*c*</sub> = 5), nếu một khung giờ chỉ có 1 hoặc 2 học viên tương thích thì vế trái `3 · y ≤ ∑ x` buộc *y*<sub>*k*,*c*</sub> = 0 (không được mở lớp nhóm thiếu người), từ đó thúc đẩy bộ giải tự động dịch chuyển các học viên có 2–3 khung giờ rảnh về chung một ca để vượt ngưỡng 3 học viên. Ở cấu hình mặc định, nhóm đặt *γ* = 0,05 để ưu tiên tối đa số học viên vào lớp trước khi gom gọn số ca mở.

### 4.4 Giả định và cách kiểm tra

Bảng 4.2 liệt kê các giả định chính được sử dụng trong mô hình tối ưu hóa – mô phỏng và cách nhóm kiểm chứng độ bền của từng giả định trước khi đưa ra khuyến nghị.

**Bảng 4.2.** Giả định của mô hình và cách nhóm kiểm tra

| Giả định trong mô hình | Cách nhóm kiểm tra và đối chứng |
| :--- | :--- |
| Nhu cầu cơ sở *N* = 60 học viên/tháng và *M* = 10 gia sư | Thử nghiệm độ nhạy *N* ∈ {45, 60, 75, 90} và *M* ∈ {6, 8, 10, 12} (Mục 6.3) |
| Phụ huynh cung cấp tối đa 3 khung giờ khi CSKH hỏi kỹ | Đối chứng cố định cùng tập học viên với *m* ∈ {1, 2, 3} khung giờ (Bảng 6.3) |
| Gia sư cập nhật đúng khung giờ trống trên hệ thống | Bổ sung tỷ lệ 8% gia sư bận đột xuất trong mô phỏng SimPy để kiểm tra bước dự phòng |
| Xếp tay AS-IS có bước Quản lý cố gắng ghép vớt nhóm thiếu người | Lập trình hàm AS-IS có vòng cứu vớt thủ công sang các nhóm hợp lệ còn chỗ (< 5 người) |
| Ưu tiên tối đa tỷ lệ nhận lớp (*P* = 1.000, *γ* = 0,05) | Quét *γ* ∈ {10, 1065, 1085, 1105} để dựng đường biên đánh đổi Pareto (Mục 6.2) |

---

## 5 Triển khai tính toán và kết quả chạy

### 5.1 Chuỗi xử lý

Toàn bộ kết quả định lượng và hình vẽ trong báo cáo được sinh tự động bằng các tệp mã Python trong thư mục `du_an_nhom20/`, không chỉnh sửa tay bất kỳ con số nào. Bảng 5.1 trình bày các bước trong chuỗi xử lý và kết quả chạy thực tế.

**Bảng 5.1.** Các bước của chuỗi xử lý, việc thực hiện và kết quả chính của lần chạy gần nhất

| Tệp mã | Việc thực hiện | Kết quả chạy |
| :--- | :--- | :--- |
| `export_real_data_template.py` | Trích xuất ẩn danh trạng thái hồ sơ, lịch lớp và nhật ký chuyển chặng từ DB thật | Xuất 4 tệp CSV sạch thông tin cá nhân khi nạp dữ liệu máy chủ |
| `CatPlus_Sim_Opt_Model.py` | Sinh 20 chu kỳ tháng (`seed = 42`), giải AS-IS, giải MILP bằng HiGHS và mô phỏng SimPy | *R*<sub>ghép</sub> tăng từ 60,4% lên 92,7%; *W* giảm từ 22,56h xuống 10,29h |
| `CatPlus_Sim_Opt_Model.py` *(độ nhạy & Pareto)* | Chạy 11 kịch bản độ nhạy (*N*, *M*, *m*) và quét 4 mức chi phí mở lớp *γ* | Xuất `simulation_results.json` và 4 biểu đồ `fig1`..`fig4` |
| `draw_resource_map.py` | Dựng sơ đồ Bản đồ nguồn lực và cơ chế đồng tạo giá trị (Hình 2.1) | Xuất `fig0_resource_map.png` (220 DPI) |
| `draw_bpmn_diagrams.py` | Kết xuất trực quan hai sơ đồ Swimlane BPMN 2.0 khớp với tệp `.bpmn` | Xuất `fig_bpmn_as_is.png` và `fig_bpmn_to_be.png` |
| `build_preview_docs.py` | Đồng bộ số liệu, tự động đánh số trang Mục lục và xuất HTML, PDF, Word | Hoàn tất trọn bộ báo cáo định dạng chuẩn học thuật |

Về mặt kỹ thuật, nhóm phát biểu bài toán (4.2)–(4.5) dưới dạng ma trận thưa (`scipy.sparse.coo_matrix`) và giải trực tiếp bằng bộ giải quy hoạch nguyên **HiGHS** tích hợp trong `scipy.optimize.milp` [6], kết hợp thư viện mô phỏng sự kiện rời rạc `simpy` [7]. Mỗi bài toán tháng (60–90 học viên, khoảng 350 biến nhị phân) đều hội tụ về nghiệm tối ưu toàn cục trong dưới 0,5 giây trên máy tính cá nhân.

### 5.2 Trích mã nguồn và nhật ký chạy

Đoạn mã dưới đây trích phần thiết lập ràng buộc sĩ số hai đầu (4.5) và lời gọi bộ giải HiGHS trong tệp `du_an_nhom20/CatPlus_Sim_Opt_Model.py`, khớp trực tiếp với mô hình toán ở Mục 4.3:

```python
# Trich tu du_an_nhom20/CatPlus_Sim_Opt_Model.py (ham solve_to_be_milp)
for (k, tid, slot, lvl, mode, l_cap, u_cap) in y_vars:
    yi = y_index[(k, lvl, mode)]
    compat_x = [x_index[(i, k)] for i, s in enumerate(students)
                if (i, k) in x_index and s["level"] == lvl and s["mode"] == mode]
    if compat_x:
        # Rang buoc can tren: sum(x_ik) - U_c * y_kc <= 0
        rows.extend([row_idx] * (len(compat_x) + 1))
        cols.extend(compat_x + [yi])
        vals.extend([1.0] * len(compat_x) + [-float(u_cap)])
        lbs.append(-np.inf); ubs.append(0.0); row_idx += 1
        # Rang buoc can duoi nhom (quorum >= 3): sum(x_ik) - L_c * y_kc >= 0
        if l_cap > 1:
            rows.extend([row_idx] * (len(compat_x) + 1))
            cols.extend(compat_x + [yi])
            vals.extend([1.0] * len(compat_x) + [-float(l_cap)])
            lbs.append(0.0); ubs.append(np.inf); row_idx += 1

A = coo_matrix((vals, (rows, cols)), shape=(row_idx, total_vars)).tocsc()
res = milp(c=c_obj, integrality=np.ones(total_vars),
           bounds=Bounds(0, 1), constraints=LinearConstraint(A, lbs, ubs),
           options={"time_limit": 2.5, "mip_rel_gap": 0.005})
```

Khung dưới đây trích kết quả chạy thực tế từ tệp nhật ký tổng hợp `du_an_nhom20/simulation_results.json` khi chạy lệnh `uv run python du_an_nhom20/CatPlus_Sim_Opt_Model.py`:

```text
> uv run --with simpy --with scipy --with matplotlib python du_an_nhom20/CatPlus_Sim_Opt_Model.py
Running strict coupled baseline simulation (20 replications, N=60, M=10)...
Done! Baseline summary:
  [AS-IS] match_rate = 60.42% (±8.71%) | fit_matched = 96.75 | fit_all = 58.45
          wait_mean  = 22.56h (2.82d)  | P90 = 31.29h | SLA_16h = 18.00%
          rho_mgr    = 49.67% | WIP L  = 5.64 cases | lost = 23.75 (group_quorum: 17.50)
  [TO-BE] match_rate = 92.67% (±4.36%) | fit_matched = 93.28 | fit_all = 86.45
          wait_mean  = 10.29h (1.29d)  | P90 = 13.24h | SLA_16h = 99.25%
          rho_mgr    =  8.67% | WIP L  = 2.57 cases | lost =  4.40 (-81.5% closed_lost)
```

---

## 6 Kết quả so sánh các phương án

### 6.1 So sánh AS-IS và TO-BE

Bảng 6.1 và Hình 6.1 đối chiếu phương án xếp tay hiện tại (AS-IS) với ba cấu hình của phương án TO-BE khi CSKH thu thập tối đa 1, 2 hoặc 3 khung giờ rảnh từ phụ huynh trên cùng tập nhu cầu.

**Bảng 6.1.** So sánh phương án cơ sở (AS-IS) và các cấu hình TO-BE (*N* = 60 học viên/tháng, *M* = 10 gia sư)

| Phương án | *R*<sub>ghép</sub> (%) | *N*<sub>rớt</sub> (ca/tháng) | Fit<sub>ghép</sub> (điểm) | Fit<sub>chung</sub> (điểm) | *W* TB (giờ) | P90 (giờ) | SLA<sub>16h</sub> (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| AS-IS (xếp tay tuần tự) | 60,4 | 23,75 | 96,8 | 58,5 | 22,56 | 31,29 | 18,0 |
| TO-BE (MILP, chỉ hỏi 1 khung giờ) | 58,3 | 25,00 | 100,0 | 58,3 | 9,69 | 12,84 | 99,0 |
| TO-BE (MILP, hỏi tối đa 2 khung giờ) | 87,8 | 7,33 | 94,2 | 82,7 | 10,21 | 13,23 | 98,8 |
| **TO-BE (MILP, hỏi tối đa 3 khung giờ — đề xuất)** | **92,7** | **4,40** | **93,3** | **86,5** | **10,29** | **13,24** | **99,3** |

Bảng 6.1 làm sáng tỏ một phát hiện quản trị rất quan trọng: nếu CSKH chỉ hỏi đúng 1 khung giờ duy nhất rồi đưa vào thuật toán MILP (*TO-BE 1 khung giờ*), tỷ lệ ghép lớp chỉ đạt **58,3%** — không hơn gì cách xếp tay (60,4%), dù thời gian xử lý giảm nhờ bỏ vòng hỏi lại. Nguyên nhân là khi mỗi học sinh chỉ có 1 lựa chọn cố định, máy tính cũng không có khoảng linh hoạt nào để dồn các học sinh học nhóm về chung một ca đủ 3 người. Ngược lại, ngay khi CSKH khai thác được tối đa **2 khung giờ**, tỷ lệ ghép vọt lên **87,8%**, và đạt **92,7%** khi hỏi tối đa **3 khung giờ** (giảm lượng học viên rớt từ 23,75 xuống còn 4,40 em/tháng, tức giảm **81,5%**). Độ lệch chuẩn giữa các tháng cũng giảm một nửa (từ 8,7% xuống 4,4%), giúp doanh thu và lịch mở lớp của trung tâm ổn định hơn rõ rệt.

![So sánh ba chỉ số KPI trọng tâm giữa AS-IS và TO-BE](./fig1_as_is_vs_to_be_kpi.png)
*Hình 6.1. Đối chiếu ba chỉ số KPI cốt lõi giữa quy trình xếp tay hiện tại (AS-IS) và cấu hình đề xuất TO-BE (thu thập 1–3 khung giờ kết hợp gợi ý MILP).*

Về độ phù hợp lịch, Fit<sub>ghép</sub> của cấu hình đề xuất đạt 93,3 điểm, thấp hơn 3,5 điểm so với AS-IS (96,8 điểm) vì mô hình chủ động xếp một số học viên linh hoạt sang khung giờ ưu tiên số 2 (80 điểm) hoặc số 3 (60 điểm) để gom đủ nhóm 3–5 học viên và nhường ca hiếm cho các bạn chỉ rảnh 1 buổi. Đổi lại, điểm phù hợp tính trên toàn bộ khách đăng ký (Fit<sub>chung</sub>) tăng mạnh từ **58,5 lên 86,5 điểm** (+28,0 điểm). Đồng thời, thời gian chờ trung bình giảm **54,4%** (từ 22,56 xuống 10,29 giờ làm việc), nâng tỷ lệ hồ sơ chốt xong trong 2 ngày làm việc từ **18,0% lên 99,3%**.

### 6.2 Đánh đổi đa mục tiêu và đường biên Pareto

Trong thực tế vận hành, trung tâm luôn đứng trước sự đánh đổi giữa chất lượng phục vụ người học (tăng tỷ lệ nhận lớp) và chi phí nguồn lực nhà cung cấp (giảm số ca lớp gia sư phải mở). Bảng 6.2 và Hình 6.2a khảo sát đường biên Pareto bằng cách quét trọng số chi phí mở lớp *γ* trong hàm mục tiêu (4.2) từ 10 đến 1.105 (với *P* = 1.000).

**Bảng 6.2.** Đường biên đánh đổi Pareto giữa số ca gia sư phải mở và tỷ lệ ghép thành công khi thay đổi *γ*

| Trọng số chi phí mở lớp *γ* | Số ca lớp mở TB / tháng | *R*<sub>ghép</sub> (%) | Fit<sub>chung</sub> (điểm) | Ý nghĩa vận hành tương ứng với cấu hình nghiệm |
| :---: | :---: | :---: | :---: | :--- |
| *γ* = 10 | 33,25 | 91,3 | 84,9 | Mở tối đa cả lớp nhóm và lớp 1–1 ở mọi mức ưu tiên 1, 2, 3 |
| *γ* = 1.065 | 32,17 | 89,4 | 84,1 | Ngừng mở các lớp lẻ 1–1 rơi vào khung giờ ưu tiên 3 (*P* + 60 = 1.060 < *γ*) |
| *γ* = 1.085 | 29,67 | 85,3 | 80,7 | Chỉ mở lớp 1–1 nếu đạt ưu tiên 1; dồn tối đa học sinh vào các nhóm 4–5 người |
| *γ* = 1.105 | 8,92 | 50,7 | 46,1 | Ngừng mở hoàn toàn lớp 1–1 (*P* + 100 < *γ*); chỉ mở các lớp nhóm đông người |

Kết quả trên Bảng 6.2 minh họa rõ đặc tính "bước nhảy nghiệm nguyên": khi *γ* vượt qua ngưỡng lợi ích của một ca kèm 1–1 ở ưu tiên 3 (1.060), ưu tiên 2 (1.080) và ưu tiên 1 (1.100), cấu hình lớp mở thay đổi theo từng nấc rõ rệt. Ở mức *γ* = 1.085, trung tâm tiết kiệm được 3,6 ca gia sư mỗi tháng so với *γ* = 10 mà vẫn duy trì tỷ lệ ghép trên 85%. Trong khi đó, trên không gian hai mục tiêu chất lượng (Hình 6.2b), phương án xếp tay AS-IS (60,4%; 58,5 điểm) bị trội hoàn toàn (dominated) bởi cả hai cấu hình TO-BE 2 khung giờ và 3 khung giờ.

![Đường biên Pareto và kiểm định trội Pareto](./fig4_pareto_tradeoff.png)
*Hình 6.2. (a) Đường biên Pareto đánh đổi giữa số ca lớp gia sư phải mở và tỷ lệ ghép thành công; (b) Kiểm định trội Pareto giữa AS-IS và các cấu hình TO-BE.*

### 6.3 Độ ổn định và phân tích độ nhạy

Nhóm kiểm tra độ bền của khoảng cách cải thiện giữa TO-BE và AS-IS qua 11 kịch bản biến động nhu cầu, nhân sự gia sư và số khung giờ thu thập (Bảng 6.3 và Hình 6.3).

**Bảng 6.3.** Tỷ lệ ghép thành công (%) và hiệu số cải thiện (điểm %) theo các kịch bản độ nhạy

| Nhóm tham số khảo sát | Giá trị thử nghiệm | AS-IS (%) | TO-BE (%) | Hiệu số TO-BE − AS-IS | Tỷ lệ bận Quản lý *ρ*<sub>QL</sub> (AS-IS → TO-BE) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Lượng học viên *N* (*M* = 10) | 45 hồ sơ/tháng | 58,5 | 87,0 | +28,5 | 37,2% → 6,6% |
| Lượng học viên *N* (*M* = 10) | 60 hồ sơ/tháng (gốc) | 64,6 | 92,5 | +27,9 | 48,0% → 8,5% |
| Lượng học viên *N* (*M* = 10) | 75 hồ sơ/tháng | 64,6 | 91,6 | +27,0 | 62,4% → 10,7% |
| Lượng học viên *N* (*M* = 10) | 90 hồ sơ/tháng | 65,3 | 87,5 | +22,2 | 72,6% → 12,8% |
| Số gia sư *M* (*N* = 60) | 6 gia sư (thiếu hụt) | 50,1 | 75,3 | +25,2 | 54,8% → 8,5% |
| Số gia sư *M* (*N* = 60) | 8 gia sư | 56,3 | 85,4 | +29,1 | 52,3% → 8,6% |
| Số gia sư *M* (*N* = 60) | 10 gia sư | 63,1 | 93,9 | +30,8 | 47,8% → 8,5% |
| Số gia sư *M* (*N* = 60) | 12 gia sư | 62,2 | 91,9 | +29,7 | 48,0% → 8,5% |
| Số khung giờ hỏi tối đa *m* | *m* = 1 khung giờ | 60,8 | 58,3 | −2,5 | 49,4% → 8,5% |
| Số khung giờ hỏi tối đa *m* | *m* = 2 khung giờ | 60,8 | 87,8 | +27,0 | 49,4% → 8,5% |
| Số khung giờ hỏi tối đa *m* | *m* = 3 khung giờ | 60,8 | 92,1 | +31,3 | 49,4% → 8,5% |

Trong mọi kịch bản có thu thập từ 2 khung giờ trở lên, phương án TO-BE đều vượt AS-IS từ **+22,2 đến +31,3 điểm phần trăm**. Có hai hiện tượng thực tiễn rất đáng lưu ý trên Hình 6.3: thứ nhất, khi lượng đăng ký thấp (*N* = 45), tỷ lệ ghép của cả hai phương án đều thấp hơn mức *N* = 60 vì lượng học sinh thưa làm giảm xác suất có đủ 3 em trùng cấp học và khung giờ để mở lớp nhóm; khi nhu cầu tăng lên *N* = 90, tỷ lệ bận của Quản lý ở AS-IS vọt lên **72,6%** (tỷ lệ đạt chuẩn 2 ngày sụp xuống còn 10,8%), trong khi TO-BE vẫn giữ *ρ*<sub>QL</sub> ở mức nhẹ nhàng 12,8%. Thứ hai, ngay cả khi trung tâm chỉ còn **6 gia sư**, mô hình MILP vẫn ghép được **75,3%** học viên — cao hơn cả khi xếp bằng tay mà có tới **12 gia sư** (62,2%). Điều này khẳng định nút thắt nằm ở cơ chế gom nhóm hơn là thiếu hụt nhân sự đơn thuần.

![Phân tích độ nhạy trên ba chiều biến động](./fig3_sensitivity_analysis.png)
*Hình 6.3. Phân tích độ nhạy của tỷ lệ ghép thành công theo lượng học viên, số gia sư và số khung giờ thu thập.*

---

## 7 Đề xuất cải tiến (TO-BE)

### 7.1 Thay đổi trong quy trình

Phương án TO-BE giữ nguyên đội ngũ nhân sự (2 CSKH, 1 Quản lý học vụ, 10 gia sư) và tôn trọng triết lý lấy con người làm chủ của CatPlus: CSKH vẫn trực tiếp trò chuyện tư vấn với phụ huynh, và Quản lý học vụ vẫn là người kiểm duyệt cuối cùng trước khi mở lớp. Quy trình chỉ thay đổi ở ba điểm cốt lõi (Hình 7.1): (i) CSKH khai thác và nhập chuẩn hóa **1–3 khung giờ ưu tiên** của học sinh ngay trong cuộc gọi đầu tiên; (ii) Gia sư đánh dấu sẵn các ca trống cố định hằng tuần trên hệ thống; và (iii) Hệ thống tự động chạy mô hình MILP theo hai đợt mỗi ngày (11h30 và 17h30) để đề xuất danh sách ghép lớp tối ưu kèm phương án dự phòng cho Quản lý duyệt trong 1 vòng.

![Sơ đồ BPMN 2.0 quy trình TO-BE](./fig_bpmn_to_be.png)
*Hình 7.1. BPMN TO-BE của quy trình ghép đôi – xếp lịch có module MILP hỗ trợ ra quyết định (tệp chuẩn: `catplus_matching_to_be.bpmn`).*

Bảng 7.1 quy định quy tắc ra quyết định cụ thể cho Quản lý học vụ khi xử lý bảng đề xuất từ phần mềm.

**Bảng 7.1.** Bảng quyết định xử lý của Quản lý học vụ sau mỗi đợt chạy gợi ý MILP

| Tình huống trên bảng gợi ý của hệ thống | Hành động của Quản lý học vụ |
| :--- | :--- |
| Học viên được gợi ý vào lớp 1–1 hoặc nhóm đủ 3–5 em, gia sư xác nhận | Bấm duyệt tạo lớp học thử/chính thức; chuyển CSKH báo lịch chốt cho phụ huynh |
| Gia sư được gợi ý chính báo bận đột xuất (khoảng 8% trường hợp) | Chọn ngay phương án dự phòng số 2 trên màn hình mà không cần gọi hỏi lại phụ huynh |
| Nhóm gợi ý mới gom được 2 học viên có lịch rảnh trùng nhau | Giữ chờ thêm tối đa 1 đợt chạy kế tiếp (nửa ngày); nếu chưa đủ 3 em thì tư vấn chuyển sang 1–1 |
| Học viên rơi vào biến lớp ảo (*u*<sub>*i*</sub> = 1, lịch quá hẹp) | Nhận cảnh báo sớm ngay trong ngày đầu để CSKH chủ động thương lượng mở rộng khung giờ |

### 7.2 Lựa chọn cấu hình và lộ trình triển khai

Nhóm đề xuất chọn cấu hình **thu thập tối đa 3 khung giờ kết hợp trọng số ưu tiên nhận lớp (*P* = 1.000, *γ* = 0,05)** cho giai đoạn đầu vì mục tiêu sống còn của trung tâm đang tăng trưởng là giữ chân tối đa học viên đăng ký mới (*R*<sub>ghép</sub> = 92,7%) và cam kết phản hồi lịch trong 2 ngày (SLA<sub>16h</sub> = 99,3%). Khi đội ngũ gia sư gần chạm trần công suất vào mùa cao điểm ôn thi, Quản lý có thể nâng *γ* lên vùng 1.065–1.085 (Bảng 6.2) để ưu tiên dồn vào lớp nhóm. Lộ trình triển khai gồm hai bước gọn nhẹ:

1. **Bước 1 — Chuẩn hóa dữ liệu đầu vào (2 tuần đầu, chưa cần tích hợp sâu):** Cập nhật biểu mẫu tư vấn của CSKH để bắt buộc ghi nhận tối thiểu 2–3 khung giờ khả dụng của học viên theo thứ tự ưu tiên, đồng thời lập bảng đăng ký ca trống cố định hằng tuần cho 10 gia sư. Chỉ riêng việc có sẵn hai bảng dữ liệu chuẩn này đã loại bỏ được phần lớn tin nhắn hỏi dò trên Zalo.
2. **Bước 2 — Tích hợp module gợi ý MILP vào trang Quản lý (từ tuần thứ 3):** Nhúng hàm giải `solve_to_be_milp` (dùng thư viện mã nguồn mở `scipy` sẵn có trong môi trường Python/Django của CatPlus) thành một nút bấm *"Gợi ý xếp lớp đợt này"* trên màn hình của Quản lý học vụ; theo dõi song song với quyết định thực tế của Quản lý trong 1 tháng để tinh chỉnh trọng số.

### 7.3 Vai trò, nguồn lực và chỉ số theo dõi

Trong mô hình mới, phần mềm chuyển từ công cụ ghi chép thụ động sang nguồn lực tác động (operant resource) hỗ trợ tính toán tổ hợp, giải phóng hơn 80% thời gian dò lịch tay cho Quản lý học vụ để tập trung kiểm soát chất lượng chuyên môn. Để duy trì hiệu quả lâu dài, nhóm đề xuất bộ chỉ số theo dõi định kỳ dựa trên bốn góc nhìn của Thẻ điểm cân bằng (Balanced Scorecard, Bảng 7.2).

**Bảng 7.2.** Chỉ số theo dõi đề xuất sau khi áp dụng quy trình ghép lịch mới

| Góc nhìn quản trị | Chỉ số theo dõi | Cách tính và nguồn dữ liệu trên hệ thống | Tần suất |
| :--- | :--- | :--- | :--- |
| Người thụ hưởng (Học viên) | *R*<sub>ghép</sub>, SLA<sub>16h</sub> và Fit<sub>ghép</sub> | Tỷ lệ nhập học, % hồ sơ chốt ≤ 16h làm việc và điểm khớp lịch từ DB | Hằng tuần |
| Quy trình nội bộ | Tỷ lệ phải hỏi đổi lịch lại (Rework) | Phần trăm hồ sơ CSKH phải gọi lại phụ huynh xin đổi giờ sau lần đầu | Hằng tuần |
| Nguồn lực & Tài chính | Sĩ số trung bình lớp nhóm & ca thiếu người | Sĩ số TB các lớp nhóm mở mới (mục tiêu ≥ 3,8 em/lớp); thống kê ca có *u*<sub>*i*</sub> = 1 | Hằng tháng |
| Học hỏi & Phát triển | Tỷ lệ khớp giữa gợi ý MILP và duyệt thực tế | Tỷ lệ gợi ý được Quản lý giữ nguyên không phải sửa tay; cập nhật lại trọng số | Hằng quý |

### 7.4 Đánh đổi

Phương án cải tiến đi kèm bốn đánh đổi thực tế cần được trung tâm chấp nhận và quản trị rõ ràng. Thứ nhất, cuộc gọi tư vấn đầu tiên của CSKH sẽ kéo dài thêm khoảng 3–5 phút để khai thác kỹ 2–3 khung giờ rảnh của gia đình, đổi lại CSKH không phải gọi đi gọi lại xin đổi giờ ở các ngày sau. Thứ hai, việc gom hồ sơ chạy theo hai đợt mỗi ngày tạo ra độ trễ chờ gom đợt từ 1 đến 3,5 giờ làm việc, nhưng nhờ cắt bỏ vòng lặp nhắn tin Zalo nên tổng thời gian chờ của học viên vẫn giảm hơn một nửa (từ 22,56 xuống 10,29 giờ). Thứ ba, điểm phù hợp lịch tính riêng trên nhóm vào lớp giảm nhẹ 3,5 điểm (từ 96,8 xuống 93,3 điểm) do một số học viên linh hoạt được xếp sang lựa chọn ưu tiên 2 hoặc 3 nhằm gom đủ nhóm 3–5 người để cứu thêm 32,3% học viên khác. Cuối cùng, hiệu quả của mô hình phụ thuộc vào kỷ luật cập nhật lịch trống hằng tuần của đội ngũ gia sư.

---

## 8 Kết luận

### 8.1 Trả lời câu hỏi phân tích

**Q1. Tỷ lệ ghép lớp thành công và vai trò của số khung giờ thu thập.** Trên cùng đội ngũ 10 gia sư và quy định cứng lớp nhóm 3–5 học viên, phương án TO-BE nâng tỷ lệ ghép thành công từ **60,4% lên 92,7%** (+32,3 điểm phần trăm), giảm số học viên bị rớt mỗi tháng từ 23,75 xuống 4,40 em (−81,5%). Phân tích độ nhạy chứng minh điều kiện tiên quyết là CSKH phải thu thập được tối thiểu **2 đến 3 khung giờ khả dụng** của học sinh (nếu chỉ hỏi 1 khung giờ, MILP chỉ đạt 58,3%).

**Q2. Đánh đổi về độ phù hợp lịch học.** Để gom các học sinh rời rạc thành các nhóm đủ từ 3 đến 5 người, mô hình điều phối một phần học viên linh hoạt sang khung giờ ưu tiên 2 hoặc 3, làm điểm phù hợp trên tập vào lớp giảm nhẹ 3,5 điểm (96,8 xuống 93,3 điểm), nhưng nâng điểm phù hợp chung trên toàn bộ học viên đăng ký tăng thêm **+28,0 điểm** (từ 58,5 lên 86,5 điểm) và trội Pareto hoàn toàn so với cách xếp tay.

**Q3. Thời gian chờ học viên và tải nhân sự.** Mô phỏng hàng đợi gắn kết cho thấy thời gian chờ trung bình giảm **54,4%** (từ 22,56 xuống 10,29 giờ làm việc, tức từ 2,82 xuống 1,29 ngày), phân vị P90 giảm **57,7%** (từ 31,29 xuống 13,24 giờ), nâng tỷ lệ chốt lịch trong 2 ngày làm việc từ **18,0% lên 99,3%**. Số hồ sơ ứ đọng trung bình giảm từ 5,64 xuống 2,57 hồ sơ, đồng thời giải phóng tỷ lệ bận thủ công của Quản lý học vụ từ **49,7% xuống còn 8,7%**.

Từ góc độ khoa học dịch vụ, nghiên cứu cho thấy trung tâm đào tạo có thể tăng mạnh số lớp khai giảng và rút ngắn hơn một nửa thời gian chờ mà chưa cần tuyển thêm gia sư hay thay thế vai trò tư vấn của con người, chỉ bằng cách chuẩn hóa thông tin đầu vào của khách hàng (UST) và bổ sung công cụ tối ưu hóa như một nguồn lực tác động (SDL) hỗ trợ Quản lý ra quyết định.

### 8.2 Giới hạn

- Các con số định lượng hiện tại được tính trên bộ dữ liệu mô phỏng tái lập (`seed = 42`); dù cấu trúc lớp và quy trình bám sát hệ thống CatPlus, phân phối xác suất chọn từng khung giờ trong tuần vẫn là giả định cần được hiệu chỉnh lại bằng dữ liệu lịch sử thật.
- Mô hình hiện xét từng đợt độc lập với quy định lớp nhóm mở mới phải đủ 3–5 học viên, chưa mô hình hóa chi tiết việc ghép bổ sung học viên mới vào các lớp nhóm cũ đang học dở chương trình.
- Các yếu tố định tính ngoài khung giờ và cấp học (như phong cách truyền đạt của từng gia sư hay yêu cầu chọn thầy quen của phụ huynh) chưa được đưa vào hàm mục tiêu mà phụ thuộc bước duyệt cuối của Quản lý học vụ.

### 8.3 Hướng phát triển

- Chạy kịch bản trích xuất dữ liệu ẩn danh `export_real_data_template.py` trên máy chủ sản xuất của CatPlus ngay khi hoàn tất nhập liệu để hiệu chỉnh lại phân phối nhu cầu theo giờ và kiểm định đối chứng ngoài mẫu giữa các tháng.
- Mở rộng mô hình MILP cho phép ghép xen kẽ học viên mới vào các lớp nhóm đang hoạt động có sĩ số 3–4 em và cùng tiến độ chuyên đề.
- Sử dụng thống kê các ca rơi vào biến lớp ảo (*u*<sub>*i*</sub> = 1) theo từng khung giờ để thiết kế chính sách phụ cấp khuyến khích gia sư mở thêm ca dạy vào các khung giờ cao điểm cuối tuần.

---

## Tài liệu tham khảo

[1] Steven Alter. Work System Theory: Overview of Core Concepts, Extensions, and Challenges for the Future. *Journal of the Association for Information Systems*, 14(2):72–121, 2013. doi: 10.17705/1jais.00323.

[2] Stephen L. Vargo and Robert F. Lusch. Institutions and axioms: an extension and update of service-dominant logic. *Journal of the Academy of Marketing Science*, 44(1):5–23, 2016. doi: 10.1007/s11747-015-0456-3.

[3] Scott E. Sampson and Craig M. Froehle. Foundations and Implications of a Proposed Unified Services Theory. *Production and Operations Management*, 15(2):329–343, 2006. doi: 10.1111/j.1937-5956.2006.tb00248.x.

[4] John D. C. Little. A Proof for the Queuing Formula: *L* = *λW*. *Operations Research*, 9(3):383–387, 1961. doi: 10.1287/opre.9.3.383.

[5] Mark S. Daskin. *Service Science*. John Wiley & Sons, Hoboken, NJ, 2010. doi: 10.1002/9780470877876.

[6] Q. Huangfu and J. A. J. Hall. Parallelizing the dual revised simplex method. *Mathematical Programming Computation*, 10(1):119–142, 2018. (Bộ giải quy hoạch nguyên HiGHS trong `scipy.optimize.milp`).

[7] Team SimPy. SimPy: Discrete event simulation for Python. `https://simpy.readthedocs.io/`, 2026. Truy cập ngày 23/11/2026.

[8] Object Management Group (OMG). Business Process Model and Notation (BPMN), Version 2.0.2. `https://www.omg.org/spec/BPMN/2.0.2/`, 2014.

---

## Phụ lục: Khai báo minh bạch sử dụng AI

Thực hiện quy định tại Mục 11 của Hướng dẫn dự án học phần INT3501, Nhóm 20 công bố chi tiết phạm vi sử dụng công cụ AI hỗ trợ và quy trình tự kiểm chứng của nhóm đối với từng thành phần trong báo cáo tại Bảng A.1. Nhóm phân biệt rõ ràng giữa kiến trúc nghiệp vụ thật của nền tảng CatPlus và bộ số liệu mô phỏng tái lập (`seed = 42`), tuyệt đối không trình bày dữ liệu giả lập như số liệu thu thập thực tế.

**Bảng A.1.** Bảng khai báo sử dụng AI theo từng thành phần và cách nhóm kiểm chứng

| Thành phần | Dùng AI? | Phần AI hỗ trợ và công cụ | Cách nhóm tự kiểm chứng |
| :--- | :---: | :--- | :--- |
| Văn bản, lập luận, tổng quan | Có | AI hỗ trợ rà soát bố cục 8 mục theo mẫu báo cáo học phần và biên tập câu chữ mạch lạc | Nhóm đối chiếu toàn bộ nội dung với quy trình thực tế của CSKH, Quản lý tại CatPlus và tài liệu gốc [1]–[8] |
| Ảnh và hình minh họa | Không | Không dùng AI sinh ảnh giả lập; cả 6 biểu đồ kết quả đều xuất trực tiếp từ mã chạy Python | Kiểm tra trực quan độ phân giải, phông chữ tiếng Việt và đối chiếu khớp với tệp kết quả JSON |
| Sơ đồ BPMN, bản đồ nguồn lực | Có | AI hỗ trợ sinh khung XML cho 2 tệp `.bpmn` và mã vẽ Matplotlib cho Hình 2.1, 3.1, 7.1 | Nhóm mở kiểm tra trên `https://demo.bpmn.io/new`, rà soát đủ Pool/Lane, Message Flow, cổng XOR và ngoại lệ |
| Bảng, biểu đồ, số liệu | Có | AI hỗ trợ viết hàm xuất thống kê trung bình 20 chu kỳ tháng sang `simulation_results.json` | Ghi chú rõ nguồn dữ liệu mô phỏng tái lập; tự tính kiểm tra lại Định luật Little (*L* = 0,25 × *W*) và các hiệu số |
| Công thức, mô hình, mô phỏng | Có | AI hỗ trợ chuyển quy định lớp 1–1 và lớp nhóm 3–5 học viên sang hệ ràng buộc MILP và SimPy | Kiểm tra từng bất đẳng thức (4.2)–(4.5), xác nhận tính hợp lý của 11 kịch bản độ nhạy và đường biên Pareto |
| Mã nguồn thực nghiệm | Có | AI hỗ trợ viết `CatPlus_Sim_Opt_Model.py`, `export_real_data_template.py` và mã xuất PDF/DOCX | Nhóm trực tiếp chạy kiểm thử không lỗi toàn bộ tệp `.py` và đối chiếu khớp tên bảng/trường với dự án CatPlus |
