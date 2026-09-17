# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Nguyễn Thị Chinh**  
*Mã học viên:* `2A0202602876`  
*Vai trò trong nhóm:* **Product Manager / UX & User Validation**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`

---

### 1. Vai trò và trách nhiệm trong dự án
Tôi đảm nhiệm vai trò Quản lý Sản phẩm (Product Manager) kiêm Thiết kế Trải nghiệm (UX), giữ vai trò là "tiếng nói của người dùng" trong đội ngũ. Trọng tâm của tôi là đảm bảo sản phẩm giải quyết đúng nỗi đau có thật, giữ vững ranh giới đạo đức sư phạm, và thiết kế luồng thao tác mượt mà giúp giảng viên đưa ra quyết định nhanh nhất.

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm
* **Xác định Vấn đề & JTBD:** Soạn thảo Core JTBD không chứa chữ AI, phân tích bối cảnh thất bại của các giải pháp hiện tại (đọc lướt chatlog, thiên lệch kẻ phát biểu, bài quiz trễ).
* **Phân tích Chiến lược & Ma trận Đánh giá (Impact Matrix):** Xây dựng bảng so sánh 3 ứng viên giải pháp, bảo vệ quyết định loại bỏ AI chấm điểm tự động và Chatbot viết lại slide dựa trên phân tích Chi Phí Sai Sót (Cost-of-Error).
* **Thiết kế Trải nghiệm Người dùng (Web Cockpit UX):** Xây dựng luồng thao tác 5 bước từ lúc chọn bài đến khi duyệt giáo án; thiết kế bố cục 2 cột (Dual-pane Cockpit) giúp giảng viên vừa xem bản đồ nhiệt vừa đối chiếu bằng chứng gốc.
* **Chủ trì Vòng Kiểm chứng Người dùng (Khối R6):** Trực tiếp thiết kế kịch bản 5 nhịp chuẩn Stanford CS177, phỏng vấn Thầy Hoàng Minh Đức và bạn Lê Tuấn Nghĩa, ghi nhận trích dẫn và đo lường chỉ số Sean Ellis Disappointment Rate.
* **Biên soạn Slide Thuyết trình:** Thiết kế cấu trúc 6 trang slide theo đúng quy tắc *"Không có bằng chứng thì không có slide"* và phân vai kịch bản pitch 6 phút cho 4 thành viên.

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
* AI hỗ trợ tôi đóng vai (Role-play) các đối tượng người dùng khác nhau (Giảng viên khó tính, Sinh viên yếu thế) để phản biện tính khả thi của giải pháp trước khi đem phỏng vấn người thật.
* Giúp rà soát toàn bộ văn bản trong `spec.md` để loại bỏ các từ ngữ buzzword sáo rỗng, chuyển hóa thành các câu lệnh kiểm chứng được.
* Gợi ý cấu trúc phân bổ thời gian hợp lý cho bài thuyết trình 6 phút trên sân khấu.

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case):** Khi mới bắt đầu dự án tại CP1, cả nhóm từng hào hứng với ý tưởng: *"Cho AI tự động sửa lại file slide PDF của trường và gửi email cảnh báo tự động cho sinh viên"*. Chúng tôi nghĩ rằng tự động hóa càng nhiều thì sản phẩm càng "ngầu" và công nghệ càng cao.
* **Hậu quả & Phân tích:** Khi đem ý tưởng này đi hỏi nhanh Thầy Đức (TA Lead), Thầy gạt đi ngay: *"Slide là giáo trình chính thống của học viện, không một giảng viên nào cho phép một con bot tự ý sửa chữ trên slide của mình. Còn nếu bot tự gửi email cho sinh viên mà sai kiến thức thì ai chịu trách nhiệm?"*. Ý tưởng suýt nữa đẩy nhóm vào vết xe đổ của sự ảo tưởng tự động hóa (Automation Complacency).
* **Bài học & Giải pháp:** **Trong giáo dục đại học, sai sót kiến thức là cực kỳ đắt đỏ!** Tôi đã lập tức điều chỉnh định hướng sản phẩm từ *Automate* sang **Augment (Human-in-the-loop)**:
  - Thiết lập Non-goal #1: AI tuyệt đối không tự sửa file gốc.
  - Thiết lập Non-goal #2: AI không chấm điểm phán xét học viên.
  - Thiết kế nút bấm *"Phê duyệt & Đưa vào giáo án"*: AI chỉ giữ vai trò chuyên viên nghiên cứu dữ liệu soạn thảo bản nháp (Draft); Giảng viên luôn là người làm chủ cuối cùng.
  Chính sự chuyển hướng này đã giúp giải pháp của nhóm nhận được sự đồng thuận và khen ngợi tuyệt đối từ cả Giảng viên và Sinh viên trong đợt thử nghiệm R6.
