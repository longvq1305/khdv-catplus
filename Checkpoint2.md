# CHECKPOINT 2 - CUSTOMER JOURNEY VÀ SERVICE BLUEPRINT CATPLUS

## Quy trình: Học viên làm một bài lập trình được giao và phục hồi sau kết quả chưa đạt

- **Học phần:** Khoa học dịch vụ
- **Khách hàng chính:** Học viên
- **Nhà cung cấp:** CatPlus và gia sư

---

## 1. Liên hệ với Resource-Value Map từ Checkpoint 1

| Thành phần ở Checkpoint 1 | Vai trò trong quy trình được chọn |
|---|---|
| **Tác nhân** | Học viên, gia sư, Learning Web, Academic Service, OJ/Judge |
| **Operant resources** | Năng lực giải bài và tự debug của học viên; tri thức sư phạm của gia sư; rule chấm và năng lực điều phối của nền tảng |
| **Operand resources** | Statement, source code, testcase/package, submission, verdict, lịch sử làm bài |
| **Đề xuất giá trị** | Nối hoạt động lớp học, luyện code, chấm tự động và hỗ trợ gia sư trong cùng chuỗi dữ liệu |
| **Output** | Kết quả chạy thử, submission, verdict, điểm, bình luận gợi ý hoặc nhận xét hỗ trợ |
| **Outcome** | Học viên hiểu lỗi và sửa được bài |
| **Value-in-context** | Nâng cao năng lực giải quyết vấn đề trong mục tiêu học tập cá nhân |
| **Quy tắc** | Quyền truy cập theo lớp, chính sách hiển thị testcase, phạm vi phụ trách của gia sư, không xem code đúng của người khác trước khi AC |

Từ Resource-Value Map ở Checkpoint 1, nhóm chọn đi sâu vào khoảng trống giữa kết quả chấm chưa đạt và hoạt động hỗ trợ của gia sư. Đây là điểm mà output kỹ thuật chưa chuyển thành outcome học tập.

~~~mermaid
flowchart LR
    subgraph A["TÁC NHÂN VÀ TÀI NGUYÊN"]
        S["Học viên<br>kiến thức + nỗ lực + mã nguồn"]
        T["Gia sư<br>tri thức + kỹ năng sư phạm"]
        P["CatPlus/OJ<br>đề bài + lịch sử + năng lực chấm"]
    end

    subgraph I["TÍCH HỢP TÀI NGUYÊN"]
        I1["Viết và chạy thử"]
        I2["Nộp bài và chấm"]
        I3["Đọc lịch sử, chẩn đoán và hướng dẫn"]
    end

    VP["ĐỀ XUẤT GIÁ TRỊ<br>Môi trường luyện tập nối bài học,<br>chấm tự động và hỗ trợ gia sư"]

    subgraph V["GIÁ TRỊ ĐƯỢC HIỆN THỰC HÓA"]
        O1["Output<br>kết quả chấm / gợi ý / phản hồi"]
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
    R["Quyền truy cập + chính sách testcase<br>+ quy tắc lớp học"] -.-> I2
    R -.-> I3
~~~

---

## 2. Phạm vi quy trình

| Thuộc tính | Xác định |
|---|---|
| **Process instance** | Một học viên làm một Problem thuộc một Assignment/Problem Set được giao |
| **Khách hàng/người dùng** | Học viên |
| **Nhà cung cấp** | CatPlus; gia sư khi cần hỗ trợ |
| **Trigger** | Học viên mở Problem được giao và bắt đầu làm bài |
| **Happy outcome** | Học viên hiểu và sửa được lỗi; submission đạt Accepted; tiến độ bài được cập nhật |
| **Alternative end state** | Học viên dừng phiên khi chưa đạt và cần tiếp tục/hỗ trợ sau |
| **Đầu vào** | Statement, source code, kiến thức học viên, package/checker và ngữ cảnh assignment |
| **Trong biên** | Đọc đề, viết/run, submit, xem verdict/lịch sử, tự sửa, gia sư xem submission và hỗ trợ |
| **Ngoài biên** | Soạn đề trên Polygon, giao assignment trước đó, quản lý học phí và đánh giá kết quả dài hạn |

