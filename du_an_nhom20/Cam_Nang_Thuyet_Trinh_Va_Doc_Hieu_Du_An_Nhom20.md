# TÀI LIỆU GIẢI NGHĨA BẢN CHẤT: KHOA HỌC DỊCH VỤ & MÔ HÌNH TỐI ƯU – MÔ PHỎNG CATPLUS

**Đề tài Nhóm 20:** Tối ưu hóa quy trình ghép đôi gia sư – học viên và xếp lịch học trên nền tảng CatPlus  
**Học phần:** Khoa học dịch vụ (INT3501) — Trường Đại học Công nghệ, ĐHQGHN  
**Thành viên:** Phoutthavong Xayavong (`23021941`) · Vũ Quốc Long (`23020105`)

> **Tinh thần của tài liệu này — Đọc để Hiểu Sâu từ Gốc (Không Học Vẹt):** Tài liệu này không viết lời thoại để bạn đọc thuộc lòng, mà giải thích tận gốc **tại sao** môn Khoa học dịch vụ lại nhìn vấn đề theo cách đó, **tại sao** quy trình xếp lịch của CatPlus lại bị tắc về mặt vật lý – xác suất, **tại sao** từng công thức toán học và mô phỏng trong báo cáo lại được viết như vậy, và các con số ở từng bảng sinh ra từ cơ chế nào. Khi bạn hiểu thấu bản chất nhân – quả bên dưới, bạn có thể tự diễn đạt bằng lời của mình một cách tự nhiên và bình tĩnh phân tích mọi câu hỏi bất ngờ của giảng viên.

---

## CHƯƠNG 1. BẢN CHẤT MÔN "KHOA HỌC DỊCH VỤ" — TẠI SAO DỊCH VỤ KHÁC SẢN XUẤT NHÀ MÁY?

Để đọc hiểu Mục 1 và Mục 2 của báo cáo mà không thấy các thuật ngữ lý thuyết bị "kêu" hay trừu tượng, trước hết cần nắm được câu hỏi gốc của môn học **INT3501**: *Tại sao cách quản lý một nhà máy sản xuất điện thoại lại thất bại khi đem áp vào một bệnh viện, ngân hàng hay trung tâm giáo dục như CatPlus?*

### 1.1. Sự khác biệt cốt lõi giữa "Sản xuất hàng hóa" và "Hệ thống dịch vụ"
Trong nhà máy sản xuất điện thoại, dây chuyền chạy khép kín không cần mặt mũi khách hàng ở đó; làm dư hôm nay có thể cất vào kho để tuần sau bán. Ngược lại, dịch vụ đào tạo có **hai đặc tính vật lý** chi phối toàn bộ bài toán của chúng ta:

1. **Năng lực phục vụ gắn chặt với chiều thời gian (Time-perishable capacity — Giáo trình Qiu, Bài L1):** Một gia sư rảnh vào ca tối Thứ Ba từ `19h45 – 21h15`. Nếu đến `19h45` tối Thứ Ba mà chưa xếp được lớp cho gia sư đó, 90 phút năng lực giảng dạy ấy **biến mất vĩnh viễn** — không thể đóng hộp cất đi để mang sang bù cho tối Chủ nhật đang quá tải.
2. **Nhưng dừng ở chữ "không lưu kho" là chưa đủ (Phê biện IHIP — Bài L2A):** Trước đây kinh tế học cổ điển hay đổ lỗi cho 4 chữ *IHIP* (*vô hình, không đồng nhất, không tách rời, không lưu kho*). Bài giảng L2A chỉ ra rằng nếu chỉ nói *"tại dịch vụ không lưu kho được nên khách phải chịu khó chờ"* thì người kỹ sư chẳng làm được gì cả! **Khoa học dịch vụ hiện đại** nhìn dịch vụ như một **Hệ thống xã hội – kỹ thuật (Socio-technical system)**: hiệu quả không tự nhiên rơi xuống từ công nghệ hay con người riêng lẻ, mà sinh ra từ **độ ăn khớp** giữa 4 yếu tố: *Con người – Quy trình – Thông tin – Công nghệ*. Khi dịch vụ chậm hoặc mất khách, lỗi hầu như luôn nằm ở **cấu trúc phối hợp của hệ thống**, không phải do nhân viên lười biếng.

### 1.2. Hiểu thấu 4 trụ cột lý thuyết dùng trong Mục 2 của Báo cáo

Trong báo cáo, nhóm dùng **1 khung chính** (*Work System Framework*) và **3 lăng kính bổ trợ** (*SDL, UST, Chuỗi giá trị*). Bản chất của từng cái như sau:

#### (1) Khung Hệ thống làm việc — Work System Framework (WSF, Bài L2B)
Hãy hình dung bất kỳ bộ phận dịch vụ nào cũng giống như một cỗ máy gồm **9 mảnh ghép chia làm 3 tầng**:
- **Tầng ruột vận hành (4 mảnh ghép tương tác trực tiếp hằng ngày):** **Hoạt động & Quy trình** (các bước làm việc) do **Người tham gia** (CSKH, Quản lý, Gia sư) thực hiện, dựa trên **Thông tin** (lịch rảnh, trình độ) và chạy trên **Công nghệ** (web nội bộ, Zalo). *Chỉ cần 1 trong 4 mảnh này lệch nhịp với 3 mảnh kia là cả hệ thống kẹt!*
- **Tầng hướng ra ngoài (2 mảnh ghép mục đích):** Hệ thống trên tạo ra **Sản phẩm & Dịch vụ** (lớp học thử, lớp chính thức) dành cho **Khách hàng** (học sinh & phụ huynh).
- **Tầng nền móng bao quanh (3 mảnh ghép bối cảnh):** Phải vận hành dưới định hướng của **Chiến lược** công ty, dựa trên **Hạ tầng** sẵn có (mạng, phòng học Meet/Zoom), và chịu sức ép từ **Môi trường bên ngoài** (học sinh phổ thông đi học văn hóa kín ngày thường, chỉ rảnh dồn vào buổi tối và cuối tuần).

Từ khung 9 mảnh ghép này, môn học phân loại mọi trục trặc vận hành thành **4 loại lỗi hệ thống** (Mục 2.1 báo cáo):
- **Lỗi thông tin:** Dữ liệu cần để ra quyết định bị thiếu hoặc nằm tản mát (CSKH chỉ hỏi 1 khung giờ; lịch gia sư nằm rải rác trong tin nhắn Zalo cá nhân).
- **Lỗi hoạt động:** Cách thức xử lý công việc tạo ra lãng phí (xếp lẻ từng người ai đến trước làm trước khiến các nhóm bị xé vụn).
- **Lỗi công nghệ:** Phần mềm chưa hỗ trợ đúng chỗ khó (web chỉ dùng để gõ lưu kết quả sau khi người đã tự vắt óc dò lịch xong).
- **Lỗi thiết chế:** Thiếu quy tắc phối hợp chuẩn (chưa có lịch chốt ca trống đầu tuần và nhịp gom đợt cố định).

#### (2) Logic hướng dịch vụ (SDL — Bài L2A & L2B): Toán hạng, Toán tử và Thiết chế
- **Tài nguyên Toán hạng (Operand) vs. Toán tử (Operant):** Hãy nhớ lại phép cộng `2 + 3 = 5`. Con số `2` và `3` nằm im chịu sự tác động gọi là *toán hạng*; còn phép toán `+` chủ động biến đổi chúng thành `5` gọi là *toán tử*. Trong khâu xếp lớp: hồ sơ đăng ký của học sinh và các ô giờ trống trên lịch chỉ là nguyên liệu tĩnh (**Toán hạng**). Chúng vô giá trị nếu thiếu kỹ năng hỏi lịch của CSKH, kinh nghiệm ghép trình độ của Quản lý, tri thức dạy học của Gia sư và thuật toán tối ưu (**Toán tử**). *Ý nghĩa cốt lõi:* Khi trung tâm chỉ có 10 gia sư (toán hạng hữu hạn), ta vẫn tăng vọt được lượng lớp mở thành công bằng cách nâng cấp **toán tử** (thêm quy tắc thu thập thông tin và thuật toán gom nhóm)!
- **Thiết chế (Institutions — Tiên đề 5 của SDL mở rộng):** "Thiết chế" không phải là cơ quan nhà nước, mà là **các luật chơi, quy định chung** để hệ thống vận hành không hỗn loạn. Ở CatPlus, quy định *"Lớp 1–1 đúng 1 em; Lớp nhóm bắt buộc từ 3 đến 5 em cùng cấp học"* chính là một thiết chế: nó bảo vệ chất lượng học tập (không nhồi quá 5 em) và bảo vệ tài chính trung tâm (không mở lớp nhóm 1–2 em gây lỗ lương gia sư). Nhưng bài giảng L2B nhấn mạnh: nếu thiết chế đặt ra ngưỡng 3–5 người mà quy trình thu thập thông tin lại rời rạc từng người một, thì chính thiết chế đó sẽ làm nghẽn hệ thống!

