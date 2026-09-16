# 📋 SỔ TAY QUẢN LÝ TIẾN ĐỘ 6 CHECKPOINT (CP1 — CP6)
## VLearn Class Confusion Copilot — Hackathon Day 05-06
**Phòng:** E403 · **Ca:** 3A (16/9 — 18/9/2026) · **Cụm thi:** Cụm 1  
**Đội ngũ:** `K4-3A-E403-FinTech` · **Track:** Track A (Đề A2 · Class Confusion Heatmap & Pedagogical Copilot)  
**Kho mã nguồn GitHub:** [https://github.com/ratrichero/K4-3A-E403-FinTech](https://github.com/ratrichero/K4-3A-E403-FinTech)

---

## I. THÔNG TIN ĐỊNH DANH NHÓM & NỘP FORM

> ⚠️ **QUY TẮC SỐNG CÒN:**  
> 1. **Cả 5 mốc form phải nộp bằng DUY NHẤT một mã học viên của Đội trưởng (Tạ Việt Cường - `2A0202602560`).** BTC ghép 5 phiếu dựa trên mã này; đổi mã sẽ bị coi là 2 nhóm khác nhau và mất điểm.  
> 2. **Không commit thư mục `data/`** lên GitHub công khai (đã đưa vào `.gitignore`).  
> 3. Nộp đúng hạn = 5 điểm/mốc; nộp muộn = 0 điểm mốc đó (tổng 25 điểm nộp).

| Thông tin | Chi tiết |
|---|---|
| **Đội trưởng (TechLead)** | **Tạ Việt Cường** — Mã HV: `2A0202602560` (Người duy nhất nộp form) |
| **Thành viên 2** | **Dương Đạt Khang** (Data Scientist / Mining & Analytics) |
| **Thành viên 3** | **Chung Văn Duy** (Prompt Engineer / Pedagogical Copilot) |
| **Thành viên 4** | **Nguyễn Thị Chinh** (Product Manager / UX & Validation) |
| **Willing User 1 (Đã khai CP1)** | **Thầy Hoàng Minh Đức** — TA Lead phụ trách môn Agentic AI K4 |
| **Willing User 2 (Đã khai CP1)** | **Bạn Lê Tuấn Nghĩa** — Học viên K4 (Phòng E403, Cluster 2) |
| **Link Repo GitHub công khai** | `https://github.com/ratrichero/K4-3A-E403-FinTech` |
| **Tệp Demo tương tác** | [`present.html`](file:///d:/VinUniAI/Lab05/present.html) |
| **Tài liệu Product Discovery** | [`ProductDiscovery.md`](file:///d:/VinUniAI/Lab05/ProductDiscovery.md) |

---

## II. BẢNG TIẾN ĐỘ TỔNG QUAN 6 CHECKPOINT (CA 3A · 47,5 GIỜ)

| Mốc | Thời hạn | Điểm | Yêu cầu trọng tâm | Trạng thái nhóm | Tệp bằng chứng |
|:---:|:---:|:---:|---|:---:|---|
| **CP1** | **19:30 · 16/9** | 5 đ | Canvas 4 ô + Đội trưởng + Repo GitHub + 2 Willing Users | ✅ **ĐÃ XONG** | `ProductDiscovery.md` (Mục I), `README.md` |
| **CP2** | **21:00 · 16/9** | 5 đ | Luồng hoạt động bấm được (Clickable Mock) / Sơ đồ luồng | ✅ **ĐÃ XONG** | `present.html` (Heatmap + Floating Resizable Copilot) |
| **CP3** | **16:00 · 17/9** | 5 đ | Video thao tác 30s + Số đo đánh giá (Golden Set 20 test cases) | 🔄 **ĐANG LÀM** | `scripts/eval_golden_set.py` + `demo_30s.mp4` |
| **CP4** | **21:00 · 17/9** | 5 đ | Chốt `spec.md` (Khóa chuẩn "đạt" + Khai báo backlog chưa xong) | ⏳ **ĐÃ SOẠN SẴN** | `spec.md` |
| **CP5** | **13:00 · 18/9** | 5 đ | Slide PDF (6 trang) + Video demo dự phòng pitch + Đánh giá R6 | ⏳ **KẾ HOẠCH** | `slides_pitch.pdf` + `backup_demo.mp4` |
| **CP6** | **17:30 · 18/9** | 67 đ | Thuyết trình 6 phút tại Phòng E403 + Trả lời chất vấn Q&A | ⏳ **KẾ HOẠCH** | Sân khấu E403 Cụm 1 |

---

## III. NỘI DUNG CHI TIẾT & BẢN NỘP TỪNG CHECKPOINT

### 🟢 CHECKPOINT 1 (Hạn: 19:30 · 16/9) — CHỐT CANVAS + REPO
* **Mục tiêu:** Định hình chân dung người dùng, vấn đề cốt lõi và phạm vi lát cắt giải pháp trước khi viết mã.
* **Thông tin điền Form nộp:**
  * **Họ tên & Mã HV Đội trưởng:** Tạ Việt Cường — `2A0202602560`
  * **Link GitHub Repo:** `https://github.com/ratrichero/K4-3A-E403-FinTech`
  * **Khai báo 2 Willing Users:**
    1. Thầy Hoàng Minh Đức (TA Lead VLearn) — Email: `duc.hm@vlearn.edu.vn`
    2. Bạn Lê Tuấn Nghĩa (Học viên K4) — Mã HV: `2A0202602112`
  * **Nội dung Canvas 4 ô:**
    1. **Pain Point:** Giảng viên/TA mù mờ về điểm nghẽn kiến thức bài giảng (13.494 lượt hỏi nhưng `understanding_level` bị bỏ trống 99.85%; 89.8% bot chỉ nhắc lý thuyết vẹt, không tổng hợp cho GV).
    2. **Bằng chứng từ dữ liệu:** Slide 18 bài D02 có 92 lượt hỏi dồn dập (chiếm 38.6% buổi học), học viên nhầm lẫn nghiêm trọng giữa CoT và ReAct (Turn ID `T00891`).
    3. **Problem & Impact:** Giảng viên tốn 3-4 giờ đọc chatlog thủ công hoặc vào lớp dạy lướt qua điểm nghẽn, dẫn đến 65% học viên kẹt bài tập Lab 2.
    4. **Lát cắt giải pháp (Thin Slice):** Class Confusion Heatmap tự động gắn thẻ điểm nóng theo từng trang Slide + Trợ lý AI Copilot đề xuất can thiệp sư phạm 2 phút (ví dụ tương phản, quiz đầu giờ).

---

### 🟢 CHECKPOINT 2 (Hạn: 21:00 · 16/9) — CHO THẤY LUỒNG HOẠT ĐỘNG
* **Mục tiêu:** Nguyên mẫu bấm thử được (Interactive Clickable Prototype) thể hiện luồng làm việc khép kín của Giảng viên.
* **Nội dung đã hoàn thành:**
  * File giao diện: [`present.html`](file:///d:/VinUniAI/Lab05/present.html) đã được đẩy lên GitHub `main`.
  * **Luồng 5 bước đã tích hợp:**
    1. **Bước 1 — Chọn phạm vi dữ liệu:** Dropdown chọn Khóa (K4 Live / K3 Lịch sử) và Bài giảng (D02 Agent Architectures).
    2. **Bước 2 — Quét Confusion Heatmap:** Banner cảnh báo Top 3 trang slide nghẽn nhất (#1 Slide 18: 92 câu; #2 Slide 12: 67 câu; #3 Slide 6: 54 câu).
    3. **Bước 3 — Kiểm chứng bằng chứng gốc:** Bảng Evidence Inspector trích xuất nguyên văn Turn ID (`T00891`, `T01042`, `T01155`) từ `tutor_turns.csv`.
    4. **Bước 4 — AI sinh phương án can thiệp:** 3 nút sinh tức thì: Ví dụ tương phản đời thường (Tra cứu thời tiết), Câu hỏi Quiz 4 lựa chọn, hoặc Đoạn nhắc lại 1 slide.
    5. **Bước 5 — Phê duyệt & Áp dụng:** Nút *"Phê duyệt can thiệp"* lưu vào giáo án và kích hoạt thông báo xác nhận Toast.
  * **Tính năng Floating Desktop Widget độc đáo:**
    * Cửa sổ AI Copilot nổi ở góc phải dưới, hiển thị mặc định.
    * Đầy đủ nút chỉnh 3 kích cỡ (`Nhỏ 380p`, `Vừa 520p`, `Lớn 760p`, `Phóng to toàn màn hình`).
    * Có tay cầm kéo góc `⤡` để co giãn kích thước tự do theo chuột.
    * Thanh tiêu đề nắm kéo (draggable) di chuyển vị trí bất kỳ đâu trên màn hình, nút `📌` gắn lại góc.
* **Link nộp Form:** Nộp link dẫn tới GitHub Repo chứa file `present.html` (kèm hướng dẫn mở trực tiếp bằng trình duyệt).

---

### 🟡 CHECKPOINT 3 (Hạn: 16:00 · 17/9) — VIDEO THAO TÁC 30S + SỐ ĐO ĐÁNH GIÁ
* **Mục tiêu:** Chứng minh sản phẩm có backend AI chạy thật trên dữ liệu thật và có số đo định lượng rõ ràng (Golden Set).
* **Nhiệm vụ cần thực hiện trong sáng 17/9:**
  1. **Xây dựng bộ Golden Test Set (20 test cases):**
     * Chọn 20 lượt hỏi đại diện từ `tutor_turns.csv` (10 câu tại Slide 18 CoT/ReAct, 5 câu tại Slide 12 Loop, 5 câu tại Slide 6 Memory).
     * Gán nhãn thủ công (Ground Truth) mức độ hiểu và lỗ hổng khái niệm.
  2. **Chạy Pipeline phân tích AI thật (Python Backend):**
     * Script `scripts/eval_golden_set.py` đọc 20 dòng này, gọi LLM phân loại lỗ hổng và đề xuất can thiệp.
     * Tính toán số đo:
       * **Độ chính xác phát hiện lỗ hổng (Confusion Detection Accuracy):** Mục tiêu ≥ 85% (17/20 câu).
       * **Tỷ lệ trích dẫn đúng Turn ID gốc (Grounding Rate):** 100% (không bịa Turn ID).
       * **Thời gian phản hồi trung bình (Latency):** < 2.5s.
  3. **Quay Video thao tác màn hình 30 giây (`demo_30s.mp4`):**
     * Thao tác thật: Mở trang, click Slide 18 trên Heatmap ➔ Bấm hỏi Copilot ➔ Copilot phản hồi kèm dẫn chứng Turn ID thật trong 30s.
     * Tải lên Google Drive (mở quyền "Bất kỳ ai có liên kết") hoặc đính kèm vào link nộp form.

---

### ⚪ CHECKPOINT 4 (Hạn: 21:00 · 17/9) — CHỐT `spec.md` & KHÓA CHUẨN ĐẠT
* **Mục tiêu:** Khóa định nghĩa "Thế nào là sản phẩm đạt chất lượng" trước khi hoàn thiện mã, tự khai phần chưa xong.
* **Nội dung cam kết trong `spec.md`:**
  * **Chuẩn Đạt (Success Criteria):**
    * Accuracy phát hiện hiểu sai khái niệm: ≥ 85% trên tập kiểm thử 20 ca.
    * Trích dẫn nguồn: 100% can thiệp phải liên kết được ít nhất 1 Turn ID thật trong chatlog.
    * Thời gian xử lý: Sinh gợi ý can thiệp sư phạm trong ≤ 3 giây.
  * **Tự khai phần chưa làm xong (Backlog declaration):**
    * Chưa tích hợp đẩy trực tiếp slide vào hệ thống slide VLearn PPTX (mới xuất markdown/quiz text).
    * Chưa kết nối WebSocket thời gian thực khi học viên đang chat dồn dập (mới xử lý theo lô sau buổi học).

---

### ⚪ CHECKPOINT 5 (Hạn: 13:00 · 18/9) — SLIDE PDF + VIDEO DEMO DỰ PHÒNG PITCH
* **Mục tiêu:** Bộ tài liệu hoàn chỉnh sẵn sàng cho buổi pitch, bảo đảm không bị gián đoạn kể cả khi mất mạng.
* **Sản phẩm nộp:**
  1. **Tệp Slide 6 trang xuất định dạng PDF (`slides_pitch.pdf`):**
     * Slide 1: Bối cảnh & Điểm đau (Giảng viên mù thông tin điểm nghẽn bài giảng).
     * Slide 2: Khám phá dữ liệu (Bằng chứng 92 lượt hỏi tại Slide 18 từ `tutor_turns.csv`).
     * Slide 3: Giải pháp Class Confusion Heatmap & Copilot sư phạm.
     * Slide 4: Kiến trúc kỹ thuật (Pipeline lọc tín hiệu, RAG truy xuất Turn ID, Failure handling).
     * Slide 5: Kết quả thực nghiệm (Đo lường 20 ca test, phản hồi từ 2 Willing Users - Khối R6).
     * Slide 6: Phân công nhóm & Kế hoạch phát triển tiếp theo.
  2. **Video demo dự phòng (`backup_demo.mp4`):** Quay trọn vẹn kịch bản demo 2 phút để ban giám khảo chiếu nếu phòng thi gặp sự cố wifi.
  3. **Biên bản đánh giá người dùng (Khối R6):** Phản hồi thực tế từ Thầy Hoàng Minh Đức và bạn Lê Tuấn Nghĩa sau khi trải nghiệm bản demo.

---

### ⚪ CHECKPOINT 6 (17:30 · 18/9) — THUYẾT TRÌNH TẠI PHÒNG E403
* **Hình thức:** Pitch 6 phút tại Cụm 1 Phòng E403.
* **Phân bổ thời gian (6 phút):**
  * `0:00 - 1:30`: Trình bày Vấn đề & Dữ liệu mỏ neo (Tạ Việt Cường & Nguyễn Thị Chinh).
  * `1:30 - 3:30`: Live Demo trên `present.html` (Tạ Việt Cường).
  * `3:30 - 4:30`: Kiến trúc RAG, Golden Set và khối R6 (Dương Đạt Khang & Chung Văn Duy).
  * `4:30 - 6:00`: Trả lời câu hỏi chất vấn từ Giám khảo (Mọi thành viên đều nắm vững code & prompt theo quy tắc vibe-coding).

---

## IV. BẢNG CHECKLIST KIỂM TRA TRƯỚC MỖI LẦN GỬI FORM

- [ ] Đã kiểm tra người nộp form đúng là **Tạ Việt Cường** (Mã: `2A0202602560`) chưa?
- [ ] Link GitHub đã công khai (Public) và truy cập được ở chế độ ẩn danh (Incognito)?
- [ ] Đã kiểm tra không có file dữ liệu bí mật nào trong `data/` bị đẩy lên GitHub?
- [ ] Các tệp đính kèm (Video/Slide) đã bật quyền truy cập *"Bất kỳ ai có đường liên kết đều xem được"*?
- [ ] Đã nộp trước thời hạn ít nhất 15 phút để tránh nghẽn mạng?