### Chuỗi hoạt động chính

~~~mermaid
flowchart LR
    A["1. Mở đề"] --> B["2. Viết và chạy thử"]
    B --> C["3. Submit"]
    C --> D{"4. Verdict?"}
    D -->|AC| E["5A. Hoàn thành"]
    D -->|Non-AC| F["5B. Đọc kết quả và sửa"]
    F --> C
    F --> I["Dùng Gợi ý với AI<br>nếu chức năng được bật"]
    I --> B
    F --> G["6. Cần hỗ trợ"]
    G --> H["Gia sư xem ngữ cảnh và hướng dẫn"]
    H --> B
~~~

---

## 3. Customer Journey Map AS-IS

### 3.1. Journey theo góc nhìn học viên

| Stage | Mục tiêu của học viên | Hành động | Touchpoint/kênh | Evidence/kết quả nhìn thấy | Trải nghiệm dự kiến và pain point |
|---|---|---|---|---|---|
| **1. Hiểu bài** | Biết bài yêu cầu gì | Mở Problem, đọc statement, ví dụ và giới hạn | Learning Web - Problem workspace | Statement, input/output mẫu, starter code | Có thể lúng túng nếu chưa nhận ra dạng bài |
| **2. Tạo lời giải** | Chuyển ý tưởng thành code | Viết code, chọn ngôn ngữ, chạy thử với mẫu | Monaco editor và chức năng Run | Compile/runtime output, so sánh sample nếu có | Phản hồi run giúp sửa lỗi cục bộ nhưng không chứng minh đúng trên test ẩn |
| **3. Gửi chấm** | Biết lời giải có đạt không | Nhấn Submit và chờ | Nút Submit, vùng kết quả | Trạng thái pending/judging rồi verdict, điểm, thời gian, bộ nhớ | Việc chờ kết quả làm gián đoạn mạch suy nghĩ khi hệ thống xử lý chậm |
| **4. Diễn giải non-AC** | Biết nguyên nhân và bước tiếp theo | Mở chi tiết submission, xem verdict/lịch sử và test được phép reveal | Result và Submission History | WA/TLE/MLE/RTE/CE; một phần test có thể được hiển thị | **[P1]** Verdict có thể chưa đủ để học viên yếu xác định cơ chế sai |
| **5. Tự phục hồi** | Sửa được bài bằng năng lực bản thân | Đặt test, sửa mã nguồn, chạy thử; có thể chủ động dùng Gợi ý với AI khi chức năng được bật; nộp lại | Editor, Run, Submit, History, Gợi ý với AI | Chuỗi phiên bản mã nguồn, kết quả chấm và bình luận gợi ý tại dòng code | Có nguy cơ lặp sửa-thử-nộp hoặc nhận gợi ý nhưng vẫn chưa hiểu nguyên nhân |
| **6. Nhận hỗ trợ và hoàn thành** | Có hướng dẫn đúng ngữ cảnh, tự sửa và đạt AC | Báo gia sư hoặc chờ gia sư phát hiện; nhận gợi ý; sửa và submit | Phiên học, kênh trao đổi và màn hình theo dõi của gia sư | Gia sư xem mã nguồn/kết quả; học viên nhận hướng dẫn; cuối cùng AC hoặc tạm dừng | **[P2]** Chưa có yêu cầu hỗ trợ tự động nên việc chuyển giao và thời gian chờ chưa được quản lý |

### 3.2. Journey trực quan

~~~mermaid
journey
    title Hành trình AS-IS: làm bài và phục hồi sau non-AC
    section Hiểu và thử
      Đọc statement: 4: Học viên
      Viết code và chạy mẫu: 4: Học viên, CatPlus
    section Chấm bài
      Submit và chờ verdict: 3: Học viên, OJ
      Nhận non-AC chưa đủ chẩn đoán: 2: Học viên
    section Phục hồi
      Sửa và submit lại: 2: Học viên
      Tìm hoặc chờ hỗ trợ: 1: Học viên, Gia sư
      Nhận hướng dẫn và đạt AC: 5: Học viên, Gia sư