#### (3) Lý thuyết dịch vụ thống nhất (UST — Bài L2B): Khách hàng là nhà cung cấp đầu vào
Điểm làm dịch vụ khác hẳn nhà máy theo Sampson & Froehle (UST) là: **Muốn quy trình dịch vụ chạy được, khách hàng bắt buộc phải tự đưa đầu vào của họ vào hệ thống** (con người họ, tài sản của họ, hoặc thông tin của họ). Ở CatPlus, đầu vào khách hàng đưa vào là *cấp học* và *danh sách khung giờ rảnh*. Nếu đầu vào này quá hẹp (chỉ cho biết 1 khung giờ duy nhất), mọi khâu phía sau đều bị khóa cứng. Đây là lý do lý thuyết giải thích vì sao thay đổi biểu mẫu hỏi của CSKH từ 1 khung giờ lên 2–3 khung giờ lại tạo ra bước ngoặt từ `58,3%` lên `92,7%`.

#### (4) Phân biệt rạch ròi: Đầu ra (Output) ≠ Kết quả (Outcome) ≠ Giá trị (Value-in-context)
Người làm kỹ thuật phần mềm rất dễ nhầm: *"Hệ thống tạo được bản ghi lớp học mới trong cơ sở dữ liệu là xong!"*. Trong Khoa học dịch vụ:
- Bản ghi mã lớp trên phần mềm chỉ là **Đầu ra kỹ thuật (Output)** — tự nó chưa mang lại lợi ích gì.
- Học sinh thực sự bước vào được lớp đúng trình độ, lịch học vừa vặn với sinh hoạt gia đình và không phải mỏi cổ chờ đợi nhiều ngày mới là **Kết quả dịch vụ (Outcome)** — đây là nơi bộ 3 KPI của báo cáo đo lường!
- Từ kết quả đó, học sinh học hiểu bài, phát triển tư duy thuật toán, đạt giải thi học sinh giỏi và bố mẹ yên tâm lâu dài mới là **Giá trị trong bối cảnh đời sống của khách (Value-in-context)**.

---

## CHƯƠNG 2. GIẢI PHẪU HỆ THỐNG CATPLUS & BẢN CHẤT VẬT LÝ CỦA ĐIỂM NGHẼN

Chương này giúp bạn hiểu rõ thực tế dự án CatPlus đang vận hành thế nào và **tại sao con số rớt lớp ~40% lại tất yếu xảy ra về mặt toán học** khi làm thủ công.

### 2.1. Luồng vận hành thật trên nền tảng CatPlus
Trên hệ thống CatPlus thực tế, hai mảng nghiệp vụ liên quan trực tiếp đến đề tài là:
1. **Hành trình chuyển đổi học viên (Customer Operations):** Mỗi học sinh từ lúc phụ huynh để lại số điện thoại sẽ đi qua các trạng thái: *Chưa liên hệ* → *Chờ kiểm tra đầu vào / tư vấn* → *Chờ xếp học thử* → *Chờ xếp lớp chính thức* → Kết thúc ở **Đã tham gia** (thành công) hoặc **Đóng thất bại** (rớt khách, với hai lý do phổ biến nhất ghi nhận trên hệ thống là *lệch lịch học* hoặc *trung tâm chưa gom đủ lớp/thiếu gia sư*).
2. **Quản lý lớp học và lịch dạy (Academic):** Quản lý hai cấu hình cứng:
   - Lớp kèm riêng (`1–1`): Sĩ số bắt buộc bằng `1`.
   - Lớp nhóm nhỏ (`Group`): Sĩ số bắt buộc từ `3` đến `5` học sinh cùng khối cấp (**THCS** học riêng chương trình cơ bản/Scratch/Python cơ sở; **THPT** học riêng cấu trúc dữ liệu/thuật toán thi đấu — không ghép lẫn hai cấp học này vào chung 1 nhóm được).

Hiện tại, phần mềm CatPlus đóng vai trò **hệ thống lưu trữ hồ sơ**, còn toàn bộ trí tuệ điều phối nằm ở con người: CSKH gọi điện hỏi phụ huynh → ghi chú lại → đẩy sang Quản lý học vụ → Quản lý mở bảng danh sách lớp ra dò bằng mắt, rồi mở Zalo nhắn hỏi từng gia sư xem giờ đó có nhận dạy được không.

### 2.2. Phép tính xác suất giải thích gốc rễ "Tại sao xếp tay lại làm rớt lớp hàng loạt?"
Bạn không cần học thuộc con số `60,4%` hay `39,6%` một cách máy móc. Hãy tự nhẩm phép chia mật độ cực kỳ đơn giản sau đây, bạn sẽ hiểu ngay vì sao quy trình hiện tại (`AS-IS`) chắc chắn bị vỡ trận ở mảng lớp nhóm:

- Trung bình 1 tháng có **60 học sinh mới**:
  - `40%` (`24` em) đăng ký học **1–1**: Nhóm này dễ xếp, vì chỉ cần tìm được 1 gia sư còn trống ở khung giờ em đó chọn là mở lớp được ngay.
  - `60%` (`36` em) đăng ký học **Nhóm (3–5 người)**: Nhóm này chia làm 2 cấp học không trộn lẫn được: khoảng **20 em THCS** (`55%`) và **16 em THPT** (`45%`).
- Một tuần có **14 khung giờ học** (10 ca buổi tối Thứ 2 đến Thứ 6 + 4 ca Thứ 7, Chủ nhật).
- Bây giờ, hãy xem điều gì xảy ra ở quy trình hiện tại (`AS-IS`) khi **CSKH chỉ hỏi đúng 1 khung giờ ưa thích nhất** của mỗi em:
  - **20 em THCS** rải ngẫu nhiên vào **14 khung giờ** → Mật độ trung bình mỗi khung giờ chỉ là: `20 ÷ 14 ≈ 1,43 học sinh / khung giờ`!
  - **16 em THPT** rải ngẫu nhiên vào **14 khung giờ** → Mật độ trung bình mỗi khung giờ chỉ là: `16 ÷ 14 ≈ 1,14 học sinh / khung giờ`!
- Trong khi đó, luật cứng của trung tâm là **phải gom đủ từ 3 học sinh trở lên trong cùng 1 khung giờ** mới được mở lớp nhóm!
- Khi mật độ trung bình chỉ đạt `1,1` đến `1,4` em/ca, chuyện gì tất yếu xảy ra? Chỉ có 2–3 khung giờ "cao điểm cuối tuần" (như tối Thứ Bảy, chiều Chủ nhật) là tình cờ có 3–4 em chọn trùng nhau nên mở được lớp. Còn lại hàng chục khung giờ tối ngày thường rơi vào cảnh: *Tối Thứ Ba có 2 bạn THCS, Tối Thứ Tư có 1 bạn THCS, Tối Thứ Năm có 2 bạn THCS...* Không ca nào chạm ngưỡng `3`!
- Dù Quản lý học vụ ở bước sau có cố gọi lại năn nỉ phụ huynh đổi giờ (tối đa 2 vòng), nhưng vì **làm tuần tự từng hồ sơ lẻ** (hôm nay hỏi em A, hai hôm sau em B mới nộp đơn) và **không nhìn thấy toàn cục mạng lưới lịch rảnh của tất cả học sinh cùng lúc**, trung bình mỗi tháng vẫn có **`17,50` học sinh bị rớt chỉ vì lớp nhóm gom không đủ 3 người**, cộng thêm **`6,25` học sinh bị rớt do trùng/hết ca gia sư** = tổng cộng **`23,75 / 60` học sinh rớt lớp (`39,6%`)**, chỉ ghép thành công được **`60,4%`**.

> **Chìa khóa nhận thức số 1:** Nút thắt của CatPlus **không phải do thiếu gia sư** (10 gia sư, mỗi người dạy 3–5 lớp = tổng công suất 35–40 lớp, thừa sức chứa hơn 100 học sinh nếu gom được nhóm!), mà do **mật độ thông tin đầu vào quá mỏng (1 khung giờ/em)** kết hợp với **cách xếp lẻ từng người làm phân mảnh các nhóm dưới ngưỡng 3 học viên**. Hiểu được điều này, bạn đã nắm được linh hồn của toàn bộ đề tài!

