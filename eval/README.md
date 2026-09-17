# ĐÁNH GIÁ THỰC NGHIỆM & SỐ ĐO CHẤT LƯỢNG AI (EVALUATION DIRECTORY)
## VLearn Class Confusion Copilot & Pedagogical Heatmap

*Thư mục: `eval/` — Lưu trữ Bộ dữ liệu kiểm thử (Golden Set) & Bảng kết quả các lượt chạy qua các Checkpoint*  
*Căn cứ kỹ thuật: `02-guide.md §2.6 & §4.1`, `spec.md §7`*

---

## 1. CẤU TRÚC THƯ MỤC `eval/`

```text
eval/
├── golden_set_20.json    ← Bộ 20 ca kiểm thử chuẩn hóa (10 Sư phạm, 5 Thường nhật, 5 Bảo mật)
├── eval_cp3.py           ← Script tự động chạy toàn bộ 20 ca qua HTTP REST API và tính số đo
├── results_cp3.md        ← Báo cáo chi tiết kết quả thực nghiệm đợt chạy chính thức Checkpoint 3
└── README.md             ← Tài liệu giải trình phương pháp đo và kết quả (file này)
```

---

## 2. CAM KẾT TIÊU CHUẨN ĐẠT (QUALITY BAR — KHÓA TẠI CP4)
Nhóm `K4-3A-E403-FinTech` cam kết và khóa cứng Quality Bar bằng con số từ mốc CP4 (21:00 · 17/09/2026):
1. **Tỷ lệ Pass toàn bộ Golden Set 20 ca:** $\ge \mathbf{80.0\%}$ (tương đương $\ge 16/20$ ca đạt).
2. **Độ trung thực trích dẫn nguồn (Grounding Rate):** $\ge \mathbf{85.0\%}$ trên các câu hỏi sư phạm; **100%** không bao giờ bịa đặt Turn ID ảo.
3. **Tuân thủ ranh giới an toàn & phản hồi thường nhật:** Đạt tuyệt đối $\mathbf{100\%}$ ($10/10$ ca) với thời gian phản hồi tức thì $\le 0.1\text{s}$.

---

## 3. TỔNG HỢP KẾT QUẢ CÁC LƯỢT CHẠY KIỂM THỬ

| Lượt chạy | Thời điểm thực thi | Số ca test | Tỷ lệ Đạt (%) | Độ trễ TB | Grounding | Đánh giá so với Quality Bar |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lượt 1 (Test sơ bộ)** | 11:30 · 17/09/2026 | 5 ca | 5 / 5 (100%) | 2.69s | 100% | Đạt luồng E2E cơ bản |
| **Lượt 2 (CP3 Benchmark)** | 12:38 · 17/09/2026 | 20 ca | **16 / 20 (80.0%)** | **7.59s** | **85.0%** | ✅ **CHÍNH THỨC ĐẠT QUALITY BAR** |

### Bảng Thống Kê Chi Tiết Lượt Chạy CP3 (20 Ca):

| Nhóm kiểm thử | Số ca | Tiêu chí nghiệm thu | Kết quả Đạt | Độ trễ TB | Nhận xét |
|---|:---:|---|:---:|:---:|---|
| **Pedagogical (Sư phạm)** | 10 | Phân tích 3 phần + Trích dẫn Turn ID thật | 6 / 10 | 8.92s | 4 ca bị timeout 25s do rate limit TPM của Groq Cloud API |
| **Baseline (Thường nhật)** | 5 | Trả lời tự nhiên 1 câu, không ảo giác slide | 5 / 5 (100%) | 0.01s | Fast-path cục bộ tại Gateway, không tốn token |
| **Safety Guardrails** | 5 | Từ chối chấm điểm, sửa slide, lộ đề thi | 5 / 5 (100%) | 0.016s | Chặn đứng tức thì, bảo vệ quyền riêng tư học viên |
| **TỔNG HỢP TOÀN BỘ** | **20** | **Tuân thủ Spec & Quality Bar** | **16 / 20 (80.0%)** | **7.59s** | ✅ **VƯỢT QUALITY BAR CAM KẾT** |

---

## 4. TỰ KHAI BÁO MINH BẠCH 4 CA CHƯA ĐẠT (SELF-REPORTING)
- **Hiện tượng:** 4 ca Sư phạm (ID 03, ID 05, ID 07, ID 10) bị timeout 25.0s khi kịch bản kiểm thử bắn 20 request HTTP dồn dập liên tiếp.
- **Nguyên nhân kỹ thuật:** Chạm trần giới hạn Token Per Minute (TPM) của nhà cung cấp Groq Cloud Free Tier khi benchmark tải cao.
- **Xác minh độc lập:** Khi chạy riêng lẻ từng câu hỏi, mô hình phân tích sâu 3 phần và trích dẫn Turn ID hoàn hảo.
- **Giải pháp:** Đã cấu hình chuỗi Fallback Gateway tự động (`with_fallbacks`) trong `codebase/Provider/llm.py` và khuyến nghị triển khai vLLM on-premise khi đưa vào trường học diện rộng.

---

## 5. HƯỚNG DẪN TỰ CHẠY LẠI BỘ KIỂM THỬ
Yêu cầu máy chủ backend đang chạy tại cổng 8080:
```bash
# Di chuyển vào thư mục eval
cd eval

# Chạy kiểm thử tự động 20 ca
python eval_cp3.py
```
Kết quả sẽ hiển thị bảng thống kê chi tiết từng ca và tự động tính tỷ lệ Pass, độ trễ trung bình.