~~~

> Thang điểm 1-5 thể hiện đánh giá của nhóm về trải nghiệm học viên tại từng giai đoạn.

Trong quy trình hiện tại, Gợi ý với AI là một nhánh tùy chọn do học viên chủ động sử dụng. Chức năng này không tự xác định học viên bị kẹt và không tự chuyển trường hợp đó cho gia sư.

### 3.3. Hai pain point trọng tâm

1. **P1 - Khoảng trống chẩn đoán:** verdict và phần testcase được phép reveal chưa chắc đủ để mọi học viên biến output kỹ thuật thành hiểu biết.
2. **P2 - Khoảng trống chuyển giao:** gia sư có thể xem bài nộp, mã nguồn và tiến độ, nhưng hệ thống chưa tự tạo yêu cầu hỗ trợ và chuyển cho một gia sư cụ thể khi học viên có chuỗi bài nộp chưa đạt.

---

## 4. Service Blueprint AS-IS

### 4.1. Ma trận năm tầng

| Tầng / Stage | 1. Mở đề | 2. Viết và Run | 3. Submit/chấm | 4. Nhận non-AC | 5. Tự sửa / cần giúp | 6. Hỗ trợ / kết thúc |
|---|---|---|---|---|---|---|
| **Evidence** | Statement, ví dụ, giới hạn | Editor, run output | Submission ID, pending/judging | Verdict, điểm, thời gian/bộ nhớ, history, test được reveal | Mã nguồn mới, lịch sử nhiều lần; bình luận AI nếu học viên yêu cầu và chức năng được bật | Lời hướng dẫn của gia sư, kết quả AC hoặc trạng thái chưa hoàn thành |
| **Customer actions** | Đọc và xác định yêu cầu | Viết code, chọn ngôn ngữ, chạy mẫu | Nhấn Submit, theo dõi trạng thái | Đọc kết quả, so sánh các lần nộp | **[R1]** Sửa, chạy thử, có thể yêu cầu AI gợi ý rồi nộp lại; báo cần giúp nếu không tiến triển | **[W1]** Chờ được hỗ trợ, sau đó áp dụng hướng dẫn, tự sửa và nộp lại |
| **LINE OF INTERACTION** | \- | Học viên tương tác Learning Web | Học viên gửi yêu cầu tới OJ | Learning Web trả kết quả | Học viên tiếp tục tương tác hoặc chủ động báo gia sư | **[H1]** Trường hợp được chuyển sang gia sư để trao đổi và hướng dẫn |
| **Frontstage** | Learning Web hiển thị Problem đúng phạm vi | Giao diện gửi yêu cầu chạy thử và hiển thị kết quả | Giao diện tạo submission và cập nhật trạng thái | **[F1]** Giao diện hiển thị verdict/history nhưng có thể chưa đủ để học viên biết cách sửa | Giao diện tiếp tục hiển thị lịch sử; hiển thị nút và bình luận Gợi ý với AI nếu chức năng được bật | Gia sư trao đổi và hướng dẫn học viên |
| **LINE OF VISIBILITY** | \- | Phân cách giao diện/encounter nhìn thấy với xử lý nội bộ | \- | \- | \- | \- |
| **Backstage** | Kiểm tra quyền học viên và lấy dữ liệu bài | Tạo lần chạy thử và lưu kết quả | Tạo submission, đưa bài vào hàng chờ chấm | Nhận kết quả từ máy chấm và cập nhật lịch sử | Khi học viên yêu cầu, OJ chuẩn bị ngữ cảnh và gọi dịch vụ gợi ý; đồng thời tổng hợp các lần nộp cho màn hình gia sư nhưng chưa tự tạo yêu cầu hỗ trợ | **[SR1]** Gia sư mở bài nộp, thử phương án sửa và chuẩn bị hướng dẫn |
| **Support processes** | Identity, Academic và kho bài Polygon | OJ, cơ sở dữ liệu và checker | Judge Bridge và DMOJ | Chính sách hiển thị testcase và lưu lịch sử | Dịch vụ gợi ý AI nếu được bật, Tutor API và màn hình theo dõi lớp | Dữ liệu lớp, buổi học và nhận xét học viên |

