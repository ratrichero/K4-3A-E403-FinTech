# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Chung Văn Duy**  
*Mã học viên:* `2A0202602854`  
*Vai trò trong nhóm:* **Prompt Engineer / LLM Gateway & Benchmark**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`

---

### 1. Vai trò và trách nhiệm trong dự án
Tôi đảm nhiệm vị trí Kỹ sư Thiết kế Chỉ thị (Prompt Engineer), chịu trách nhiệm định hình "trí tuệ sư phạm" của Copilot. Nhiệm vụ cốt lõi của tôi là đảm bảo mọi câu trả lời của AI đều sắc bén, đúng phương pháp sư phạm, tuyệt đối không bịa đặt, và tuân thủ các nguyên tắc thiết kế tương tác người-máy (HAX/PAIR).

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm
* **Thiết kế Hệ thống Prompt Sư phạm (`prompts.py`):**
  - Xây dựng chỉ thị bắt buộc cấu trúc 3 phần độc lập: **[Quan sát thực chứng]** ➔ **[Giả thuyết nhận thức]** ➔ **[Cần đối chứng trên lớp]**.
  - Soạn thảo các template sinh can thiệp 2 phút: Ví dụ tương phản đời thường (Counter-analogy), Kịch bản nói đầu giờ, và Câu hỏi trắc nghiệm Concept MCQ có đáp án bẫy.
* **Hiện thực hóa HAX Guardrails:**
  - Áp dụng nguyên tắc **HAX G10 (Scope down when in doubt)**: Thiết kế Prompt xử lý câu hỏi mơ hồ (Clarification Prompt) để chủ động hỏi lại lịch sự khi câu hỏi quá ngắn gọn.
  - Áp dụng **Safe Abstention**: Chỉ thị cho mô hình thông báo yên tâm khi slide không có dữ liệu hỏi, tuyệt đối không được bịa điểm nghẽn nhận thức.
* **Cấu hình Gateway & Benchmark (`Provider/llm.py`):** Thiết lập kết nối mô hình `qwen/qwen3.8-27b` trên Groq Cloud kèm fallback tự động sang HCNSEC; trực tiếp đo lường số liệu 20 ca kiểm thử CP3.

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
* AI giúp tôi thử nghiệm nhanh hàng chục biến thể ẩn dụ đời thường (Analogies) để tìm ra ví dụ đắt giá nhất: *CoT giống như Bác sĩ ngồi suy nghĩ trong đầu; còn ReAct là Bác sĩ kê đơn xét nghiệm máu rồi nhìn kết quả mới chẩn đoán tiếp!*
* Hỗ trợ tạo các câu hỏi trắc nghiệm Concept MCQ với các phương án bẫy đánh trúng tâm lý hiểu sai của người học.
* Giúp rà soát câu chữ prompt để tối ưu số lượng token đầu vào (Context compression).

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case):** Ở phiên bản prompt đầu tiên, tôi chỉ yêu cầu chung chung: *"Hãy phân tích vì sao học viên khó hiểu ở slide này và đề xuất giải pháp"*. Khi chạy thử, LLM bắt đầu "chém gió" lý thuyết sư phạm dài dòng, đưa ra các nhận định chung chung như *"do kiến thức trừu tượng"*, và tệ nhất là **hoàn toàn không trích dẫn được bất kỳ mã Turn ID hay câu hỏi thật nào của học sinh**.
* **Hậu quả & Phân tích:** Khi đưa cho giảng viên đọc thử, thầy nhận xét ngay: *"Cái này tôi hỏi ChatGPT chung chung cũng ra được, đâu cần nhìn vào dữ liệu của lớp tôi!"*. Câu trả lời bị rớt tiêu chuẩn Factuality & Grounding.
* **Bài học & Giải pháp:** **LLM cần "rào chắn cấu trúc" (Structural Constraints) cực kỳ nghiêm ngặt!** Tôi đã viết lại toàn bộ System Prompt:
  1. Ép buộc mọi câu mở đầu phải có dẫn chứng mã Turn ID trong ngoặc vuông `[Turn T#####]`.
  2. Cung cấp dữ liệu hội thoại thô dạng danh sách bôi đen để LLM đối chiếu.
  3. Cấm tuyệt đối việc suy diễn nếu context rỗng.
  Kết quả là ở đợt đo CP3, tỷ lệ Grounding tăng vọt lên **85.0%** và **100% không bao giờ bịa Turn ID ảo**, biến Copilot thành trợ lý thực chứng đáng tin cậy.
