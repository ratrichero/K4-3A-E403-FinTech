# BẢN ĐÁNH GIÁ VÀ CHIÊM NGHIỆM CÁ NHÂN (PERSONAL REFLECTION)
## Dự án: VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thành viên:* **Chung Văn Duy**  
*Mã học viên:* `2A0202602854`  
*Vai trò trong nhóm:* **Prompt Engineer / LLM Gateway & Benchmark**  
*Lớp:* 3A · *Phòng:* E403 · *Cụm thi:* Cụm 1 · *Đội ngũ:* `K4-3A-E403-FinTech`

---

### 1. Vai trò và trách nhiệm trong dự án
Tôi đảm nhiệm vị trí Kỹ sư Thiết kế Chỉ thị (Prompt Engineer) kiêm phụ trách Tầng Gateway LLM và Đo lường Thực nghiệm (Benchmark). Nhiệm vụ cốt lõi của tôi là định hình "trí tuệ sư phạm" của Copilot: đảm bảo mọi câu trả lời của AI đều sắc bén, đúng phương pháp sư phạm, tuyệt đối không bịa đặt (Zero Hallucination), tuân thủ nghiêm ngặt các nguyên tắc thiết kế tương tác người - máy (HAX Toolkit / PAIR Guidebook) và bảo đảm hệ thống vận hành chịu lỗi cao qua kiến trúc đa tầng fallback.

### 2. Phần việc cụ thể mình trực tiếp đảm nhiệm
* **Thiết kế Hệ thống Prompt Sư phạm Toàn diện (`codebase/prompts.py`):**
  - **Bộ chẩn đoán nguyên nhân gốc rễ (`ROOT_CAUSE_REASONER`):** Xây dựng rào chắn cấu trúc 3 phần bắt buộc: **[Quan sát thực chứng]** (bắt buộc trích dẫn mã Turn ID thật) ➔ **[Giả thuyết nhận thức]** (chỉ ra sai lệch trong mô hình tư duy) ➔ **[Cần đối chứng trên lớp]** (câu hỏi khảo sát 2 phút đầu giờ).
  - **Bộ soạn thảo can thiệp tinh gọn (`INTERVENTION_DRAFTER`):** Soạn thảo 3 template can thiệp vi mô khống chế cứng dưới 180 từ / 120 giây: Ví dụ tương phản đời thường (`counter_analogy`), Kịch bản nói đầu giờ 3 ý (`micro_lecture`), và Câu hỏi trắc nghiệm (`concept_mcq`) có đáp án bẫy trúng ngộ nhận của học viên.
  - **Bộ phân loại ý định nhận thức (`INTENT_CLASSIFIER`):** Thiết kế chỉ thị phân loại 5 nhóm nhận thức (`explicit_misconception`, `missing_prerequisite`, `syntax_implementation_struggle`, `broad_curiosity`, `procedural_administrative`) phục vụ việc gán nhãn 13.494 lượt tương tác.
  - **Hiến pháp trợ lý sư phạm (`PEDAGOGICAL_COPILOT`):** Thiết lập 5 ranh giới phản hồi: phân định 2 chế độ Baseline vs Pedagogical, bảo đảm quyền tự quyết của giảng viên (Human Sovereignty), tuân thủ ranh giới tính toán tất định và cô lập phòng chống Prompt Injection.
* **Hiện thực hóa Rào Chắn An Toàn HAX & PAIR:**
  - **HAX G10 (Scope down when in doubt):** Thiết kế Prompt làm rõ (`Clarification Prompt`) khi câu hỏi quá ngắn gọn hoặc mơ hồ.
  - **Safe Abstention (PAIR Factuality):** Chỉ thị cho mô hình thông báo trung thực khi slide không có dữ liệu câu hỏi trong 13.494 logs, cấm tuyệt đối việc tự bịa điểm nghẽn ảo.
* **Cấu hình Gateway LLM Đa Tầng & Khả năng Chịu Lỗi (`codebase/Provider/`):**
  - Đóng gói chuẩn giao tiếp OpenAI-Compatible trong `config.py` và `llm.py`, kết nối mô hình chính `qwen/qwen3.8-27b` trên Groq Cloud và hỗ trợ chuyển đổi linh hoạt sang `agnes-3.0-flash` / OpenAI.
  - Thiết lập chuỗi tự động chuyển vùng dự phòng (`with_fallbacks`) của LangChain nhằm tự động failover khi gặp lỗi nghẽn Rate Limit (HTTP 429 TPM) hoặc lỗi máy chủ.