### 4.2. Sơ đồ Blueprint rút gọn

~~~mermaid
flowchart TB
    subgraph EV["EVIDENCE"]
        E1["Statement"] --> E2["Editor / Run"] --> E3["Judging"] --> E4["Non-AC + History"] --> E5["Chuỗi phiên bản / gợi ý tùy chọn"] --> E6["Hướng dẫn / AC"]
    end

    subgraph CA["CUSTOMER ACTIONS"]
        C1["Đọc đề"] --> C2["Viết và run"] --> C3["Submit"] --> C4["Đọc non-AC"] --> C5["R1: Sửa hoặc cần giúp"] --> C6["W1: Chờ và áp dụng hướng dẫn"]
    end

    LI["--------------- LINE OF INTERACTION ---------------"]

    subgraph FS["FRONTSTAGE"]
        F1A["Hiển thị Problem"] --> F2["Nhận run"] --> F3["Nhận submit / hiển thị trạng thái"] --> F4["F1: Hiển thị verdict<br>chưa đủ chẩn đoán"] --> F5["Hiển thị lịch sử / gợi ý tùy chọn"] --> F6["H1: Chuyển sang gia sư<br>để hướng dẫn"]
    end

    LV["---------------- LINE OF VISIBILITY ----------------"]

    subgraph BS["BACKSTAGE"]
        B1["Kiểm tra quyền"] --> B2["Xử lý run"] --> B3["Tạo submission và chuyển máy chấm"] --> B4["Lưu kết quả"] --> B5["Xử lý gợi ý / tổng hợp theo lớp"] --> B6["SR1: Gia sư thử và<br>chuẩn bị hướng dẫn"]
    end

    subgraph SP["SUPPORT PROCESSES"]
        S1["Identity + Academic"] --> S2["OJ + CSDL"] --> S3["Judge Bridge + DMOJ"] --> S4["Quy tắc hiển thị kết quả"] --> S5["AI tùy chọn + Tutor API"] --> S6["Dữ liệu lớp học"]
    end

    E1 --- C1
    E2 --- C2
    E3 --- C3
    E4 --- C4
    E5 --- C5
    E6 --- C6
    C2 -.-> F2
    C3 -.-> F3
    C4 -.-> F4
    C5 -.-> F5
    C6 -.-> F6
    F2 -.-> B2
    F3 -.-> B3
    F4 -.-> B4
    F5 -.-> B5
    F6 -.-> B6
    B1 -.-> S1
    B2 -.-> S2
    B3 -.-> S3
    B4 -.-> S4
    B5 -.-> S5
    B6 -.-> S6
~~~

**Cách đọc hai đường phân cách**

- **Line of interaction:** nằm giữa Customer actions và Frontstage; mọi lần click, submit, xem kết quả hoặc trao đổi với gia sư đi qua đường này.
- **Line of visibility:** nằm giữa Frontstage và Backstage; học viên thấy giao diện, kết quả chấm và hướng dẫn nhưng không thấy hoạt động điều phối máy chấm, lưu dữ liệu hay tổng hợp tiến độ cho gia sư.

---

## 5. Chẩn đoán trên Blueprint

Trên Blueprint, P1 thể hiện thành failure point F1 và vòng làm lại R1; P2 thể hiện thành handoff H1 và waiting point W1.

