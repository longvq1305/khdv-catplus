# CHECKPOINT 1 - PHÂN TÍCH HỆ THỐNG DỊCH VỤ CATPLUS

## Đề tài: Hệ thống dịch vụ đào tạo lập trình có hỗ trợ chấm bài tự động

- **Học phần:** Khoa học dịch vụ
- **Đối tượng phân tích:** CatPlus Platform
- **Người thụ hưởng chính:** Học viên

---

## 1. Đăng ký và mô tả ngắn gọn đề tài

### 1.1. Tên đề tài tạm thời

**Phân tích hệ thống dịch vụ đào tạo lập trình CatPlus theo Logic hướng dịch vụ và các mô hình hệ thống dịch vụ.**

### 1.2. Mô tả

CatPlus kết nối hoạt động quản lý lớp học với hoạt động luyện lập trình. Gia sư giao Problem Set; học viên đọc đề, chạy thử và nộp bài; hệ thống OJ chấm mã nguồn và trả kết quả; gia sư theo dõi tiến độ, xem bài nộp và hỗ trợ học viên khi cần. Không gian làm bài còn có chức năng Gợi ý với AI khi được bật, nhưng học viên phải chủ động yêu cầu và gợi ý này không thay thế gia sư.

Trong phạm vi môn học, nhóm xem CatPlus là một hệ thống dịch vụ chứ không chỉ là một phần mềm chấm code. Đề bài, trình soạn thảo và máy chấm là các phương tiện hỗ trợ; giá trị chỉ hình thành khi học viên, gia sư và nền tảng cùng tham gia vào quá trình học tập.

---

## 2. Ranh giới hệ thống, tác nhân và bên thụ hưởng

### 2.1. Ranh giới hệ thống

**Trong biên phân tích**

- Learning Web và không gian làm bài của học viên.
- Academic Service: lớp, buổi học, assignment, tiến độ và ngữ cảnh gia sư.
- OJ Service, Judge Bridge và DMOJ: run, submit, chấm và trả verdict.
- Hoạt động của học viên, gia sư và quản lý học vụ liên quan trực tiếp tới giao bài, làm bài, theo dõi và hỗ trợ.

**Ngoài biên nhưng có ảnh hưởng**

- Codeforces Polygon - nguồn package đề bài.
- Hạ tầng mạng và máy chủ.
- Quy định lớp học, chuẩn liêm chính học thuật và chính sách hiển thị testcase.
- Phụ huynh, kỳ thi và thị trường tuyển dụng. Đây là các bên liên quan và yếu tố bối cảnh, không trực tiếp tham gia quy trình làm bài đang được phân tích.

### 2.2. Các tác nhân chính

| Tác nhân | Vai trò dịch vụ | Tài nguyên đóng góp | Lợi ích/kết quả kỳ vọng |
|---|---|---|---|
| **Học viên** | Người thụ hưởng chính và đồng tạo giá trị | Mục tiêu, thời gian, nỗ lực, mã nguồn, thông tin về chỗ chưa hiểu | Hiểu lỗi, giải được bài, phát triển năng lực lập trình |
| **Gia sư** | Nhà cung cấp năng lực sư phạm | Tri thức thuật toán, kỹ năng chẩn đoán, thời gian hỗ trợ | Theo dõi đúng học viên cần giúp, hỗ trợ có ngữ cảnh |
| **CatPlus/OJ** | Tác nhân số và phương tiện cung ứng | Statement, editor, submission history, năng lực chấm, dữ liệu tiến độ và chức năng gợi ý khi được bật | Phản hồi kỹ thuật nhanh, nhất quán và có thể truy vết |
| **Quản lý học vụ** | Tác nhân điều phối/authority | Quyền truy cập, quy tắc lớp, lịch và chính sách | Chất lượng dịch vụ và trách nhiệm được kiểm soát |
| **Polygon/DMOJ** | Đối tác kỹ thuật trong mạng dịch vụ | Package đề, testcase, checker, môi trường thực thi | Đề và kết quả chấm có độ tin cậy |
| **Phụ huynh** | Stakeholder/tác nhân tài trợ | Kinh phí, kỳ vọng và hỗ trợ học tập | Nhìn thấy sự tiến bộ; không phải người dùng trực tiếp của AS-IS |

### 2.3. Bên thụ hưởng chính

**Học viên** là người thụ hưởng chính. Một verdict Accepted là **output kỹ thuật**; kết quả dịch vụ là học viên hiểu cách giải và sửa được lỗi; giá trị trong bối cảnh là khả năng vận dụng kiến thức cho bài khác, kỳ thi hoặc mục tiêu cá nhân.

---

## 3. Failure được lựa chọn

### 3.1. Phát biểu failure

**Khoảng trống phản hồi sư phạm sau một chuỗi bài nộp chưa đạt.**

Khi bài nộp chưa đúng, CatPlus trả về trạng thái như WA, TLE, MLE, RTE hoặc CE, kèm điểm và thông tin thực thi. Học viên có thể xem lịch sử nộp bài và một số test được phép hiển thị. Tuy nhiên, những thông tin này chưa phải lúc nào cũng đủ để học viên biết mình sai ở đâu và nên sửa theo hướng nào.