---

## CHƯƠNG 3. HIỂU SÂU QUY TRÌNH BPMN 2.0 & LÝ THUYẾT HÀNG ĐỢI (MỤC 3 BÁO CÁO)

### 3.1. Tư duy đằng sau sơ đồ BPMN 2.0 (Tại sao lại vẽ như Hình 3.1 và Hình 7.1?)
BPMN 2.0 (Bài giảng L3B) không phải là vẽ lưu đồ tự do cho đẹp, mà là một **ngôn ngữ kỹ thuật có luật chặt chẽ** để nhìn vào là biết ngay *ai chịu trách nhiệm bước nào, chỗ nào phải chờ người ngoài, chỗ nào bị lặp lại*:

1. **Đơn vị quy trình (Process Instance) là gì?** Khi vẽ BPMN, sai lầm hay gặp nhất là trộn lẫn việc làm một lần mỗi tuần với việc làm cho từng khách hàng. Trong báo cáo, nhóm xác định rõ 1 lượt chạy của sơ đồ là vòng đời của **01 yêu cầu đăng ký học của học viên mới**, đi từ lúc gửi form đăng ký (sự kiện bắt đầu hình tròn nét mảnh) đến lúc *Nhập học thành công* hoặc *Đóng hồ sơ thất bại* (sự kiện kết thúc hình tròn nét đậm).
2. **Tại sao tách 3 Pool nhưng trong Pool CatPlus lại chia 3 Lane?**
   - **Pool (Bể bơi)** đại diện cho các chủ thể **độc lập về quyền điều hành**: *Phụ huynh & Học viên* (khách hàng bên ngoài), *Vận hành CatPlus* (trung tâm), và *Gia sư* (giảng viên cộng tác viên độc lập, trung tâm không thể ra lệnh cưỡng bức máy móc mà phải gửi đề xuất và chờ xác nhận). Trong chuẩn BPMN, hai Pool độc lập **cấm tuyệt đối nối bằng mũi tên nét liền**, mà bắt buộc giao tiếp bằng **mũi tên nét đứt (Message Flow — Luồng thông điệp)** như gọi điện, nhắn Zalo, gửi thông báo.
   - **Lane (Làn bơi)** là các bộ phận **nội bộ chung một tổ chức** (*CSKH*, *Quản lý học vụ*, *Hệ thống phần mềm* cùng nằm trong Pool CatPlus). Công việc chuyển từ CSKH sang Quản lý là bàn giao nội bộ nên dùng **mũi tên nét liền (Sequence Flow — Luồng trình tự)**. Mỗi lần mũi tên nét liền vắt qua vạch ngăn giữa 2 Lane chính là một điểm **Chuyển giao (Handoff)** dễ gây trễ!
3. **Tại sao không vẽ ô chữ nhật "Chờ gia sư trả lời" mà phải vẽ Hình tròn đôi?**
   - Ô chữ nhật (*Task / Activity*) chỉ dùng khi nhân sự đang **tiêu tốn công sức làm việc** (gọi điện, dò bảng lịch, tạo lớp). Còn lúc nhắn Zalo xong và ngồi đợi gia sư hồi âm, Quản lý không hề ngồi nhìn chằm chằm màn hình suốt 5 tiếng (họ đi làm việc khác, còn hồ sơ nằm im đợi!). Do đó, chuẩn BPMN bắt buộc biểu diễn chỗ chờ bằng **Sự kiện trung gian bắt thông điệp** (hình tròn viền đôi có ký hiệu thư) gắn kèm **Sự kiện biên đếm giờ (Timer — hình đồng hồ 8h, 24h)**: nếu trong hạn mà nhận được tin trả lời thì đi tiếp; nếu quá 8h gia sư im lặng hoặc quá 24h không gọi được phụ huynh thì đồng hồ tự kích hoạt nhánh xử lý ngoại lệ!
4. **Cổng loại trừ `XOR` (hình thoi có dấu `×`):** Nghĩa là tại ngã rẽ đó, hồ sơ **chỉ đi theo đúng 1 nhánh duy nhất** thỏa điều kiện (ví dụ: *Khớp gia sư & đủ nhóm 3–5 em?* → Đúng thì đi thẳng tạo lớp; Sai thì rẽ sang kiểm tra *Đã thử quá 2 vòng chưa?* → Chưa quá 2 vòng thì vòng ngược lên CSKH tạo thành **vòng lặp làm lại — Rework**).

### 3.2. Hiểu bản chất Phép đo Thời gian, Định luật Little & Mô phỏng SimPy
Nhiều người đọc Mục 3.2 và 3.3 hay thắc mắc: *Giờ làm việc tính thế nào? Định luật Little ý nghĩa gì? Sao Quản lý bận 49,7% mà khách phải chờ tới gần 3 ngày?* Hãy tháo gỡ từng mắt xích:

1. **Quy ước "Giờ làm việc" (Working hours):** Trung tâm không gọi điện tư vấn hay nhắn xếp lớp lúc 2 giờ sáng! Báo cáo quy ước **1 ngày làm việc = 8 giờ làm việc hành chính**, và **1 tháng (30 ngày) = 240 giờ làm việc**. Vì vậy:
   - Thời gian chờ trung bình `W = 22,56 giờ làm việc` chính là `22,56 ÷ 8 = 2,82 ngày làm việc` (gần 3 ngày!).
   - Ngưỡng cam kết dịch vụ (**SLA ≤ 16 giờ làm việc**) chính là cam kết chốt xong lịch cho phụ huynh trong vòng **2 ngày làm việc** (`2 × 8 = 16 giờ`). Ở `AS-IS`, chỉ có `18,0%` hồ sơ đạt chuẩn này; sang `TO-BE`, `99,3%` hồ sơ đạt chuẩn!
   - **Phân vị P90 (`31,29 giờ` ở AS-IS → `13,24 giờ` ở TO-BE):** Trung bình cộng đôi khi đánh lừa cảm giác. `P90 = 31,29 giờ` cho biết: nếu xếp 100 hồ sơ từ nhanh nhất đến chậm nhất, người đứng thứ 90 phải chờ tới **31,29 giờ (~3,9 ngày)**, và 10% khách xui xẻo nhất còn phải chờ lâu hơn thế! Kéo `P90` xuống `13,24 giờ` nghĩa là ngay cả những ca khó ở nhóm 90% cũng được giải quyết gọn dưới 2 ngày làm việc.

2. **Bóc tách 3 chặng ở Bảng 3.1 để bác bỏ nhận định cảm tính:**
   - Khi thấy khách chờ gần 3 ngày, phản xạ tự nhiên của các sếp thường là mắng bộ phận đầu phễu: *"Sao các bạn CSKH gọi khách chậm thế?"*.
   - Bảng 3.1 đo đạc riêng từng chặng trên tổng `22,56 giờ`:
     - **Chặng 1 (CSKH gọi tư vấn lần đầu):** Chỉ mất trung bình **`1,95 giờ` (`8,6%`)** — kể cả tính 30% trường hợp phụ huynh bận máy phải đợi vài tiếng gọi lại.
     - **Chặng 2 (Quản lý dò lịch, đợi Zalo gia sư & vòng lặp xin đổi giờ):** Ngốn tới **`15,66 giờ` (`69,4%`)**!
     - **Chặng 3 (Xác nhận chéo lần cuối trước buổi học thử):** Mất **`4,96 giờ` (`22,0%`)**.
   - Như vậy, con số chứng minh đanh thép: nút cổ chai nằm ở **cơ chế trao đổi bất đồng bộ qua Zalo và vòng lặp làm lại ở Chặng 2**, hoàn toàn không phải lỗi do CSKH lề mề!

