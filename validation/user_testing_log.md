# BIÊN BẢN KIỂM CHỨNG NGƯỜI DÙNG THỰC TẾ (USER VALIDATION LOG — KHỐI R6)
## VLearn Class Confusion Copilot & Pedagogical Heatmap
*Dự án tham gia Hackathon AI20k · Nhóm: K4-3A-E403-FinTech · Cụm 1 (Phòng E403)*  
*Thời điểm thực hiện: 14:00 – 15:00 · 17/09/2026*  
*Mục đích: Xác thực tính hữu dụng, độ tin cậy và chi phí sai sót của sản phẩm với 2 Willing Users đã khai báo tại CP1.*

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

## 2. NHẬT KÝ CHI TIẾT 2 PHIÊN KIỂM CHỨNG (USER TESTING SESSIONS)

### Phiên 1: Thầy Hoàng Minh Đức (Willing User 1 — Giảng viên / TA Lead VLearn)
* **Thông tin đối tượng:** TA Lead phụ trách học phần Agentic AI khóa K4 VLearn (Email: `duc.hm@vlearn.edu.vn`).
* **Thời gian phỏng vấn:** 14:10 – 14:25 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Tạ Việt Cường (TechLead).

| Hạng mục quan sát | Chi tiết ghi nhận thực tế từ phiên test |
|---|---|
| **Bối cảnh thực tế (Context)** | *"Mỗi buổi dạy xong, sinh viên chat ầm ĩ trên Discord và VLearn. Mình thường mất cả tiếng tối hôm đó lướt chatlog nhưng chỉ thấy vài bạn hỏi to mồm. Nhiều bạn im lặng rồi hôm sau nộp bài Lab 2 bị kẹt cứng ở vòng lặp ReAct, mình phải giải thích đi giải thích lại."* |
| **Hành vi thao tác (Observe)** | - Mở giao diện: Mắt quét ngay vào dải Heatmap màu đỏ rực và khối **Top 3 Điểm Nghẽn**.<br>- Thao tác tức thì: Bấm ngay vào **Slide 18 (#1 với 92 câu hỏi)**.<br>- Do dự ~5 giây ở thanh công cụ bên phải vì có nhiều nút sinh can thiệp.<br>- Bấm nút *"Soạn ví dụ tương phản"* ➔ Đọc lướt trong 10 giây và gật đầu mỉm cười.<br>- Bấm nút *"Phê duyệt & Đưa vào giáo án"* ➔ Bất ngờ thấy mã kiểm toán `🔐 SHA-256: b62ef61d...` xuất hiện trên thông báo Toast và danh sách Tasks. |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | 1. *"Cái hay nhất là nó trích được đúng Turn `T05456` với câu hỏi thật của sinh viên, chứ không phải AI tự phán bừa."*<br>2. *"Ví dụ tương phản Bác sĩ chẩn đoán (CoT) với Bác sĩ kê đơn xét nghiệm (ReAct) soạn trúng tim đen hiểu lầm của sinh viên. Cái này mình chiếu 2 phút đầu giờ là cả lớp thông ngay!"*<br>3. *"Nếu có mã băm SHA-256 lưu lại thế này thì ban học thuật trường có thể nghiệm thu được việc giảng viên đã cập nhật giáo án."* |
| **Điểm khó chịu / Góp ý** | *"Ban đầu mình không biết danh sách giáo án đã duyệt lưu ở đâu. Sau khi bấm duyệt, nên tự động chuyển tab hoặc làm nổi bật tab 'Kế hoạch cải tiến' để giảng viên thấy kết quả ngay."* (Mức độ nghiêm trọng: **Trung bình**). |
| **Sean Ellis Test** | **RẤT TIẾC (Very Disappointed)** — *"Nếu có cái này thì TA Lead chúng mình đỡ được 80% thời gian trực chat giải thích thủ công sau giờ học."* |

---

### Phiên 2: Bạn Lê Tuấn Nghĩa (Willing User 2 — Học viên K4 VLearn)
* **Thông tin đối tượng:** Học viên khóa K4 AI Engineering (Mã HV: `2A0202602112`, Phòng E403, Cluster 2).
* **Thời gian phỏng vấn:** 14:35 – 14:50 · 17/09/2026 tại Phòng Lab E403.
* **Người thực hiện phỏng vấn & ghi chép:** Nguyễn Thị Chinh (Product Manager) & Chung Văn Duy (Prompt Engineer).

| Hạng mục quan sát | Chi tiết ghi nhận thực tế từ phiên test |
|---|---|
| **Bối cảnh thực tế (Context)** | *"Lúc học slide 18 em cứ tưởng ReAct chỉ là Chain of Thought viết dài thêm một bước. Đến lúc làm Lab 2 chạy vòng lặp Agent thì code bị lặp vô tận, em hỏi Tutor AI thì bot chỉ nhai lại định nghĩa tiếng Anh dài dòng khiến em càng rối."* |
| **Hành vi thao tác (Observe)** | - Bấm vào tab Slide 18 trên Heatmap.<br>- Đọc mục **Bằng chứng thật**: Nhìn thấy câu hỏi nguyên văn của các bạn khác: *"Ủa vậy Thought với Action khác nhau thế nào ở code?"* ➔ Bạn thốt lên: *"Đúng cái em đang thắc mắc luôn!"*<br>- Bấm xem câu hỏi trắc nghiệm Concept MCQ do AI sinh ra ➔ Trả lời thử câu hỏi và đọc phần giải thích đáp án bẫy.<br>- Mất khoảng 3 phút đọc trọn vẹn cả ví dụ tương phản và giải thích. |
| **Trích dẫn nguyên văn (Verbatim Quotes)** | 1. *"Đọc ví dụ bác sĩ xong là em hiểu ngay vì sao code Lab của mình bị lỗi vòng lặp: vì em thiếu bước Observation từ Tool trả về cho Thought tiếp theo!"*<br>2. *"Giao diện nhìn trực quan như phòng điều khiển máy bay, nhìn màu đỏ là biết chỗ nào cả lớp đang bí."*<br>3. *"Em mong giảng viên chiếu mấy cái ví dụ đối lập này ngay trên lớp trước khi giao bài Lab."* |
| **Điểm khó chịu / Góp ý** | *"Khi dùng trên laptop màn hình nhỏ 13 inch, phần khung chat Copilot hơi che mất một phần chữ của slide nếu mở cửa sổ nổi."* (Mức độ nghiêm trọng: **Thấp — Đã xử lý bằng chế độ co giãn resize và docked side-by-side**). |
| **Sean Ellis Test** | **RẤT TIẾC (Very Disappointed)** — *"Học viên tụi em rất cần biết mình có đang hiểu sai giống các bạn khác hay không để không bị tự ti."* |

---

## 3. BẢNG TỔNG HỢP & 4 ĐIỀU RÚT RA (ACTIONABLE SYNTHESIS)

| Người thử nghiệm | Vai trò | Nhiệm vụ thực hiện | Quan sát chính | Trích dẫn tâm đắc nhất | Đánh giá mức độ |
|---|---|---|---|---|:---:|
| **Thầy Hoàng Minh Đức** | TA Lead VLearn | Tìm điểm nghẽn D02 & Duyệt can thiệp | Thao tác mượt mà, ấn tượng với trích dẫn Turn ID thật và mã SHA-256 | *"Ví dụ Bác sĩ chẩn đoán vs Kê đơn xét nghiệm trúng tim đen hiểu lầm của sinh viên."* | ⭐⭐⭐⭐⭐ (5/5) |
| **Bạn Lê Tuấn Nghĩa** | Học viên K4 | Tra cứu hiểu lầm Slide 18 & Thử quiz | Đọc chăm chú bằng chứng thật, hiểu rõ nguyên nhân lỗi code Lab 2 | *"Đọc ví dụ xong là hiểu ngay vì sao bài Lab của mình bị lặp vô tận."* | ⭐⭐⭐⭐⭐ (5/5) |

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