Gia sư có thể xem tiến độ, mã nguồn và kết quả chấm của học viên trong lớp phụ trách. Học viên cũng có thể chủ động dùng Gợi ý với AI nếu chức năng được bật. Điểm còn thiếu là hệ thống chưa tự nhận biết một học viên đang bị kẹt, chưa tạo yêu cầu hỗ trợ từ chuỗi bài nộp sai và chưa phân công yêu cầu đó cho gia sư. Vì vậy, khi tự sửa hoặc gợi ý tự động chưa giải quyết được vấn đề, học viên vẫn phải chủ động hỏi hoặc gia sư phải tự phát hiện qua màn hình theo dõi.

### 3.2. Chuỗi nhân quả dự kiến

Kết quả chưa đạt nhưng chưa đủ để chẩn đoán → học viên sửa thử và nộp lại → tiếp tục không đạt → cần hỗ trợ → việc chuyển sang gia sư diễn ra thủ công → học viên phải chờ hoặc tạm dừng bài làm.

---

## 4. Resource-Value Map

### 4.1. Bảng Tài nguyên - Giá trị

| Thành phần | Áp dụng vào CatPlus |
|---|---|
| **Tác nhân** | Học viên, gia sư, quản lý học vụ, CatPlus/OJ, Polygon/DMOJ |
| **Operant resources** | Tư duy và nỗ lực của học viên; tri thức và kỹ năng sư phạm của gia sư; rule chấm, năng lực điều phối và dữ liệu tích lũy của nền tảng |
| **Operand resources** | Mã nguồn, statement, testcase/package, máy chủ, submission record, assignment và lịch sử verdict |
| **Tích hợp tài nguyên** | Học viên dùng tri thức để tạo source; OJ kết hợp source với package/checker để sinh verdict; gia sư kết hợp source, lịch sử và ngữ cảnh học tập để đưa ra hướng dẫn |
| **Đề xuất giá trị** | Một môi trường học lập trình nối lớp học, bài tập, chấm tự động và hoạt động hỗ trợ gia sư trong cùng chuỗi dữ liệu |
| **Output** | Assignment, kết quả chạy thử, submission, verdict, điểm, gợi ý tự động hoặc nhận xét hỗ trợ |
| **Outcome** | Học viên xác định được lỗi, sửa được bài và hình thành kiến thức có thể tái sử dụng |
| **Value-in-context** | Tự tin hơn khi giải bài; tiến bộ theo mục tiêu học tập; gia sư hỗ trợ đúng trọng tâm |
| **Bối cảnh/quy tắc** | Quyền truy cập theo lớp; chỉ hiển thị một phần testcase; không xem code đúng của người khác trước khi AC; gia sư chỉ xem học viên thuộc lớp phụ trách |

### 4.2. Sơ đồ Resource-Value Map

~~~mermaid
flowchart LR
    subgraph A["TÁC NHÂN VÀ TÀI NGUYÊN"]
        S["Học viên<br>mục tiêu + nỗ lực + source"]
        T["Gia sư<br>tri thức + kỹ năng sư phạm"]
        P["CatPlus/OJ<br>đề + lịch sử + năng lực chấm/gợi ý"]
    end

    subgraph I["TÍCH HỢP TÀI NGUYÊN"]
        I1["Viết và run code"]
        I2["Submit và chấm"]
        I3["Đọc lịch sử, chẩn đoán và hướng dẫn"]
    end

    VP["ĐỀ XUẤT GIÁ TRỊ<br>Môi trường luyện tập nối bài học,<br>chấm tự động và hỗ trợ gia sư"]

    subgraph V["HIỆN THỰC HÓA GIÁ TRỊ"]
        O1["Output<br>verdict / điểm / gợi ý / phản hồi"]
        O2["Outcome<br>hiểu lỗi và sửa được bài"]
        O3["Value-in-context<br>năng lực giải quyết vấn đề"]
    end

    S --> I1
    P --> VP --> I1
    I1 --> I2
    P --> I2
    I2 --> I3
    T --> I3
    I3 --> O1 --> O2 --> O3

    R["Quyền + policy testcase<br>+ quy tắc lớp học"] -.-> I2
    R -.-> I3
~~~

**Điểm đứt gãy giá trị:** hệ thống đã tạo ra output là kết quả chấm, nhưng outcome “học viên hiểu lỗi và sửa được bài” chỉ xuất hiện khi học viên và gia sư tiếp tục kết hợp thông tin, kinh nghiệm và hoạt động hỗ trợ.

---

## 5. Ba mô hình mở rộng

### 5.1. Unified Services Theory (UST)

**Lý do chọn:** Quy trình không thể diễn ra nếu học viên không cung cấp đầu vào đáng kể.