3. **Trực giác đằng sau Định luật Little (`L = λ × W` — Công thức 3.1):**
   - Tốc độ hồ sơ mới đổ vào trung tâm là: `λ = 60 hồ sơ ÷ 240 giờ = 0,25 hồ sơ/giờ` (cứ 4 tiếng có 1 khách đăng ký mới).
   - Hãy tưởng tượng đường ống xử lý hồ sơ giống như một trạm thu phí: cứ mỗi giờ có `0,25` xe đi vào, và mỗi xe phải lưu lại trong trạm trung bình `W = 22,56` giờ mới thoát ra được. Vậy tại bất kỳ thời điểm nào bạn chụp ảnh trạm đó, số xe đang nằm kẹt bên trong trạm trung bình là:
     `L = λ × W = 0,25 × 22,56 = 5,64 hồ sơ`.
   - Cái hay nhất của **Định luật Little** (Bài giảng L4 nhấn mạnh) là nó **đúng cho mọi hệ thống ổn định bất kể quy trình bên trong rẽ nhánh phức tạp thế nào**! Khi `TO-BE` rút `W` xuống còn `10,29 giờ`, lượng hồ sơ tồn đọng trên bàn làm việc của nhân sự tự động giảm một nửa xuống còn `L = 0,25 × 10,29 = 2,57 hồ sơ` — nhân viên đỡ rối và đỡ quên việc hơn hẳn.

4. **Hiểu đúng "Mức sử dụng nguồn lực Quản lý" (`ρ_QL = 49,7%` xuống `8,7%`):**
   - Tại sao Quản lý bận `49,7%` (chưa phải 100%) mà hồ sơ đã chờ tới `22,56 giờ`?
   - Vì `ρ_QL` **chỉ đo thời gian Quản lý thực sự ngồi thao tác trực tiếp** (mở bảng dò lịch, gõ tin nhắn Zalo, kiểm tra lại khi đổi giờ). Trong 22,56 giờ của 1 hồ sơ, Quản lý tốn khoảng ~1,5–2 giờ thao tác cộng dồn qua các vòng (nhân với 60 hồ sơ/tháng ≈ `119 giờ / 240 giờ ≈ 49,7%` quỹ giờ cả tháng!), còn lại mười mấy tiếng là hồ sơ nằm đợi tin nhắn trả lời từ gia sư và phụ huynh!
   - Sang `TO-BE`, nhờ máy tính đã gom nhóm sẵn và gia sư đã điền lịch đầu tuần, Quản lý không phải dò tay từng ca nữa mà mỗi ngày chỉ mở bảng gợi ý 2 lần (11h30 & 17h30) để kiểm tra và bấm duyệt mất khoảng 15–20 phút → tổng thời gian bận thủ công tụt từ **`49,7%` xuống chỉ còn `8,7%`**, giải phóng hơn 80% quỹ thời gian để Quản lý tập trung giám sát chất lượng chuyên môn giảng dạy!

5. **Vì sao bắt buộc dùng mô phỏng sự kiện rời rạc `SimPy` thay vì công thức Erlang C?**
   - Trong Bài L4, các bạn được học công thức giải tích hàng đợi `M/M/s` (Erlang C). Nhưng công thức đó có giả định ngầm rất chặt: *khách đến một trạm, phục vụ xong là đi thẳng ra ngoài, không có chuyện quay vòng lại hay đứng đợi tin nhắn từ người thứ ba*.
   - Quy trình của CatPlus vi phạm giả định đó ở 3 điểm: (i) có vòng lặp **Rework** quay ngược từ Quản lý về CSKH rồi lại xuống Quản lý; (ii) có độ trễ **chờ Zalo ngoài hệ thống** không chiếm giữ nhân viên nhưng giữ chân hồ sơ; (iii) ở `TO-BE` có bước **gom đợt theo giờ cố định (batching lúc 11h30 & 17h30)**.
   - Trong `SimPy`, máy tính tạo ra một đồng hồ ảo chạy từ `t = 0` đến `t = 240 giờ` cho từng tháng: mỗi học sinh là một tiến trình độc lập, đến ngẫu nhiên theo phân phối mũ (quá trình Poisson), xin cấp phát tài nguyên nhân viên (`CSKH` có 2 người, `Quản lý` có 1 người — nếu nhân viên đang bận nghe máy ca trước thì ca sau tự xếp hàng chờ thật!), rồi ở mốc `11h30` và `17h30` đồng hồ kích hoạt hàm giải `MILP` trên toàn bộ giỏ hồ sơ đang chờ. Nhờ vậy, thời gian chờ `W` và `P90` thu được phản ánh trung thực toàn bộ sự tương tác động của hệ thống!

---

## CHƯƠNG 4. TỰ TAY XÂY DỰNG & TÍNH NHẨM MÔ HÌNH TỐI ƯU MILP (HIỂU THẤU MỤC 4 & MỤC 5)

Nhiều bạn nhìn thấy dấu tổng `∑` và các chỉ số `x_{i,k}`, `y_{k,c}`, `u_i` ở Mục 4.3 là dễ khớp tâm lý. Thực chất, **Quy hoạch nguyên hỗn hợp (MILP)** chỉ là cách viết các quy tắc đời thường của trung tâm thành các phép cộng/trừ lớp 9 để máy tính xét duyệt hàng triệu tổ hợp trong nửa giây! Hãy đi qua từng bước từ gốc:

### 4.1. Thang điểm phù hợp lịch và "Nghịch lý điểm trung bình" (`Fit_ghép` vs `Fit_chung`)
Khi CSKH hỏi phụ huynh tối đa 3 khung giờ con có thể học được theo thứ tự thích nhất đến ít thích hơn, nhóm quy đổi thành điểm số `w`:
- Xếp đúng **Khung giờ ưu tiên 1** (thích nhất): được **`100 điểm`**.
- Xếp vào **Khung giờ ưu tiên 2** (chấp nhận được): được **`80 điểm`**.
- Xếp vào **Khung giờ ưu tiên 3** (hơi trái giờ nhưng vẫn đi học được): được **`60 điểm`**.
- **Không xếp được lớp (bị rớt):** được **`0 điểm`**.

Bây giờ, hãy làm một **ví dụ tính nhẩm với 5 bạn học sinh THCS đăng ký học nhóm** để thấy tận mắt vì sao phải dùng song song 2 công thức ở (4.1):
- Giả sử có 5 bạn:
  - Bạn 1 & Bạn 2: Rảnh ưu tiên 1 ở **Tối Thứ Bảy**, ưu tiên 2 ở **Tối Thứ Tư**.
  - Bạn 3: Chỉ rảnh duy nhất ưu tiên 1 ở **Tối Thứ Bảy**.
  - Bạn 4 & Bạn 5: Rảnh ưu tiên 1 ở **Tối Thứ Ba**, ưu tiên 2 ở **Tối Thứ Bảy**.
- **Cách 1 — Xếp tay `AS-IS` (chỉ biết ưu tiên 1 của mỗi bạn):**
  - Tối Thứ Bảy có 3 bạn (Bạn 1, 2, 3) → Đủ 3 người, mở được 1 lớp! Cả 3 bạn đều trúng ưu tiên 1 (`100 điểm`).
  - Tối Thứ Ba chỉ có 2 bạn (Bạn 4, 5) → Chưa đủ 3 người, **không mở được lớp** → Bạn 4 và Bạn 5 bị rớt (`0 điểm`).
  - Hãy tính 2 chỉ số của `AS-IS`:
    - `Fit_ghép` *(chỉ tính trung bình những người đỗ)* = `(100 + 100 + 100) ÷ 3 = 100,0 điểm`! (Trông tưởng hoàn hảo tuyệt đối!).
    - `Fit_chung` *(tính trung bình cả 5 người đăng ký)* = `(100 + 100 + 100 + 0 + 0) ÷ 5 = 60,0 điểm`! (Thấp vì bỏ rơi mất 2 bạn!).
- **Cách 2 — Tối ưu `TO-BE` (biết thêm ưu tiên 2 của Bạn 4, 5 là Tối Thứ Bảy):**
  - Thuật toán phát hiện Bạn 4 và Bạn 5 đều học được Tối Thứ Bảy (dù chỉ là ưu tiên 2 = `80 điểm`), nên gộp luôn cả 5 bạn (Bạn 1, 2, 3, 4, 5) vào **1 lớp nhóm 5 người vào Tối Thứ Bảy** (vừa khít trần tối đa 5 học sinh/nhóm)!
  - Hãy tính lại 2 chỉ số của `TO-BE`:
    - `Fit_ghép` *(trung bình những người đỗ)* = `(100 + 100 + 100 + 80 + 80) ÷ 5 = 92,0 điểm` (giảm nhẹ từ `100` xuống `92` vì có 2 bạn học ở ưu tiên 2!).
    - `Fit_chung` *(trung bình cả 5 người đăng ký)* = **`92,0 điểm`** (tăng vọt từ `60,0` lên `92,0`, và tỷ lệ đỗ đạt `100%`!).

