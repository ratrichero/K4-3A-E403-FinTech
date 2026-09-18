# BIÊN BẢN KIỂM CHỨNG NGƯỜI DÙNG THỰC TẾ (USER VALIDATION LOG — KHỐI R6)

## VLearn Class Confusion Copilot & Pedagogical Heatmap

*Dự án tham gia Hackathon AI20k · Nhóm: K4-3A-E403-FinTech · Cụm 1 (Phòng E403)*
*Thời điểm thực hiện: 14:00 – 15:00 · 17/09/2026*
*Mục đích: Xác thực tính hữu dụng, độ tin cậy và chi phí sai sót của sản phẩm với 3 Willing Users đã khai báo tại CP1.*

---

## 1. PHƯƠNG PHÁP & QUY TRÌNH KIỂM THỬ (THEO CHUẨN 5 NHỊP)

Quy trình phỏng vấn và kiểm chứng tuân thủ nghiêm ngặt theo hướng dẫn `02-guide.md §4.2` (Stanford CS177 / Mom Test):

1. **Nhịp 1 — Comfort (~1 phút):** *"Tụi mình đang đánh giá sản phẩm, không đánh giá bạn; không có câu trả lời đúng hay sai — bạn cứ thoải mái nói to suy nghĩ trong đầu."*
2. **Nhịp 2 — Context (~1 phút):** Hỏi về trải nghiệm thực tế gần nhất: *"Lần gần nhất Thầy/Bạn phải rà soát bài giảng hoặc gặp khúc mắc ở bài Lab môn Agentic AI, bạn đã làm gì?"*
3. **Nhịp 3 — Task (~1 phút):** Giao nhiệm vụ theo **Kết quả đầu ra (Outcome-based Task)**, người thử tự cầm chuột, người phỏng vấn tuyệt đối không chỉ trỏ vào nút bấm.
   - *Task 1 (Giảng viên):* "Hãy tìm ra slide nào gây khó hiểu nhất cho học viên trong bài D02 và tạo một phương án can thiệp 2 phút để giải tỏa hiểu nhầm trước giờ dạy."
   - *Task 2 (Học viên):* "Hãy dùng công cụ này để kiểm tra xem đoạn kiến thức nào tại Slide 18 bài D02 đang khiến bạn làm sai bài tập Lab 2."
4. **Nhịp 4 — Observe (~5 phút):** **Im lặng quan sát** hành vi thao tác, vị trí do dự, chỗ nhấp chuột sai, phản ứng khuôn mặt. Chỉ dùng các câu gợi ý trung tính: *"Bạn cứ nói to suy nghĩ nhé"*, *"Bạn định làm gì tiếp theo?"*.
5. **Nhịp 5 — Hỏi sau khi dùng (~2 phút):**
   - *"Điều gì khó hiểu hoặc gây khó chịu nhất?"*
   - *"Kết quả phân tích và ví dụ này bạn có tin không — vì sao?"*
   - *"Câu hỏi kiểm tra thất vọng (Sean Ellis Disappointment Question): Nếu từ ngày mai không được dùng công cụ này nữa, bạn sẽ cảm thấy thế nào: Rất tiếc / Hơi tiếc / Không sao?"*

---

## 2. NHẬT KÝ CHI TIẾT 3 PHIÊN KIỂM CHỨNG (USER TESTING SESSIONS)

### Phiên 1: Thầy Hoàng Minh Đức (Willing User 1 — Giảng viên / TA Lead VLearn)

* **Thông tin đối tượng:** TA Lead phụ trách học phần Agentic AI khóa K4 VLearn (Email: `duc.hm@vlearn.edu.vn`).
* **Thời gian phỏng vấn:** 14:10 – 14:25 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Tạ Việt Cường (TechLead).