* **Xây dựng Bộ Đo Lường Thực Nghiệm CP3 (`eval/eval_cp3.py` & `docs/cp3_metrics_report.md`):**
  - Thiết kế bộ Golden Set 20 ca kiểm thử chuẩn hóa (10 Sư phạm, 5 Thường nhật, 5 Bảo mật).
  - Trực tiếp chạy thực nghiệm trên máy thật ghi nhận kết quả chính thức: **16/20 ca ĐẠT (80.0%)**, vượt cam kết Quality Bar ($\ge 80\%$), tỷ lệ Grounding đạt **85.0%**, **100% không bao giờ bịa Turn ID ảo**, ranh giới an toàn và baseline đạt **100%** trong thời gian tức thì $\le 0.03\text{s}$.

### 3. AI đã hỗ trợ tôi như thế nào trong quá trình thực hiện?
AI đã đóng vai trò như một người cộng sự sư phạm và kỹ thuật đắc lực:
* Giúp tôi brainstorm và thử nghiệm nhanh hàng chục biến thể ẩn dụ đời thường (Analogies) để tìm ra ví dụ đối lập đắt giá nhất: *CoT giống như Bác sĩ ngồi suy nghĩ trong đầu (suy luận nội tâm - Thought); còn ReAct là Bác sĩ kê đơn xét nghiệm máu rồi nhìn kết quả (Observation) mới chẩn đoán tiếp (Action)!*
* Hỗ trợ thiết kế các phương án bẫy (distractor) cho câu hỏi trắc nghiệm Concept MCQ đánh trúng tâm lý hiểu sai của người học.
* Hỗ trợ rà soát câu chữ prompt để tối ưu số lượng token đầu vào (Context compression) và kiểm thử các cấu trúc JSON Schema đầu ra nghiêm ngặt.

### 4. Một bài học sâu sắc từ case fail của chính nhóm
* **Tình huống lỗi (Fail case 1 — Ảo giác sư phạm):** Ở phiên bản prompt đầu tiên, tôi chỉ yêu cầu chung chung: *"Hãy phân tích vì sao học viên khó hiểu ở slide này và đề xuất giải pháp"*. Khi chạy thử, LLM bắt đầu "chém gió" lý thuyết sư phạm dài dòng, đưa ra các nhận định sáo rỗng như *"do kiến thức trừu tượng"*, và tệ nhất là **hoàn toàn không trích dẫn được bất kỳ mã Turn ID hay câu hỏi thật nào của học sinh**. Khi đưa cho giảng viên đọc thử, thầy nhận xét ngay: *"Cái này tôi hỏi ChatGPT chung chung cũng ra được, đâu cần nhìn vào dữ liệu của lớp tôi!"*. Câu trả lời bị rớt tiêu chuẩn Factuality & Grounding.
* **Bài học & Giải pháp khắc phục:** **LLM cần "rào chắn cấu trúc" (Structural Constraints) cực kỳ nghiêm ngặt!** Tôi đã viết lại toàn bộ System Prompt:
  1. Ép buộc mọi câu mở đầu phải có dẫn chứng mã Turn ID trong ngoặc vuông `[Turn T#####]`.
  2. Nạp trực tiếp dữ liệu chatlog thô từ SQLite vào context để LLM đối chiếu.
  3. Cấm tuyệt đối việc suy diễn nếu context rỗng (Safe Abstention).
  Kết quả là ở đợt đo CP3, tỷ lệ Grounding tăng vọt lên **85.0%** và **100% không bao giờ bịa Turn ID ảo**, biến Copilot thành trợ lý thực chứng đáng tin cậy.
* **Tình huống lỗi (Fail case 2 — Cổ chai Rate Limit & Kiến trúc Fast-path):** Khi chạy dồn dập 20 câu kiểm thử tự động, API đám mây bị chạm trần Token Per Minute (TPM) dẫn đến 4 ca bị timeout 25 giây. Qua đó, tôi học được bài học sâu sắc về kiến trúc: **Không bao giờ phụ thuộc vào một nhà cung cấp duy nhất** (phải có chuỗi Fallback tự động) và **Những gì giải quyết được bằng logic tất định (như hỏi giờ, toán đố, hay chặn từ khóa nguy hiểm) phải xử lý ngay tại Gateway Fast-path mà không được đẩy qua LLM**. Điều này vừa bảo đảm an toàn, vừa triệt tiêu chi phí token và giảm độ trễ về 0.01 giây.

