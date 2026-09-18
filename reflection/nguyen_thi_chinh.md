# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Nguyễn Thị Chinh**  
*Mã học viên:* `2A0202602876`  
*Vai trò trong nhóm:* **Nghiên cứu thuật toán**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`
---

### 1. Vai trò và trách nhiệm trong dự án
Trong dự án này, tôi đảm nhiệm vai trò **Nghiên cứu thuật toán**. Công việc chính của tôi là:
- Lập trình bản mẫu chạy thực tế (Working Prototype) cho mốc **Checkpoint 3 (CP3)**.
- Đi tìm câu trả lời cho bản chất bài toán: *"Làm thế nào để xác định chính xác một slide bài giảng đang thực sự làm học viên bế tắc?"*
- Phân tích dữ liệu, nghiên cứu và xây dựng công thức tính điểm nhiệt cho slide (Pedagogical Heat Score) dựa trên dữ liệu thật của lớp học.
- Review code của thành viên trong nhóm, chỉ ra các điểm chưa hợp lý và đề xuất hướng cải tiến.

---

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm

#### 2.1. Rà soát hệ thống v1 và tìm ra các điểm chưa hợp lý
Khi đọc mã nguồn ban đầu của nhóm và phân tích dữ liệu, tôi nhận thấy một số điểm cần cải tiến như: hardcode, dùng limit khi query câu hỏi từ SQL, thiếu cache, cách chuẩn hoá dữ liệu và tính heat score.

#### 2.2. Nghiên cứu và đề xuất cách tính điểm nhiệt mới (2 chiều: Lan tỏa & Bế tắc)
Để giải quyết các vấn đề trên, tôi đề xuất chia việc đánh giá slide thành **2 khía cạnh độc lập**, đưa về thang điểm chuẩn từ 0 đến 1:

1. **Chiều 1: Độ lan tỏa trong lớp (Breadth - Khó khăn này là của số đông hay cá biệt?)**
   - Tính bằng: `Số sinh viên gặp khó ở slide / Tổng sĩ số lớp`.
   - Giúp đánh giá công bằng: biết chính xác bao nhiêu phần trăm lớp học đang gặp vấn đề, không bị phụ thuộc vào việc lớp đông hay lớp vắng.

2. **Chiều 2: Mức độ bế tắc (Depth - Học viên khó hiểu ở mức độ nào?)**
   - Kết hợp 2 yếu tố:
     + **Độ khó của câu hỏi theo Thang đo nhận thức Bloom:** Câu hỏi hiểu sai bản chất kiến thức được tính điểm cao nhất (hệ số 3.0), câu hỏi giải thích hoặc áp dụng ví dụ tính hệ số 1.5, câu hỏi ngoài lề hoặc chào hỏi chỉ tính hệ số 0.5.
     + **Độ dồn dập:** Sinh viên có phải hỏi đi hỏi lại nhiều lần ở cùng một slide hay không. Nếu hỏi đi hỏi lại nhiều mà chưa hiểu nghĩa là mức độ bế tắc càng sâu.

3. **Dùng Trung vị (Median) để chia ranh giới công bằng:**
   - Thay vì lấy điểm trung bình (dễ bị những slide có số câu hỏi đột biến như Slide 1 kéo lệch thang đo), tôi sử dụng **Trung vị (Median)** làm mốc phân chia.
   - Thêm mức sàn tối thiểu để khi cả lớp đều học tốt, hệ thống sẽ không tạo ra báo động giả.

#### 2.3. Thiết kế Bảng 4 nhóm hành động cho giảng viên
Dựa vào 2 trục điểm trên, tôi xếp các slide vào 4 nhóm hành động rõ ràng giúp giảng viên ra quyết định ngay lập tức:
- **Nhóm 1 (Nhiều người hỏi + Câu hỏi khó):** Điểm nghẽn thực sự của bài giảng $\rightarrow$ **Hành động: Giảng viên dành 15 phút đầu giờ để giảng lại cho cả lớp**.
- **Nhóm 2 (Ít người hỏi + Nhưng bế tắc sâu):** Vấn đề riêng của một vài bạn $\rightarrow$ **Hành động: Giao trợ giảng (TA) kèm riêng 1-1**, tránh làm mất thời gian của cả lớp.
- **Nhóm 3 (Nhiều người hỏi + Nhưng câu hỏi đơn giản):** Thường do slide chữ nhỏ, ký hiệu lạ hoặc nhầm số liệu $\rightarrow$ **Hành động: Sửa lại cách trình bày slide, thêm chú thích**.
- **Nhóm 4 (Ít người hỏi + Câu hỏi dễ):** Vùng an toàn $\rightarrow$ **Không cần can thiệp**.

Ngoài ra, tôi áp dụng cách lọc tối ưu (Pareto) để tự động tìm ra các slide vừa có số người hỏi nhiều nhất, vừa có mức độ khó cao nhất để giảng viên ưu tiên xử lý trước tiên => heatmap.

#### 2.4. Xây dựng bản mẫu chạy thực tế (Prototype) ban đầu cho Checkpoint 3
- Xây dựng luồng xử lý hoàn chỉnh để tạo ra bản mẫu chạy thực tế ban đầu phục vụ mốc **Checkpoint 3 (CP3)**: Giao diện giảng viên xem báo cáo, hiển thị heatmap của các slide trong lecture, tóm tắt nội dung khúc mắc của sinh viên và gợi ý can thiệp sư phạm.

---

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
- AI giúp tôi kiểm tra các trường hợp đặc biệt (như slide không có ai hỏi thì chia cho 0 thế nào, cách xử lý khi một bạn gửi quá nhiều câu hỏi liên tục).
- AI hỗ trợ tôi dựng nhanh khung code Python đọc cơ sở dữ liệu SQLite, tính toán trung vị và viết script chạy thử nghiệm tự động để xuất kết quả ra màn hình.
- AI cùng tôi phản biện về các công thức tính score mà tôi và AI đề xuất, từ đó tôi đã điều chỉnh công thức để phù hợp với thực tế.

---

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case):** Ban đầu, nhóm nghĩ đơn giản rằng: *"Cứ đếm tổng số câu hỏi và số sinh viên hỏi, slide nào số to nhất thì slide đó nóng nhất"*. Khi chạy thử, Slide 1 (trang bìa) có nhiều bạn vào chào hỏi nên điểm vọt lên cao nhất lớp, trong khi các slide chứa kiến thức chuyên sâu dù sinh viên rất khó hiểu nhưng ít câu hỏi hơn lại bị xếp ở phía sau.
* **Hậu quả & Phân tích:** Nếu giảng viên nhìn vào kết quả này, họ sẽ bị hướng dẫn sai: mất thời gian giảng lại trang bìa môn học, trong khi bỏ quên những slide kiến thức thật sự quan trọng. Nguyên nhân là do cách làm cũ chỉ đếm số lượng một cách máy móc mà không quan tâm đến nội dung và bản chất của câu hỏi.
* **Bài học & Tự nhìn nhận:**
  - Trong giáo dục, dữ liệu phải được đặt đúng vào ngữ cảnh (câu hỏi chào hỏi khác hoàn toàn với câu hỏi hiểu sai bản chất).
  - Cần cải thiện model phân loại intent của câu hỏi của sinh viên. 
  - Tôi nhận thấy trong công thức của mình vẫn còn một số hệ số đặt theo cảm tính (như tỷ lệ 0.7 và 0.3) mà chưa có số liệu thực nghiệm lớn để chứng minh là tối ưu tuyệt đối.
  - Dù tôi đã kiên định bảo vệ phương pháp của mình, nhưng tôi nhận ra mình cần cải thiện cách giải thích và trình bày để thuyết phục các thành viên trong nhóm.