| Dạng đầu vào khách hàng | Biểu hiện trong CatPlus | Liên hệ failure |
|---|---|---|
| **Bản thân khách hàng** | Sự tham gia, tập trung, nền tảng kiến thức | Năng lực tự chẩn đoán khác nhau làm cùng một verdict tạo ra kết quả khác nhau |
| **Thông tin** | Mục tiêu, câu hỏi, ngữ cảnh chỗ chưa hiểu | Câu hỏi thiếu cấu trúc làm gia sư mất thời gian tái dựng ngữ cảnh |
| **Tài sản** | Source code và các phiên bản submission | Chuỗi source/verdict là đầu vào cần thiết để chẩn đoán |

Qua UST, nhóm nhận thấy vấn đề không chỉ nằm ở máy chấm. Cách học viên mô tả chỗ chưa hiểu và các phiên bản mã nguồn mà học viên cung cấp cũng ảnh hưởng trực tiếp tới chất lượng hỗ trợ.

### 5.2. Work System Framework

**Lý do chọn:** Mô hình giúp xem xét sự ăn khớp giữa người tham gia, quy trình, thông tin và công nghệ.

Trong quy trình hiện tại, học viên là khách hàng; học viên, gia sư và quản lý học vụ là những người tham gia. Chuỗi công việc gồm giao bài, chạy thử, nộp bài, chấm, theo dõi và hỗ trợ. Thông tin được sử dụng gồm đề bài, mã nguồn, kết quả chấm, lịch sử nộp và ngữ cảnh lớp. Các thành phần công nghệ chính là Learning Web, Academic Service, OJ, Judge Bridge, DMOJ và cơ sở dữ liệu. Dịch vụ được vận hành trong bối cảnh lớp học, luyện tập và kỳ thi, dựa trên cách học thông qua thực hành có gia sư đồng hành.

Work System cho thấy CatPlus đã có dữ liệu bài nộp và công cụ để gia sư xem mã nguồn, nhưng quy trình chưa có bước chính thức biến một chuỗi bài nộp sai thành một yêu cầu hỗ trợ có người chịu trách nhiệm.

### 5.3. Resource-Service-System (RSS)

**Lý do chọn:** CatPlus gồm nhiều hệ thống dịch vụ liên kết; failure xuất hiện ở giao diện giữa chúng.

~~~mermaid
flowchart LR
    A["Academic system<br>lớp + assignment + scope"] -->|ngữ cảnh bài được giao| O
    O["OJ/Judge system<br>run + submit + verdict"] -->|feed + source + progress| T
    T["Tutoring system<br>quan sát + chẩn đoán + hỗ trợ"] -->|review / hướng dẫn| A
    O -.->|Khoảng trống: chưa tự tạo yêu cầu hỗ trợ khi bị kẹt| T
~~~

Theo RSS, vấn đề nằm ở điểm nối giữa hệ thống chấm bài và hoạt động hỗ trợ của gia sư. Dữ liệu đã có nhưng chưa được chuyển thành một yêu cầu cần xử lý.

---

## 6. Liên hệ các mô hình với failure

| Mô hình | Cách lý giải failure | Hướng cải tiến gợi ý |
|---|---|---|
| **UST** | Đầu vào của học viên gồm mã nguồn, câu hỏi và mức độ hiểu bài có sự khác biệt lớn | Chuẩn hóa cách học viên gửi yêu cầu hỗ trợ và gắn yêu cầu với đúng bài nộp |
| **Work System** | Dữ liệu đã có nhưng thiếu một bước xử lý và người chịu trách nhiệm khi học viên bị kẹt | Bổ sung yêu cầu hỗ trợ có trạng thái và người tiếp nhận |
| **RSS** | Điểm nối giữa OJ và hoạt động gia sư còn rời rạc | Tự động chuyển ngữ cảnh bài nộp sang khu vực theo dõi của gia sư |

---

## 7. Kết luận

CatPlus là một hệ thống dịch vụ xã hội-kỹ thuật, trong đó máy chấm chỉ tạo ra kết quả kỹ thuật. Kết quả học tập xuất hiện khi học viên, nền tảng và gia sư cùng sử dụng dữ liệu và tri thức để giải quyết vấn đề.

Failure được chọn là **khoảng trống phản hồi sư phạm sau chuỗi submission chưa đạt**. Ba mô hình bổ sung cho nhau:

- UST làm rõ đầu vào đáng kể và biến thiên của học viên.
- Work System chỉ ra thiếu khớp giữa dữ liệu, quy trình và người thực hiện.
- RSS định vị failure tại điểm chuyển giao giữa OJ và hoạt động hỗ trợ của gia sư.

Ở bước tiếp theo, nhóm sẽ đi sâu vào quy trình học viên mở bài được giao, viết và nộp code, nhận kết quả chưa đạt, tự sửa hoặc chuyển sang nhận hỗ trợ từ gia sư. Những điểm cần làm rõ là thời điểm có thể kết luận học viên đang bị kẹt, thời gian chờ và việc chuyển giao giữa hệ thống chấm với gia sư, cùng các dữ liệu cần giữ lại để đánh giá hiệu quả hỗ trợ. Phần mô tả hệ thống và Resource-Value Map này sẽ tiếp tục được sử dụng khi xây dựng Journey, Service Blueprint và đề xuất cải tiến cho đồ án cuối kỳ.