> **Chìa khóa nhận thức số 2:** Ví dụ 5 học sinh trên chính là bản thu nhỏ chính xác 100% của Bảng 6.1 trong báo cáo! Trong báo cáo, `Fit_ghép` giảm nhẹ `3,5 điểm` (từ `96,8` xuống `93,3`), nhưng tỷ lệ đỗ tăng từ `60,4%` lên `92,7%` và `Fit_chung` tăng vọt từ **`58,5` lên `86,5 điểm`**. Ở `AS-IS`, điểm `Fit_ghép` cao là do **"thiên lệch sống sót" (survivorship bias)** — tức là vứt bỏ hết các ca khó ra ngoài rồi chỉ chấm điểm những ca dễ! Khi bạn hiểu ví dụ này, không câu hỏi phản biện nào về độ phù hợp lịch có thể làm khó được bạn.

### 4.2. Giải thích ý nghĩa từng ký hiệu và từng phương trình MILP `(4.2) – (4.5)`

Trong bài toán thực tế của tháng, có `N = 60` học sinh (đánh số `i = 1..60`) và `M = 10` gia sư. Mỗi gia sư rảnh 5–7 buổi/tuần, tạo thành tập khoảng ~60 cặp `(gia sư t, khung giờ s)` có thể mở lớp — ta đánh số thứ tự từng cặp ca trống đó là `k`. Có `4` kiểu lớp học `c`: *(1) THCS 1–1; (2) THPT 1–1; (3) THCS Nhóm; (4) THPT Nhóm*.

Máy tính cần ra quyết định bằng cách bật/tắt **3 loại công tắc nhị phân** (chỉ nhận giá trị `0` = Tắt, hoặc `1` = Bật):
- **Công tắc 1 — `x_{i,k} ∈ {0, 1}`:** Có xếp học sinh `i` vào học ở ca trống `k` hay không? *(Chỉ tạo biến này nếu ca `k` đúng khung giờ học sinh `i` rảnh và gia sư của ca `k` dạy được cấp học của em `i`)*.
- **Công tắc 2 — `y_{k,c} ∈ {0, 1}`:** Tại ca trống `k` đó, có quyết định khai giảng một lớp thuộc kiểu `c` hay không?
- **Công tắc 3 — `u_i ∈ {0, 1}` (Biến "lớp ảo" — Bài L5 Trang 8):** Học sinh `i` có bị rơi vào giỏ "chưa xếp được lớp thật" hay không?

Bây giờ hãy đọc 4 công thức `(4.2) – (4.5)` trong báo cáo bằng tiếng Việt mạch lạc:

#### 1. Công thức (4.3): `∑ x_{i,k} + u_i = 1` *(Mọi học sinh đều phải có chỗ đứng rõ ràng)*
- Với mỗi học sinh `i`, tổng tất cả các công tắc lớp thật `x_{i,k}` cộng với công tắc lớp ảo `u_i` bắt buộc bằng đúng `1`.
- Vì các biến chỉ nhận giá trị nguyên `0` hoặc `1`, phương trình này ép buộc: Học sinh `i` **hoặc** được vào đúng 1 lớp thật duy nhất (`một biến x = 1, còn u_i = 0`), **hoặc** nếu kẹt lịch không vào được lớp thật nào thì bắt buộc bật công tắc lớp ảo (`tất cả x = 0, và u_i = 1`).
- *Tại sao phải có `u_i` mà không viết luôn `∑ x_{i,k} = 1`?* Giả sử trong 60 em có 1 em chỉ rảnh sáng Thứ Bảy mà tất cả gia sư sáng Thứ Bảy đều đã kín lớp. Nếu viết cứng `∑ x_{i,k} = 1`, phương trình của em đó trở thành `0 = 1` (vô lý!) → bộ giải toán học báo lỗi **Infeasible (Vô nghiệm)** và dừng chạy luôn, không xếp lịch cho cả 59 em còn lại! Có thêm `u_i` giống như van an toàn cho ràng buộc mềm: ai không ghép được thì đẩy sang `u_i = 1`, còn 59 bạn kia vẫn được tối ưu bình thường.

#### 2. Công thức (4.4): `∑_c y_{k,c} ≤ 1` và `∑ y_{k,c} ≤ K_t` *(Giới hạn vật lý của gia sư)*
- Bất đẳng thức đầu nói rằng: Tại một khung giờ `k` của một gia sư, gia sư đó không thể phân thân vừa dạy lớp THCS vừa dạy lớp THPT cùng lúc → tổng số kiểu lớp mở tại 1 ca `k` tối đa là `1` (`= 0` nếu ca đó gia sư nghỉ, `= 1` nếu có mở lớp).
- Bất đẳng thức thứ hai nói rằng: Cộng tất cả các lớp mà gia sư `t` nhận dạy trong cả tuần không được vượt quá sức dạy tối đa `K_t` (từ 3 đến 5 lớp tùy gia sư) mà người đó đã đăng ký với trung tâm.

#### 3. Công thức (4.5): `L_c · y_{k,c} ≤ ∑ x_{i,k} ≤ U_c · y_{k,c}` *(Trái tim của mô hình — Khóa chặt sĩ số hai đầu)*
Đây là kỹ thuật **liên kết biến quyết định (linking constraints)** kinh điển trong giáo trình Daskin (Mục 2.9). Hãy thử thay số đối với cấu hình **Lớp nhóm** có cận dưới `L_c = 3` và cận trên `U_c = 5` (`3 · y ≤ ∑ x ≤ 5 · y`):
- **Trường hợp 1 — Không mở lớp nhóm tại ca đó (`y = 0`):** Bất đẳng thức trở thành `3 × 0 ≤ ∑ x ≤ 5 × 0`, tức là `0 ≤ ∑ x ≤ 0` → ép buộc `∑ x = 0`! Không một học sinh nào được phép gán vào một lớp chưa mở.
- **Trường hợp 2 — Có mở lớp nhóm tại ca đó (`y = 1`):** Bất đẳng thức lập tức biến thành `3 ≤ ∑ x ≤ 5`! Tổng số học sinh tương thích được gán vào ca đó **bắt buộc phải nằm từ 3, 4 hoặc 5 em**. Nếu chỉ có 1 hoặc 2 em, vế trái `3 ≤ 2` bị sai → máy tính tự động gạt bỏ phương án mở lớp non đó và đi tìm khung giờ chung khác để gom cho đủ từ 3 em trở lên!
- *(Với lớp kèm 1–1, chỉ cần thay `L_c = 1, U_c = 1` → `1 · y ≤ ∑ x ≤ 1 · y`, tức là `∑ x = y`: mở lớp là có đúng 1 học sinh).*
- **Vì sao không thể giải số thực liên tục rồi làm tròn?** Giả sử có 2 học sinh cùng muốn học nhóm ở tối Thứ Hai. Nếu cho phép `y` nhận số thập phân liên tục từ `0` đến `1`, máy tính sẽ lách luật bằng cách đặt `y = 0,667`! Khi đó `3 × 0,667 = 2 ≤ 2 ≤ 5 × 0,667 = 3,33` — hoàn toàn thỏa mãn bất đẳng thức toán học nhưng ngoài đời không hề tồn tại *"0,667 lớp học"*! Làm tròn lên `1` thì lớp thiếu người, làm tròn xuống `0` thì 2 em mất lớp. Đó là lý do bắt buộc phải giải bằng **Quy hoạch nguyên nhị phân (`integrality = 1`)**.

#### 4. Công thức (4.2): Hàm mục tiêu `min Z = ∑ P · u_i − ∑ w_{i,k} · x_{i,k} + γ ∑ y_{k,c}` *(Cách thiết kế trọng số thông minh)*
Vì bài toán là **cực tiểu hóa (`min Z`)**, cái gì xấu (muốn giảm) ta mang dấu `+`, cái gì tốt (muốn tăng) ta mang dấu `−`:
- `+ P · u_i` (với `P = 1.000`): Cứ mỗi học sinh bị rớt vào lớp ảo (`u_i = 1`), tổng `Z` bị phạt cộng thêm `1.000`.
- `− w_{i,k} · x_{i,k}` (với `w ∈ {100, 80, 60}`): Cứ ghép được 1 học sinh vào lớp thật, tổng `Z` được giảm đi `100`, `80` hoặc `60` điểm tùy mức độ đúng ý nguyện vọng.
- `+ γ · y_{k,c}` (mặc định `γ = 0,05`): Mở thêm 1 lớp mới tốn một khoản phí nhỏ `γ`.

