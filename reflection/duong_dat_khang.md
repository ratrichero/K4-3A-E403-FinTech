# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Dương Đạt Khang**  
*Mã học viên:* `2A0202602624`  
*Vai trò trong nhóm:* **Data Scientist / Analytics & Validation**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`

---

### 1. Vai trò và trách nhiệm trong dự án
Trong dự án này, tôi phụ trách toàn bộ tầng dữ liệu nền tảng: khai phá 13.494 lượt hội thoại thật từ tệp `tutor_turns.csv`, xây dựng thuật toán tính toán điểm nhiệt tất định, thiết lập bộ kiểm thử chuẩn hóa Golden Set 20 ca, và tham gia đồng phỏng vấn người dùng thực tế trong Khối R6.

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm
* **Khai phá dữ liệu (Data Mining):** Phân tích 13.494 dòng logs để phát hiện các con số biết nói: trường `understanding_level` bị bỏ trống 99.85%, 89.8% hành vi của bot chỉ là nhắc lại định nghĩa (`review_concept`), và bóc tách thành công 7.284 lượt hỏi có metadata `(Trang N, đoạn được chọn: "...")`.
* **Xây dựng Thuật toán Bản đồ nhiệt (`tools.py`):** Viết logic tính toán chỉ số bối rối (Confusion Score) dựa trên số lượng học viên duy nhất bối rối và trọng số mức độ nghiêm trọng của câu hỏi, định vị chính xác Slide 18 là điểm nghẽn số 1 của bài D02 với 92 lượt hỏi.
* **Xây dựng Bộ Golden Evaluation Set (20 ca):** Thiết kế 20 ca kiểm thử bao phủ 4 lớp chỗ khó: 10 ca Sư phạm, 5 ca Thường nhật Baseline, và 5 ca Ranh giới bảo mật.
* **Kiểm chứng người dùng Khối R6:** Đồng thực hiện phỏng vấn 5 nhịp với Thầy Hoàng Minh Đức và bạn Lê Tuấn Nghĩa, ghi nhận trích dẫn nguyên văn và kết quả 100% Sean Ellis Disappointment Rate.

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
* AI giúp tôi viết các biểu thức chính quy (Regex) phức tạp để bóc tách sạch sẽ số trang slide và đoạn văn bản bôi đen từ các chuỗi câu hỏi không đồng nhất của học viên.
* Hỗ trợ tạo khung thống kê mô tả nhanh phân bố câu hỏi theo từng bài học (D01 đến D29).
* Giúp thiết kế cấu trúc JSON Schema chuẩn cho bộ Golden Set để phục vụ script kiểm thử tự động.

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case):** Ở giai đoạn đầu (trước CP2), tôi từng thử nghiệm dùng Vector Database (Embedding Cosine Similarity) để gom cụm và tính điểm số câu hỏi bối rối trên từng slide. Kết quả là điểm số và thứ hạng Top 3 slide bị trồi sụt bất thường giữa các lần chạy, có lúc Slide 18 nhảy sang Slide 17 do câu chữ của sinh viên có độ tương đồng ngữ nghĩa mơ hồ.
* **Hậu quả & Phân tích:** Giảng viên khi nhìn vào một bản đồ nhiệt mà số liệu bị thay đổi ngẫu nhiên sẽ mất hoàn toàn niềm tin vào hệ thống.
* **Bài học & Giải pháp:** **Dữ liệu thống kê dùng để ra quyết định bắt buộc phải là TẤT ĐỊNH (Deterministic)!** Nhóm đã kiên quyết loại bỏ việc dùng LLM hay Vector Search để đếm số lượng; chuyển toàn bộ logic tính nhiệt và xếp hạng sang truy vấn SQL thuần túy trên SQLite. LLM chỉ được phép nhận dữ liệu đã được tổng hợp chính xác để làm nhiệm vụ duy nhất: suy luận sư phạm. Nhờ đó, số liệu trên Heatmap đạt độ tin cậy tuyệt đối 100%.