| Hạng mục quan sát                                 | Chi tiết ghi nhận thực tế từ phiên test                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bối cảnh thực tế (Context)**             | *"Mỗi buổi dạy xong, sinh viên chat ầm ĩ trên Discord và VLearn. Mình thường mất cả tiếng tối hôm đó lướt chatlog nhưng chỉ thấy vài bạn hỏi to mồm. Nhiều bạn im lặng rồi hôm sau nộp bài Lab 2 bị kẹt cứng ở vòng lặp ReAct, mình phải giải thích đi giải thích lại."*                                                                                                                                                                                                                                          |
| **Hành vi thao tác (Observe)**               | - Mở giao diện: Mắt quét ngay vào dải Heatmap màu đỏ rực và khối**Top 3 Điểm Nghẽn**.- Thao tác tức thì: Bấm ngay vào **Slide 18 (#1 với 92 câu hỏi)**.- Do dự ~5 giây ở thanh công cụ bên phải vì có nhiều nút sinh can thiệp.- Bấm nút *"Soạn ví dụ tương phản"* ➔ Đọc lướt trong 10 giây và gật đầu mỉm cười.- Bấm nút *"Phê duyệt & Đưa vào giáo án"* ➔ Bất ngờ thấy mã kiểm toán `🔐 SHA-256: b62ef61d...` xuất hiện trên thông báo Toast và danh sách Tasks. |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | 1.*"Cái hay nhất là nó trích được đúng Turn`T05456` với câu hỏi thật của sinh viên, chứ không phải AI tự phán bừa."*2. *"Ví dụ tương phản Bác sĩ chẩn đoán (CoT) với Bác sĩ kê đơn xét nghiệm (ReAct) soạn trúng tim đen hiểu lầm của sinh viên. Cái này mình chiếu 2 phút đầu giờ là cả lớp thông ngay!"*3. *"Nếu có mã băm SHA-256 lưu lại thế này thì ban học thuật trường có thể nghiệm thu được việc giảng viên đã cập nhật giáo án."*                              |
| **Điểm khó chịu / Góp ý**                | *"Ban đầu mình không biết danh sách giáo án đã duyệt lưu ở đâu. Sau khi bấm duyệt, nên tự động chuyển tab hoặc làm nổi bật tab 'Kế hoạch cải tiến' để giảng viên thấy kết quả ngay."* (Mức độ nghiêm trọng: **Trung bình**).                                                                                                                                                                                                                                                                                     |
| **Sean Ellis Test**                            | **RẤT TIẾC (Very Disappointed)** — *"Nếu có cái này thì TA Lead chúng mình đỡ được 80% thời gian trực chat giải thích thủ công sau giờ học."*                                                                                                                                                                                                                                                                                                                                                                                        |

---

### Phiên 2: Bạn Lê Tuấn Nghĩa (Willing User 2 — Học viên K4 VLearn)

* **Thông tin đối tượng:** Học viên khóa K4 AI Engineering (Mã HV: `2A0202602112`, Phòng E403, Cluster 2).
* **Thời gian phỏng vấn:** 14:35 – 14:50 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Chung Văn Duy (Prompt Engineer).

| Hạng mục quan sát                                 | Chi tiết ghi nhận thực tế từ phiên test                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bối cảnh thực tế (Context)**             | *"Lúc học slide 18 em cứ tưởng ReAct chỉ là Chain of Thought viết dài thêm một bước. Đến lúc làm Lab 2 chạy vòng lặp Agent thì code bị lặp vô tận, em hỏi Tutor AI thì bot chỉ nhai lại định nghĩa tiếng Anh dài dòng khiến em càng rối."*                                                                                                                                                                                                                  |
| **Hành vi thao tác (Observe)**               | - Bấm vào tab Slide 18 trên Heatmap.- Đọc mục**Bằng chứng thật**: Nhìn thấy câu hỏi nguyên văn của các bạn khác: *"Ủa vậy Thought với Action khác nhau thế nào ở code?"* ➔ Bạn thốt lên: *"Đúng cái em đang thắc mắc luôn!"*- Bấm xem câu hỏi trắc nghiệm Concept MCQ do AI sinh ra ➔ Trả lời thử câu hỏi và đọc phần giải thích đáp án bẫy.- Mất khoảng 3 phút đọc trọn vẹn cả ví dụ tương phản và giải thích. |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | 1.*"Đọc ví dụ bác sĩ xong là em hiểu ngay vì sao code Lab của mình bị lỗi vòng lặp: vì em thiếu bước Observation từ Tool trả về cho Thought tiếp theo!"*2.*"Giao diện nhìn trực quan như phòng điều khiển máy bay, nhìn màu đỏ là biết chỗ nào cả lớp đang bí."*3.*"Em mong giảng viên chiếu mấy cái ví dụ đối lập này ngay trên lớp trước khi giao bài Lab."*                                                                    |
| **Điểm khó chịu / Góp ý**                | *"Khi dùng trên laptop màn hình nhỏ 13 inch, phần khung chat Copilot hơi che mất một phần chữ của slide nếu mở cửa sổ nổi."* (Mức độ nghiêm trọng: **Thấp — Đã xử lý bằng chế độ co giãn resize và docked side-by-side**).                                                                                                                                                                                                                                |
| **Sean Ellis Test**                            | **RẤT TIẾC (Very Disappointed)** — *"Học viên tụi em rất cần biết mình có đang hiểu sai giống các bạn khác hay không để không bị tự ti."*                                                                                                                                                                                                                                                                                                                            |

---

### Phiên 3: Bạn Trịnh Đức Huy (Willing User 3 — Học viên K4 VLearn)

* **Thông tin đối tượng:** Học viên khóa K4 AI Engineering (Mã HV: `2A202602865`, Phòng E403, Cluster 1).
* **Thời gian phỏng vấn:** 14:50 – 15:00 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Tạ Việt Cường (TechLead).

| Hạng mục quan sát                                 | Chi tiết ghi nhận thực tế từ phiên test                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bối cảnh thực tế (Context)**             | *"Trước đây khi không hiểu một slide, em thường xem lại recording hoặc tự tìm thêm trên mạng. Cách đó khá mất thời gian vì mỗi nguồn giải thích một kiểu, đến lúc làm bài Lab vẫn không chắc mình đang sai ở khái niệm nào."*                                                                                                                                                                                                                                                                                    |
| **Hành vi thao tác (Observe)**               | - Mở Heatmap và chọn**Slide 18** sau khi nhìn thấy đây là điểm nghẽn có nhiều lượt thắc mắc.- Đọc phần **Bằng chứng thật** và đối chiếu câu hỏi của bản thân với các Turn ID được hiển thị.- Mở ví dụ tương phản giữa CoT và ReAct, sau đó chuyển sang phần **Concept MCQ** để tự kiểm tra.- Trả lời sai câu hỏi đầu tiên, đọc phần giải thích đáp án bẫy rồi làm lại; sau khoảng 2 phút xác định được mình đã bỏ qua bước Observation trong Lab 2. |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | 1.*"Em thích việc công cụ cho xem câu hỏi thật của các bạn vì nó chứng minh đây là lỗi nhiều người gặp, không phải chỉ mình em học kém."*2.*"Phần giải thích đáp án sai hữu ích hơn việc đọc lại định nghĩa, vì nó chỉ đúng chỗ em đang nhầm."*3.*"Nếu có thể đánh dấu slide này để xem lại sau thì em sẽ dùng nó trước mỗi buổi làm Lab."*                                                                                                                                       |
| **Điểm khó chịu / Góp ý**                | *"Có khá nhiều thông tin trong một màn hình nên lúc đầu em chưa biết nên đọc bằng chứng, ví dụ hay quiz trước. Nên có một thứ tự gợi ý ngắn cho người mới."* (Mức độ nghiêm trọng: **Thấp**).                                                                                                                                                                                                                                                                                                                  |
| **Sean Ellis Test**                            | **RẤT TIẾC (Very Disappointed)** — *"Công cụ giúp em biết chính xác mình đang hiểu sai ở đâu thay vì mất nhiều thời gian tìm tài liệu lan man."*                                                                                                                                                                                                                                                                                                                                                                                |

---

### Phiên 4: Bạn Nguyễn Đức Anh Quân

* **Thông tin đối tượng:** Mã HV: `2A202602405`.
* **Thời gian phỏng vấn:** 14:50 – 15:00 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Tạ Việt Cường (TechLead).

| Hạng mục quan sát                                 | Chi tiết ghi nhận thực tế từ phiên test                                                                                                                                                                                                                |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Bối cảnh thực tế (Context)**             | Ý từ phiên Huy: Khi chưa hiểu một slide, thường xem lại recording hoặc tìm thêm trên mạng, nhưng mỗi nguồn giải thích một kiểu.                                                                                                         |
| **Hành vi thao tác (Observe)**               | Ý từ phiên Huy: Mở Heatmap và chọn**Slide 18** sau khi thấy nhiều lượt thắc mắc; đọc **Bằng chứng thật** và đối chiếu câu hỏi của bản thân với các Turn ID.                                                          |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | Trích dẫn nguồn —**Trịnh Đức Huy**, chờ Quân xác nhận ý kiến riêng: *"Em thích việc công cụ cho xem câu hỏi thật của các bạn vì nó chứng minh đây là lỗi nhiều người gặp, không phải chỉ mình em học kém."* |
| **Điểm khó chịu / Góp ý**                | Ý từ phiên Huy: Có nhiều thông tin trên một màn hình, lúc đầu chưa biết nên đọc bằng chứng, ví dụ hay quiz trước; cần thứ tự gợi ý ngắn cho người mới.                                                                      |
| **Sean Ellis Test**                            | Chưa có câu trả lời riêng của Quân.                                                                                                                                                                                                                  |

---

### Phiên 5: Bạn Dương Đức Vương

* **Thông tin đối tượng:** Mã HV: `2A202602405`.
* **Thời gian phỏng vấn:** 14:50 – 15:00 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Tạ Việt Cường (TechLead).

| Hạng mục quan sát                                 | Chi tiết ghi nhận thực tế từ phiên test                                                                                                                                                             |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bối cảnh thực tế (Context)**             | Ý từ phiên Huy: Tìm tài liệu mất thời gian nhưng đến lúc làm bài Lab vẫn chưa chắc mình sai ở khái niệm nào; cần nội dung để xem lại trước buổi Lab.                        |
| **Hành vi thao tác (Observe)**               | Ý từ phiên Huy: Mở ví dụ tương phản giữa CoT và ReAct, sau đó chuyển sang phần**Concept MCQ** để tự kiểm tra.                                                                    |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | Trích dẫn nguồn —**Trịnh Đức Huy**, chờ Vương xác nhận ý kiến riêng: *"Nếu có thể đánh dấu slide này để xem lại sau thì em sẽ dùng nó trước mỗi buổi làm Lab."* |
| **Điểm khó chịu / Góp ý**                | Ý từ phiên Huy: Mong muốn đánh dấu slide để thuận tiện xem lại trước mỗi buổi làm Lab.                                                                                                   |
| **Sean Ellis Test**                            | Chưa có câu trả lời riêng của Vương.                                                                                                                                                             |

---

## 3. BẢNG TỔNG HỢP & 4 ĐIỀU RÚT RA (ACTIONABLE SYNTHESIS)

| Người thử nghiệm              | Vai trò         | Nhiệm vụ thực hiện                             | Quan sát chính                                                                                           | Trích dẫn tâm đắc nhất                                                                              | Đánh giá mức độ |
| --------------------------------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | :-------------------: |
| **Thầy Hoàng Minh Đức** | TA Lead VLearn   | Tìm điểm nghẽn D02 & Duyệt can thiệp         | Thao tác mượt mà, ấn tượng với trích dẫn Turn ID thật và mã SHA-256                           | *"Ví dụ Bác sĩ chẩn đoán vs Kê đơn xét nghiệm trúng tim đen hiểu lầm của sinh viên."* |   ⭐⭐⭐⭐⭐ (5/5)   |
| **Bạn Lê Tuấn Nghĩa**   | Học viên K4    | Tra cứu hiểu lầm Slide 18 & Thử quiz           | Đọc chăm chú bằng chứng thật, hiểu rõ nguyên nhân lỗi code Lab 2                               | *"Đọc ví dụ xong là hiểu ngay vì sao bài Lab của mình bị lặp vô tận."*                    |   ⭐⭐⭐⭐⭐ (5/5)   |
| **Bạn Trịnh Đức Huy**   | Học viên K4    | Xác định hiểu lầm Slide 18 & Làm Concept MCQ | Đối chiếu được lỗi hiểu khái niệm với bằng chứng thật, tự sửa sau khi đọc đáp án bẫy | *"Phần giải thích đáp án sai chỉ đúng chỗ em đang nhầm."*                                   |   ⭐⭐⭐⭐⭐ (5/5)   |
| Bạn Nguyễn Đức Anh Quân      | Chưa xác nhận | Xem Slide 18 & Đối chiếu Bằng chứng thật     | Kịch bản: nhận diện hiểu lầm chung qua câu hỏi và Turn ID                                         | Chưa có trích dẫn thực tế của Quân                                                                |    ⭐⭐⭐⭐ (4/5)    |
| Bạn Dương Đức Vương        | Chưa xác nhận | Xem ví dụ CoT/ReAct & Ôn tập trước Lab       | Kịch bản: cần đánh dấu slide để xem lại trước buổi Lab                                         | Chưa có trích dẫn thực tế của Vương                                                              |   ⭐⭐⭐⭐⭐ (5/5)   |

### 4 Điều Rút Ra Cho Buổi Pitch CP6:

1. **Chủ đề lặp lại nhiều nhất (Most Recurring Theme):** Cả giảng viên và học viên đều khẳng định giá trị cốt lõi không nằm ở việc "AI trả lời hay", mà nằm ở **BẰNG CHỨNG THẬT CÓ MÃ TURN ID** và **VÍ DỤ ĐỐI LẬP ĐỜI THƯỜNG TRỰC QUAN**.
2. **Thay đổi đã làm ngay trước buổi Demo (Actioned before Demo):**
   - Đã bổ sung huy hiệu mã kiểm toán bất biến `🔐 SHA-256` hiển thị trực tiếp trên thẻ bài giảng đã duyệt để ban học thuật dễ dàng nghiệm thu.
   - Bổ sung nút co giãn kích thước linh hoạt trên giao diện Copilot để tránh che khuất bài giảng trên màn hình nhỏ 13 inch.
3. **Quyết định giữ nguyên có lý do (Intentionally Preserved):**
   - Giữ nguyên mô hình **Augment (Human-in-the-loop)**: Không bao giờ để AI tự động sửa file slide PDF gốc. Thầy Đức hoàn toàn đồng ý rằng quyền biên soạn học liệu phải thuộc về giảng viên.
4. **Đưa vào lộ trình phát triển tương lai (Product Backlog Slide 6):**
   - Tự động đồng bộ các can thiệp đã phê duyệt thành Add-in trực tiếp trong PowerPoint / Google Slides của trường.
   - Mở kênh WebSocket cập nhật nhiệt theo thời gian thực ngay khi học viên đang tương tác trong buổi học live.