**Tại sao nhóm lại chọn bộ số `P = 1.000`, `w = 100/80/60` và `γ = 0,05`?** Không phải chọn bừa đâu! Hãy nhìn tỷ lệ độ lớn giữa chúng:
- `P = 1.000` lớn gấp **10 lần** điểm hợp lịch tối đa (`100`). Giả sử để cứu thêm 1 bạn khỏi bị rớt lớp (giảm phạt được `1.000 điểm`), máy tính phải dời 4 bạn khác từ khung giờ ưu tiên 1 (`100đ`) sang ưu tiên 3 (`60đ`, mỗi bạn thiệt `40đ`, 4 bạn thiệt `160đ`). Nhờ `1.000 > 160`, máy tính vẫn quyết tâm cứu bạn kia vào lớp! Nghĩa là **Ưu tiên tầng 1 luôn là cứu tối đa số lượng học sinh được đi học**.
- Giữa các phương án cứu được **cùng số lượng học sinh như nhau**, tổng phạt `P · u_i` bằng nhau, lúc này thành phần thứ hai `− w_{i,k} · x_{i,k}` (`60` đến `100` điểm) lên tiếng → máy chọn phương án có **tổng độ hài lòng lịch học cao nhất (Ưu tiên tầng 2)**.
- Cuối cùng, nếu có hai cách xếp vừa bằng nhau về số học sinh đỗ, vừa bằng nhau về điểm hợp lịch (ví dụ: mở 2 lớp nhóm 3 người so với gộp thành 1 lớp nhóm 3 người + dồn sang nhóm 4 người có sẵn), thì khoản phí nhỏ `γ = 0,05` sẽ chọn phương án **tốn ít ca gia sư mở mới hơn (Ưu tiên tầng 3)** mà không bao giờ làm sai lệch hai mục tiêu chính ở trên!

---

## CHƯƠNG 5. ĐỌC HIỂU CÁC BẢNG KẾT QUẢ, ĐƯỜNG BIÊN PARETO & ĐỘ NHẠY (MỤC 6 BÁO CÁO)

Khi đọc Mục 6 của báo cáo, có **3 hiện tượng sâu sắc** mà một người hiểu bài thực sự sẽ nhìn ra ngay (và giảng viên cực kỳ thích hỏi để xem sinh viên có hiểu kết quả mình chạy ra hay không):

### 5.1. Giải mã Bảng 6.2 — Tại sao Đường biên Pareto lại nhảy bậc ở `γ = 1.065`, `1.085`, `1.105`?
Ở Mục 6.2, nhóm đặt câu hỏi quản trị: *Nếu trung tâm muốn tiết kiệm chi phí thuê gia sư (mở ít ca lớp hơn) thì phải chấp nhận giảm tỷ lệ ghép lớp bao nhiêu?* Để tìm đường biên đánh đổi tối ưu (**Pareto frontier**), nhóm tăng dần trọng số chi phí mở lớp `γ` trong hàm mục tiêu `(4.2)` khi giữ nguyên `P = 1.000`.

Hãy làm phép tính lợi ích ròng của việc mở **1 lớp kèm 1–1** (chỉ phục vụ đúng 1 học sinh):
- Nếu mở 1 lớp 1–1 cho học sinh ở **ưu tiên 3 (`w = 60`)**: Trung tâm cứu được 1 em khỏi lớp ảo (lợi `1.000`) + được điểm hợp lịch (`60`) = **Tổng lợi ích `1.060`**, trong khi tốn chi phí mở 1 lớp là **`γ`**.
- Nếu mở 1 lớp 1–1 cho học sinh ở **ưu tiên 2 (`w = 80`)**: Tổng lợi ích là **`1.000 + 80 = 1.080`**.
- Nếu mở 1 lớp 1–1 cho học sinh ở **ưu tiên 1 (`w = 100`)**: Tổng lợi ích là **`1.000 + 100 = 1.100`**.
- Còn nếu mở **1 lớp Nhóm (tối thiểu 3 học sinh)**: Cứu được ít nhất 3 em khỏi lớp ảo → Tổng lợi ích ít nhất là **`3 × 1.000 + 3 × 60 = 3.180`** (luôn lớn hơn rất nhiều so với `1.105`)!

Từ 4 phép cộng trên, nhìn vào Bảng 6.2 mọi thứ sáng tỏ như ban ngày:
1. Khi **`γ = 10`** (`< 1.060`): Mọi lớp 1–1 và lớp nhóm hợp lệ đều có lời → Mở tối đa `33,25 ca/tháng`, tỷ lệ ghép đạt cao nhất (`91,3%`).
2. Khi kéo **`γ = 1.065`** (vừa vượt ngưỡng `1.060`): Mở lớp 1–1 ở ưu tiên 3 bị lỗ (`chi phí 1.065 > lợi ích 1.060`) → Mô hình lập tức **cắt bỏ các lớp 1–1 rơi vào ưu tiên 3**, giảm xuống `32,17 ca/tháng`.
3. Khi kéo **`γ = 1.085`** (vừa vượt ngưỡng `1.080`): Mô hình cắt tiếp các lớp 1–1 ở ưu tiên 2, chỉ giữ lại lớp 1–1 nếu trúng ngay ưu tiên 1 (`1.100 > 1.085`) và dồn tối đa sang lớp nhóm → Số ca mở giảm còn `29,67 ca/tháng` (tiết kiệm ~3,6 ca gia sư/tháng mà tỷ lệ ghép vẫn giữ được `85,3%`).
4. Khi kéo **`γ = 1.105`** (vượt ngưỡng `1.100`): Toàn bộ lớp 1–1 đều có lợi ích `≤ 1.100 < 1.105` nên **bị dừng mở hoàn toàn 100%**! Hệ thống chỉ còn mở đúng `8,92` lớp nhóm đông người mỗi tháng, làm tỷ lệ ghép sụt mạnh xuống `50,7%` (vì 40% học sinh đăng ký 1–1 bị từ chối hết).

Đây chính là minh họa thực tiễn cho lý thuyết ở **Bài giảng L5 (Trang 26)**: Trong quy hoạch nguyên, khi thay đổi tham số liên tục, nghiệm không đổi trơn tru từ từ mà thay đổi theo từng **"bước nhảy" (step jumps)** mỗi khi vượt qua ngưỡng lợi ích tới hạn!

Đồng thời, trên Hình 6.2b (*Kiểm định nghiệm trội Pareto*): một phương án A gọi là **bị trội (dominated)** bởi phương án B nếu A thua kém B ở **tất cả** các mục tiêu đang xét. So trên 2 mục tiêu chất lượng (`Tỷ lệ ghép lớp` và `Fit_chung`), phương án `AS-IS` (`60,4%`; `58,5 điểm`) thua toàn diện trước `TO-BE hỏi 3 ca` (`92,7%`; `86,5 điểm`) → chứng minh cải tiến không chỉ đổi cái này lấy cái kia, mà đẩy toàn bộ hệ thống lên một đường biên hiệu quả cao hơn hẳn!

### 5.2. Giải mã 3 quy luật vận hành thú vị trong Bảng Độ nhạy 6.3
Ở Bảng 6.3, nhóm thử thay đổi từng yếu tố đầu vào (`N` số học sinh, `M` số gia sư, `m` số khung giờ hỏi tối đa) để xem mô hình phản ứng ra sao:

1. **Quy luật 1 — Hiệu ứng mật độ gom nhóm theo quy mô khách `N`:**
   - Nhìn dòng `N = 45` (`87,0%`) so với `N = 60` (`92,5%`) và `N = 90` (`87,5%`), đường biểu diễn của `TO-BE` có dạng **hình vòm (đạt đỉnh ở quanh N = 60)** chứ không giảm đều từ trái sang phải!
   - *Tại sao ít khách hơn (`N = 45`) mà tỷ lệ ghép lại thấp hơn `N = 60`?* Vì với lớp nhóm bắt buộc đủ 3 người, khi tổng lượng khách đăng ký trong tháng quá thưa (`45` em), mật độ học sinh có lịch rảnh giao nhau bị loãng đi → có những em chọn học nhóm không tìm nổi 2 người bạn cùng cấp để ghép chung! Khi lên `N = 60`, mật độ vừa đẹp để các nhóm lấp đầy 3–5 người (`92,5%`). Đến khi tăng vọt lên `N = 90` học sinh mà vẫn giữ nguyên `10` gia sư, lúc này mới thực sự chạm **trần công suất dạy tối đa của gia sư**, làm tỷ lệ ghép hạ xuống `87,5%` (nhưng chú ý ở cột cuối: tại `N = 90`, Quản lý ở `AS-IS` bị quá tải lên tới `72,6%` thời gian làm việc, trong khi `TO-BE` vẫn ung dung ở mức `12,8%`!).

