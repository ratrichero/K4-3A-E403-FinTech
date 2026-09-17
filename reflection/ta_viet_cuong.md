# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Tạ Việt Cường**  
*Mã học viên:* `2A0202602560`  
*Vai trò trong nhóm:* **TechLead / Full-stack Architecture**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`

---

### 1. Vai trò và trách nhiệm trong dự án
Với vai trò là TechLead của đội ngũ `K4-3A-E403-FinTech`, tôi chịu trách nhiệm cao nhất về tính đúng đắn của kiến trúc giải pháp, sự ổn định của hệ thống chạy thật (Working Prototype), và là người đại diện nộp form xuyên suốt 6 mốc Checkpoint (CP1 đến CP6).

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm
* **Thiết kế kiến trúc phân ly (Architecture Design):** Phân tách rạch ròi giữa Tầng Tất định (Deterministic Engine trong `tools.py` truy vấn SQLite 13.494 turns) và Tầng Nhận thức (Probabilistic Engine trong `agent.py`).
* **Triển khai Máy chủ Backend & API (`server.py`):** Xây dựng máy chủ HTTP đa luồng phục vụ các REST API chuẩn hóa (`/api/heatmap`, `/api/evidence`, `/api/chat`, `/api/approve`, `/api/approved`) và tích hợp máy chủ MCP JSON-RPC (`mcp_server.py`).
* **Điều phối Tác tử LangGraph StateGraph (`agent.py`):** Xây dựng StateGraph gồm 8 nút định tuyến ý định, cơ chế Fast-path cục bộ xử lý câu hỏi thường nhật và bảo mật an toàn trong 0.01s, và chuỗi suy luận sư phạm 3 phần.
* **Cơ chế Kiểm toán Bất biến (Audit Trail):** Xây dựng hàm băm SHA-256 (`hashlib.sha256`) gắn với mỗi can thiệp được giảng viên duyệt và lưu trữ thực tế vào bảng `curriculum_adaptations` trong SQLite.
* **Khóa cứng tài liệu đặc tả:** Chủ trì biên soạn và khóa cứng tệp `spec.md` chuẩn 8 phần tại mốc CP4.

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
AI đã đóng vai trò như một kỹ sư lập trình cặp (Pair-programmer) đắc lực:
* Giúp tôi thiết kế nhanh các cấu trúc Type Dict và StateGraph Schema trong LangGraph mà không gặp lỗi typing.
* Hỗ trợ tối ưu hóa các câu lệnh SQL truy vấn ma trận nhiệt trên 13.494 dòng dữ liệu, giảm thời gian phản hồi từ 120ms xuống dưới 8ms.
* Giúp rà soát toàn diện các kịch bản biên (Edge cases) theo nguyên tắc HAX Toolkit của Microsoft (G10 - Scope down, G11 - Explain why).

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case):** Trong lượt chạy kiểm thử 20 ca tự động tại mốc CP3, có 4 ca phân tích sư phạm bị timeout 25 giây do chạm trần giới hạn Token Per Minute (TPM) của nhà cung cấp API Groq Cloud khi gửi 20 request HTTP liên tục.
* **Hậu quả & Phân tích:** Lúc đầu nhóm khá bối rối vì khi chạy đơn lẻ từng câu trong IDE thì kết quả rất tốt, nhưng khi chạy dồn dập dạng benchmark thì cloud API bị nghẽn cổ chai.
* **Bài học & Giải pháp:** Không bao giờ phụ thuộc vào một nhà cung cấp LLM duy nhất trong các hệ thống đòi hỏi tính sẵn sàng cao. Tôi đã rút ra bài học lớn về việc thiết kế **Gateway Fallback đa tầng** (`with_fallbacks` chuyển sang HCNSEC/OpenAI) và nguyên lý **Fast-path cục bộ**: Những gì giải quyết được bằng logic tất định (như câu hỏi giờ, phép tính, hoặc chặn từ khóa vi phạm an toàn) phải xử lý ngay tại Gateway mà không được phép đẩy qua LLM. Điều này vừa tiết kiệm chi phí token, vừa giảm độ trễ về mức 0.01 giây.
