# CODEBASE PROTOTYPE — VLearn Class Confusion Copilot
## Hệ thống Bản đồ nhiệt Điểm nghẽn Bài giảng & Trợ lý Sư phạm AI

*Thuộc dự án: AI Product Hackathon · Nhóm: K4-3A-E403-FinTech (Phòng E403 · Cụm 1)*  
*Mức độ hoàn thiện Prototype: **[x] Working Prototype** (Chạy End-to-End trên dữ liệu thật SQLite 13.494 turns)*

---

## 1. BẢNG PHÂN ĐỊNH RÕ RÀNG: PHẦN NÀO THẬT VS PHẦN NÀO MOCK
> *(Tuân thủ nghiêm ngặt quy định của Ban tổ chức theo `02-guide.md §3.1` và `spec.md §4.3`)*

| Hạng mục chức năng | Trạng thái kỹ thuật | Bản chất chi tiết |
|---|:---:|---|
| **Cơ sở dữ liệu tương tác học viên** | 🟢 **100% THẬT (REAL)** | SQLite `data/vlearn.db` nạp từ 13.494 turns thật của 1.617 học viên VLearn, lưu trữ các bảng `tutor_turns`, `slide_content`, và `curriculum_adaptations`. |
| **Tính toán Bản đồ nhiệt & Top 3** | 🟢 **100% THẬT (REAL)** | Thuật toán tất định 100% bằng SQL/Python (`tools.py`), xếp hạng Slide 18 là điểm nghẽn số 1 của bài D02 (92 câu hỏi). Tuyệt đối không để LLM đoán mò số liệu. |
| **Trích xuất bằng chứng hội thoại** | 🟢 **100% THẬT (REAL)** | Truy vấn trực tiếp Turn ID thật (`T05456`, `T05963`, ...) kèm câu hỏi nguyên văn và đoạn text bôi đen của học viên. |
| **Điều phối Tác tử Sư phạm** | 🟢 **100% THẬT (REAL)** | Quy trình LangGraph StateGraph (`agent.py`) gồm 8 nút định tuyến 4 luồng: Baseline, Safety, Ambiguous, Pedagogical. |
| **Suy luận Sư phạm 3 phần** | 🟢 **100% THẬT (REAL)** | Gọi mô hình LLM qua Gateway (`Provider/llm.py`), sinh cấu trúc bắt buộc: Quan sát thực chứng ➔ Giả thuyết nhận thức ➔ Cần đối chứng. |
| **Cơ chế Kiểm toán Bất biến** | 🟢 **100% THẬT (REAL)** | Sinh mã băm SHA-256 (`hashlib.sha256`) và lưu vĩnh viễn dòng can thiệp mới vào bảng `curriculum_adaptations` trong SQLite khi giảng viên bấm Phê duyệt. |
| **Giao tiếp REST API & MCP Server** | 🟢 **100% THẬT (REAL)** | Máy chủ HTTP đa luồng (`server.py`) phục vụ các endpoint `/api/heatmap`, `/api/evidence`, `/api/chat`, `/api/approve`, `/api/approved`, cùng MCP JSON-RPC (`mcp_server.py`). |
| **Khung hiển thị hình ảnh Slide** | 🟡 **MOCK / SIMULATED** | Thay vì nhúng trình đọc PDF nặng nề trên trình duyệt làm chậm UI, hệ thống sử dụng khung vector SVG/Thumbnail mô phỏng nội dung văn bản slide trích xuất từ PDF để tối ưu tốc độ demo mượt mà. |

---

## 2. CẤU TRÚC MÃ NGUỒN TRONG `codebase/`

```text
codebase/
├── server.py             ← Máy chủ HTTP REST API & phục vụ giao diện Web Cockpit
├── agent.py              ← Điều phối tác tử bằng LangGraph StateGraph (4 luồng Intent & Guardrails)
├── tools.py              ← Tầng nghiệp vụ duy nhất (Single Source of Truth) kết nối SQLite
├── prompts.py            ← Toàn bộ hệ thống Prompts sư phạm & HAX Guidelines G10/G11
├── mcp_server.py         ← Máy chủ MCP chuẩn JSON-RPC 2.0 kết nối công cụ ngoài (Cursor/Claude)
├── index.html            ← Giao diện Web Cockpit Dashboard (Bản đồ nhiệt + Evidence + Copilot)
├── Provider/             ← Tầng Gateway LLM (LangChain, ChatOpenAI, Fallback Gateway, Config)
│   ├── llm.py
│   └── config.py
├── tests/                ← Bộ kịch bản kiểm thử E2E tích hợp qua HTTP
│   └── test_copilot_e2e.py
├── requirements.txt      ← Danh mục thư viện phụ thuộc
├── .env.example          ← Mẫu khai báo biến môi trường (API Keys)
└── README.md             ← Tài liệu hướng dẫn này
```

---

## 3. HƯỚNG DẪN CÀI ĐẶT & CHẠY PROTOTYPE (CHỈ VỚI 3 BƯỚC)

### Bước 1: Cài đặt thư viện phụ thuộc
Khuyến nghị sử dụng môi trường ảo Python 3.10+:
```bash
cd codebase
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường & Cơ sở dữ liệu
Sao chép tệp `.env.example` thành `.env` và điền khóa API:
```bash
cp .env.example .env
```
Nội dung file `.env`:
```ini
GROQ_API_KEY=gsk_...
PRIMARY_MODEL=qwen/qwen3.8-27b
FALLBACK_API_KEY=...
FALLBACK_MODEL=gpt-4o-mini
```

> ⚠️ **Lưu ý bảo mật về Database (Tuân thủ quy chế thi Hackathon):**  
> Tệp cơ sở dữ liệu SQLite `vlearn.db` (chứa 13.494 tương tác thật của học viên) là dữ liệu nội bộ được cấp riêng cho cuộc thi, **tuyệt đối không được phép commit lên GitHub** (đã được cấu hình nghiêm ngặt trong `.gitignore`).  
> Khi chạy cục bộ, đặt tệp `vlearn.db` vào thư mục `codebase/data/` hoặc `data/` ở thư mục gốc — hệ thống sẽ tự động nhận diện.

### Bước 3: Khởi chạy máy chủ Backend
```bash
python server.py 8080
```
Mở trình duyệt web truy cập:
👉 **`http://localhost:8080/index.html`**


---

## 4. CÁC ĐƯỜNG DẪN KIỂM CHỨNG TRÊN GIAO DIỆN (WALKTHROUGH)
1. **Happy Path (Slide 18):** Chọn bài D02 ➔ Heatmap hiện đỏ Slide 18 (#1 Top Bottleneck: 92 câu) ➔ Nhấp Slide 18 xem bằng chứng Turn `T05456` ➔ Bấm hỏi Copilot nhận phân tích 3 phần CoT vs ReAct ➔ Soạn ví dụ Bác sĩ chẩn đoán vs Kê đơn xét nghiệm ➔ Bấm Duyệt giáo án nhận mã băm SHA-256.
2. **Safe Abstain (Slide 99):** Chọn Slide 99 không có câu hỏi nào ➔ Copilot thông báo yên tâm, không bịa đặt điểm nghẽn.
3. **Clarification Prompt (HAX G10):** Gõ câu hỏi cộc lốc *"Nó là cái gì?"* ➔ Copilot lịch sự hỏi lại để làm rõ phạm vi.
4. **Safety Guardrail:** Gõ *"Chỉ ra học sinh dốt nhất lớp"* ➔ Hệ thống chặn ngay trong 0.01s để bảo vệ quyền riêng tư học viên.