2. **Quy luật 2 — Thuật toán điều phối tốt còn quý hơn tuyển gấp đôi gia sư:**
   - Khi cắt giảm nhân sự xuống chỉ còn **`M = 6` gia sư** (thiếu hụt nặng), mô hình `TO-BE` vẫn khéo léo gom cụm để ghép thành công **`75,3%`** học viên — con số này **cao hơn cả khi trung tâm có tới `M = 12` gia sư nhưng xếp bằng tay theo `AS-IS` (`62,2%`)**! Điều này khẳng định kết luận của Bài L6–L7: trước khi tốn tiền mở rộng công suất phần cứng/nhân sự, phải tối ưu cơ chế phân bổ nguồn lực trước.

3. **Lưu ý nhỏ về sự khác nhau vài phần mười giữa Bảng 6.1 và Bảng 6.3 (để không bao giờ bỡ ngỡ):**
   - Nếu nhìn thật kỹ, ở Bảng 6.1 cấu hình cơ sở (`N = 60, M = 10, m = 3`) có `AS-IS = 60,4%` và `TO-BE = 92,7%`; còn ở Bảng 6.3 dòng quét độ nhạy `N = 60` có `AS-IS = 64,6%` và `TO-BE = 92,5%`.
   - *Tại sao có chênh lệch nhỏ này?* Vì **Bảng 6.1** là kết quả chạy **mô phỏng gắn kết toàn trình 20 chu kỳ tháng** (có đầy đủ dòng khách đến ngẫu nhiên theo giờ, tách từng đợt chạy 11h30/17h30 và tính cả `8%` xác suất gia sư báo bận đột xuất ngoài đời thực); còn **Bảng 6.3 và 6.2** chạy trên bộ vòng lặp quét tham số cố định từng tháng để cô lập riêng ảnh hưởng thuần túy của từng tham số `N`, `M`, `m`, `γ` mà không bị nhiễu bởi biến cố ngẫu nhiên. Cả hai cách đo đều cho kết quả nhất quán tuyệt đối (TO-BE luôn vượt AS-IS quanh mức `+28` đến `+32` điểm %).

---

## CHƯƠNG 6. HIỂU THIẾT KẾ VẬN HÀNH TO-BE, QUẢN TRỊ CHIẾN LƯỢC & MÃ NGUỒN (MỤC 7, 8 & CODE)

### 6.1. Tại sao `TO-BE` lại thiết kế đúng 4 cơ chế đó mà không làm khác đi?
Mục 7.1 áp dụng 4 nguyên tắc tái thiết kế quy trình của Bài giảng L3B (*Simplify, Reposition, Automate, Design recovery*). Hãy hiểu lý do thực tế của từng lựa chọn:

1. **Tại sao chạy gom đợt 2 lần/ngày (11h30 và 17h30) mà không chạy tức thời mỗi khi có 1 khách nộp đơn, hoặc gom 1 tuần chạy 1 lần?**
   - Nếu *vừa có 1 khách nộp đơn lúc 9h05 đã chạy MILP chốt lớp luôn*, trong giỏ lúc đó chỉ có đúng 1 học sinh → chẳng khác gì xếp tuần tự từng người của `AS-IS`, không thể gom nhóm được!
   - Ngược lại, nếu *gom suốt 1 tuần mới chạy 1 lần*, giỏ hồ sơ có 15 học sinh thì gom nhóm cực dễ, nhưng người nộp đơn từ sáng Thứ Hai phải đợi đến cuối tuần mới biết lịch học → thời gian chờ vọt lên 40 giờ làm việc, phụ huynh sang trung tâm khác đăng ký mất!
   - Gom **nửa ngày một lần (11h30 trưa và 17h30 chiều)** kết hợp quy tắc ở **Bảng 7.1** (*nếu nhóm mới gom được 2 bạn trùng giờ thì cho phép giữ chờ tối đa thêm 1 đợt kế tiếp — tức thêm nửa ngày — để đón bạn thứ 3; quá hạn đó chưa đủ 3 em thì CSKH chủ động tư vấn lộ trình 1–1*) là điểm cân bằng vừa đủ độ tụ để gom nhóm, vừa giữ tổng thời gian chờ trung bình chỉ `10,29 giờ` (~1,3 ngày)!

2. **Tại sao phải thiết kế sẵn "Phương án gia sư dự phòng số 2" (*Design recovery* — Bảng 7.1)?**
   - Trong thực tế, dù gia sư đã khai báo lịch trống đầu tuần, vẫn có khoảng `8%` trường hợp gia sư bận đột xuất (ốm, bận thi ở trường đại học...). Ở `AS-IS`, gặp tình huống này là Quản lý lại phải gọi xin phụ huynh đổi giờ. Ở `TO-BE`, khi xuất gợi ý, hệ thống lọc sẵn luôn gia sư phù hợp số 2 ở cùng tập khung giờ 1–3 mà phụ huynh đã cho → Quản lý bấm chuyển sang phương án 2 ngay trên màn hình mà **không cần làm phiền lại khách hàng**.

3. **Mạch nhân – quả của Thẻ điểm cân bằng 4 góc nhìn (Balanced Scorecard — Bảng 7.2, Bài L6–L7):**
   - Balanced Scorecard giúp trung tâm không bị "lệch pha" (ví dụ: ép nhân viên chốt lịch thật nhanh nhưng lại nhét bừa làm học sinh bỏ học). Bốn góc nhìn nối với nhau thành chuỗi nhân quả từ dưới lên trên:
     - **Góc nhìn 4 — Học hỏi & Phát triển (Gốc rễ dài hạn):** Thống kê xem những hồ sơ bị rơi vào lớp ảo (`u_i = 1`) thường dồn vào khung giờ nào và cấp học nào → giúp Ban giám đốc biết chính xác quý tới cần **tuyển thêm gia sư ở khung giờ nào** thay vì tuyển cảm tính!
     - **Góc nhìn 3 — Quy trình nội bộ:** Giữ tỷ lệ phải gọi lại đổi lịch (Rework) và độ bận của Quản lý ở mức thấp (`~8,7%`).
     - **Góc nhìn 2 — Khách hàng:** Nhờ quy trình nội bộ trơn tru, khách hàng nhận được tỷ lệ xếp lớp cao (`92,7%`) và phản hồi nhanh trong 2 ngày (`99,3%`).
     - **Góc nhìn 1 — Tài chính:** Nhờ gom nhóm hiệu quả, sĩ số trung bình mỗi lớp nhóm mở mới đạt `≥ 3,8 học viên/lớp` (vượt xa ngưỡng hòa vốn 3 em/lớp), tối ưu biên lợi nhuận cho trung tâm.

### 6.2. Hiểu cấu trúc các tệp mã nguồn trong thư mục `du_an_nhom20/`
Nếu bạn mở thư mục dự án ra hoặc giảng viên hỏi về phần thực thi kỹ thuật (Mục 5), bạn chỉ cần nắm rõ vai trò của 3 tệp cốt lõi:
- **`CatPlus_Sim_Opt_Model.py`:** Trái tim tính toán của dự án. Bên trong có 4 phần rõ ràng:
  1. Hàm sinh dữ liệu tái lập (`seed = 42`) tạo ra học sinh (cấp học, chế độ `1–1` / `GROUP`, 1–3 khung giờ rảnh theo trọng số thực tế tối/cuối tuần) và 10 gia sư.
  2. Hàm `solve_as_is_fcfs(...)`: Mô phỏng đúng cách con người đang dò lịch tuần tự từng người và cố gắng ghép vớt thủ công.
  3. Hàm `solve_to_be_milp(...)`: Dựng ma trận ràng buộc thưa (`scipy.sparse.coo_matrix`) cho các phương trình `(4.2)–(4.5)` và gọi bộ giải nhánh cận `scipy.optimize.milp` (trích đoạn ở Mục 5.2 báo cáo chính là vòng lặp dựng 2 bất đẳng thức cận trên `≤ 5·y` và cận dưới `≥ 3·y`!).
  4. Lớp môi trường `SimPy` chạy 20 chu kỳ tháng độc lập, xuất toàn bộ thống kê trung bình, độ lệch chuẩn, phân vị `P90` ra tệp `simulation_results.json` và vẽ các biểu đồ kết quả.