| Mã | Loại | Vị trí | Biểu hiện | Ảnh hưởng |
|---|---|---|---|---|
| **[F1]** | Failure point | Stage 4, Frontstage | Kết quả chưa đạt nhưng thông tin chưa đủ để học viên biết bước sửa tiếp theo | Học viên dễ mất phương hướng |
| **[R1]** | Rework | Stage 4-5-3 | Học viên sửa và nộp lại nhiều lần mà chưa hiểu nguyên nhân | Tốn thời gian học viên và tài nguyên chấm |
| **[H1]** | Handoff | Từ OJ sang gia sư | Gia sư có thể xem bài nộp nhưng chưa có yêu cầu hỗ trợ tự động | Ngữ cảnh hỗ trợ được chuyển giao chậm hoặc không đầy đủ |
| **[W1]** | Waiting point | Stage 5-6 | Học viên chờ đến khi hỏi được gia sư hoặc gia sư nhận thấy vấn đề | Mạch suy nghĩ bị gián đoạn, bài có thể bị bỏ dở |
| **[SR1]** | Service recovery | Stage 6 | Gia sư xem mã nguồn, kết quả chấm và hướng dẫn học viên tự sửa | Học viên hiểu lỗi, tiếp tục làm và có thể đạt AC |

### Chuỗi nguyên nhân

~~~mermaid
flowchart LR
    F1["F1: non-AC chưa đủ chẩn đoán"] --> R1["R1: sửa và submit lại"]
    R1 -->|tiếp tục thất bại| H1["H1: cần bàn giao sang gia sư"]
    H1 --> W1["W1: chờ gia sư tiếp nhận"]
    W1 --> SR1["SR1: gia sư chẩn đoán và hướng dẫn"]
    SR1 --> AC["Học viên tự sửa và đạt AC"]
~~~

---

## 6. Truy vết vấn đề về Resource-Value Map ở Checkpoint 1

| Vấn đề trong quy trình | Actor liên quan | Resource liên quan | Rule/bối cảnh liên quan | Đứt gãy giá trị |
|---|---|---|---|---|
| **F1 - khoảng trống chẩn đoán** | Học viên, CatPlus/OJ | Kết quả chấm, test được hiển thị, kỹ năng tự debug | Không lộ test ẩn hoặc lời giải | Output chưa chuyển thành hiểu biết |
| **R1 - rework** | Học viên, OJ | Nỗ lực, mã nguồn, tài nguyên chấm, lịch sử | Chưa có quy tắc nhận diện học viên bị kẹt | Tài nguyên bị tiêu hao nhưng kết quả học tập không tăng |
| **H1 - handoff** | OJ, Academic, gia sư | Bài nộp, mã nguồn, ngữ cảnh lớp, tri thức gia sư | Gia sư chỉ xem học viên thuộc lớp phụ trách | Các tài nguyên chưa được kết hợp đúng thời điểm |
| **W1 - waiting** | Học viên, gia sư, quản lý | Thời gian và năng lực hỗ trợ | Chưa có quy trình tiếp nhận yêu cầu hỗ trợ | Giá trị phụ thuộc vào phối hợp thủ công |

---

## 7. Một giả thuyết cải tiến TO-BE

> **Nếu CatPlus tự tạo một yêu cầu hỗ trợ sau ba lần nộp chưa đạt liên tiếp, gắn yêu cầu với học viên và gia sư phụ trách, đồng thời đính kèm mã nguồn, kết quả chấm và lịch sử nộp bài, thì số lần sửa-nộp lại không có định hướng và thời gian chờ hỗ trợ sẽ giảm.**

---

## 8. Kết luận

Journey cho thấy pain point chính xuất hiện sau khi học viên nhận kết quả chưa đạt và không biết nên sửa theo hướng nào. Blueprint cho thấy vấn đề không nằm riêng ở máy chấm: dữ liệu bài nộp và năng lực của gia sư đã có, nhưng chưa được nối thành một quy trình hỗ trợ chủ động.

Ở Checkpoint 2, quy trình được xác định từ lúc học viên mở bài đến khi đạt AC hoặc tạm dừng để tiếp tục sau. Các vấn đề tìm thấy trên Journey và Blueprint cũng được nối lại với tác nhân, tài nguyên và quy tắc trong Resource-Value Map của Checkpoint 1. Đây là cơ sở để tiếp tục mô tả chi tiết các nhánh AC/non-AC, rework, handoff và recovery khi thiết kế quy trình.