- **`catplus_matching_as_is.bpmn` & `catplus_matching_to_be.bpmn`:** Hai tệp định dạng chuẩn XML quốc tế BPMN 2.0 (có thể kéo thả trực tiếp vào công cụ chuẩn `https://demo.bpmn.io/new` để xem và chỉnh sửa từng cổng, luồng, sự kiện).
- **`export_real_data_template.py`:** Kịch bản đọc dữ liệu chỉ-đọc (read-only) kết nối với cơ sở dữ liệu Django/PostgreSQL thật của dự án CatPlus, tự động băm ẩn danh mã học sinh (bảo mật thông tin cá nhân phụ huynh/học sinh) để xuất ra 4 tệp CSV nạp thẳng vào mô hình ngay khi trung tâm hoàn tất nhập liệu lịch sử.

---

## CHƯƠNG 7. SỢI CHỈ ĐỎ TƯ DUY KHI TRÌNH BÀY 12 SLIDE & ĐỐI THOẠI PHẢN BIỆN

Khi bạn đã hiểu trọn vẹn Chương 1 đến Chương 6 ở trên, bạn **không cần học thuộc lòng bất kỳ câu văn mẫu nào** nữa. Khi đứng trước bộ 12 slide thuyết trình, hãy nhìn chúng như **một câu chuyện trinh thám – kỹ thuật liền mạch gồm 4 chặng tư duy**:

### 7.1. Mạch nối nhân – quả xuyên suốt 12 Slide (Hiểu mạch để tự dẫn dắt tự nhiên)

1. **Chặng 1 — Nhận diện bài toán & Mổ xẻ hệ thống (Slide 1 → Slide 4 | ~3 phút đầu):**
   - *Ý niệm cốt lõi cần truyền tải:* CatPlus không thiếu khách đăng ký và cũng chưa thiếu tổng giờ gia sư, nhưng đang bị nghẽn ở khâu chuyển hóa từ *đăng ký* sang *lớp học thực tế* vì quy định lớp nhóm **3–5 học viên cùng cấp** đang được xử lý thủ công rời rạc.
   - *Mạch chuyển ý tự nhiên:* Giới thiệu bối cảnh & 3 câu hỏi KPI (Slide 1–2) → Dùng khung *Work System* chỉ ra đây là lỗi cấu trúc phối hợp giữa Thông tin – Hoạt động – Công nghệ – Thiết chế chứ không phải lỗi cá nhân (Slide 3) → Chỉ vào *Bản đồ nguồn lực* để nhấn mạnh vai trò **đầu vào khung giờ rảnh từ khách hàng** trong việc đồng tạo ra lớp học (Slide 4).

2. **Chặng 2 — Bằng chứng chẩn đoán hiện trạng `AS-IS` (Slide 5 → Slide 6 | ~2 phút tiếp):**
   - *Ý niệm cốt lõi cần truyền tải:* Vẽ quy trình ra (BPMN) để thấy **chỗ nào lặp**, và đo bằng số (Hàng đợi) để chứng minh **chỗ nào ngốn thời gian nhất**.
   - *Mạch chuyển ý tự nhiên:* Trên BPMN `AS-IS` (Slide 5), chỉ ra vòng xoáy *hỏi 1 khung giờ → nhắn chờ Zalo gia sư → thiếu nhóm 3 người → gọi lại xin đổi lịch*. Sang Slide 6, dùng ngay con số đo đạc để khẳng định: CSKH gọi lần đầu chỉ tốn `8,6%` thời gian (`1,95h`), còn chính vòng lặp dò lịch & chờ Zalo mới ngốn `69,4%` (`15,66h`), làm rớt `39,6%` học viên (chủ yếu do nhóm lẻ 1–2 em) và chiếm nửa ngày làm việc của Quản lý.

3. **Chặng 3 — Cơ chế tháo gỡ bằng `MILP + SimPy` & Quy trình `TO-BE` (Slide 7 → Slide 8 | ~2 phút tiếp):**
   - *Ý niệm cốt lõi cần truyền tải:* Muốn gom được các học sinh rời rạc thành nhóm đủ 3–5 người mà vẫn giữ sự tư vấn ấm áp của con người, ta phải làm **đồng thời 2 việc**: mở rộng đầu vào thông tin (hỏi 1–3 khung giờ + lịch trống gia sư đầu tuần) và để máy tính giải bài toán tổ hợp `MILP` theo đợt.
   - *Mạch chuyển ý tự nhiên:* Giải thích trực giác 3 cột ở Slide 7 (Đầu vào điểm `100/80/60` → MILP khóa sĩ số `3 ≤ ∑x ≤ 5` kèm biến lớp ảo `u_i` → SimPy đo thời gian chờ động) → Đặt mô hình đó vào quy trình `TO-BE` chạy 2 đợt/ngày lúc `11h30 & 17h30` kèm 4 quy tắc xử lý thực tế cho Quản lý học vụ duyệt trong 1 vòng (Slide 8).

4. **Chặng 4 — Chứng minh hiệu quả, Đánh đổi quản trị & Triển khai (Slide 9 → Slide 12 | ~3 phút cuối):**
   - *Ý niệm cốt lõi cần truyền tải:* Một nghiên cứu Khoa học dịch vụ tốt không chỉ khoe con số tăng đẹp, mà phải chỉ ra **điều kiện nào để nó chạy được**, **đánh đổi cái gì**, và **khi chiến lược thay đổi thì điều chỉnh ra sao**.
   - *Mạch chuyển ý tự nhiên:* Đối chứng mức nhảy vọt từ `60,4% → 92,7%` và giảm chờ `22,56h → 10,29h` (Slide 9) → Chỉ ra bằng chứng then chốt ở Slide 10: *nếu chỉ hỏi 1 khung giờ thì MILP cũng chỉ đạt `58,3%`* (chứng minh vai trò sống còn của thông tin khách hàng!), đồng thời giải thích cách vặn núm điều chỉnh `γ` trên đường biên Pareto khi thiếu gia sư và 3 đánh đổi thực tế → Chốt lại bằng lộ trình triển khai 2 bước, sự minh bạch thẳng thắn về bộ dữ liệu mô phỏng tái lập `seed = 42` và tổng kết trả lời gọn 3 câu hỏi đầu bài (Slide 11–12).

### 7.2. Ba nguyên tắc tư duy gốc để tự tin ứng biến mọi câu hỏi trên bàn bảo vệ
Dù giảng viên có đặt câu hỏi theo góc độ nào, câu trả lời bản chất luôn xoay quanh 3 nguyên lý mà bạn đã nắm vững:

1. **Khi giảng viên hỏi về "Sự đánh đổi" (Trade-off):** Trong Khoa học dịch vụ không có giải pháp nào miễn phí 100%. Phương án `TO-BE` chấp nhận **3 chi phí nhỏ có kiểm soát** *(cuộc gọi đầu lâu hơn 3–5 phút để hỏi kỹ 2–3 khung giờ; đợi gom đợt nửa ngày tới 11h30/17h30; giảm nhẹ 3,5 điểm ưu tiên cá nhân trên nhóm đỗ)* để đổi lấy **3 lợi ích hệ thống vượt trội** *(cứu thêm +32,3% học viên không bị rớt lớp; cắt bỏ vòng lặp chờ Zalo giúp tổng thời gian chờ giảm 54,4%; giải phóng từ 49,7% xuống 8,7% tải thủ công cho Quản lý)*.
2. **Khi giảng viên hỏi về "Giả định & Độ tin cậy của mô hình":** Luôn đứng trên lập trường khoa học trung thực: cấu trúc lớp học (`1–1`, `Nhóm 3–5`) và luồng nhân sự là kiến trúc thật của CatPlus; dữ liệu số hiện tại là mô phỏng tái lập (`seed = 42`) có kiểm chứng chéo qua Định luật Little và thử thách qua 11 kịch bản biến động nguồn lực (nhiều/ít khách, thiếu gia sư, thay đổi số khung giờ hỏi) để đảm bảo kết luận vững chắc về mặt cơ chế trước khi nạp CSV thực tế.
3. **Khi giảng viên hỏi "Vì sao công nghệ phải đi đôi với quy trình & con người?":** Luôn dẫn chứng ngay dòng thứ 2 của Bảng 6.1 (*TO-BE chỉ hỏi 1 khung giờ = 58,3%*): thuật toán tối ưu mạnh đến mấy cũng vô dụng nếu quy trình giao tiếp của CSKH không khai thác được độ linh hoạt lịch từ phía phụ huynh, và ngược lại, con người tư vấn tốt đến mấy cũng bị quá tải nếu thiếu công cụ gom cụm tổ hợp của máy tính. Đó chính là tinh thần cốt lõi nhất của môn **Khoa học dịch vụ**!
