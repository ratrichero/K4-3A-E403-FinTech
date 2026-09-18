"""
================================================================================
📊 VLEARN PEDAGOGICAL HEATMAP — 2D BLOOM & PARETO RANKING ENGINE
================================================================================
Module tính toán điểm nhiệt sư phạm chuẩn hóa dựa trên ghi chú nghiên cứu (notes.md).

1. CHỈ SỐ SƯ PHẠM:
   - Q_s: Tổng số câu hỏi phát sinh tại slide s
   - U_s: Số học viên độc lập đặt câu hỏi tại slide s
   - I_s = Q_s / U_s: Cường độ bế tắc (số câu hỏi / người)
   - C_s: Mức độ khó nhận thức theo thang Bloom chuẩn hóa [0, 1]
     Ánh xạ cột 'intent' trong SQLite vlearn.db:
     • explicit_misconception: 3.0 (Analyze / Evaluate - Hiểu sai bản chất)
     • missing_prerequisite: 1.5 (Understand - Hổng kiến thức cần giải thích)
     • syntax_implementation_struggle: 1.5 (Apply - Vướng mắc thực hành/code)
     • broad_curiosity: 0.5 (Khác - Tò mò mở rộng)
     • procedural_administrative: 0.5 (Khác - Thủ tục ngoài lề)
     C_s = sum(w_i) / (3.0 * Q_s)

2. TỌA ĐỘ 2 CHIỀU:
   - Depth_s   = 0.7 * C_s + 0.3 * (1 - 1 / I_s)
   - Breadth_s = U_s / N (N là sĩ số lớp học, mặc định 450 học viên hoặc tự động tính)

3. PHÂN BỔ 4 Ô (QUADRANTS):
   - Ngưỡng Depth:   θ_Depth   = max(0.30, Median(Depth))
   - Ngưỡng Breadth: θ_Breadth = max(0.05, Median(Breadth))
   • GÓC 1 (High Depth, High Breadth): Điểm nghẽn bài giảng (Giảng lại đầu giờ)
   • GÓC 2 (High Depth, Low Breadth):  Cần kèm riêng (TA hỗ trợ 1-1)
   • GÓC 3 (Low Depth,  High Breadth): Sửa Slide / Bổ sung ví dụ
   • GÓC 4 (Low Depth,  Low Breadth):  Bình thường (Không cần can thiệp)

4. XẾP HẠNG PARETO FRONTIER:
   - Non-dominated Sorting xác định đường biên tối ưu đa mục tiêu (Breadth & Depth).
================================================================================
"""

import os
import sys
import json
import sqlite3
import statistics
from typing import Dict, Any, List, Optional, Tuple

# Bảng trọng số Bloom ánh xạ trực tiếp từ cột 'intent' trong vlearn.db
BLOOM_INTENT_WEIGHTS = {
    "explicit_misconception": 3.0,          # Hiểu sai bản chất (3.0)
    "missing_prerequisite": 1.5,            # Cần giải thích khái niệm (1.5)
    "syntax_implementation_struggle": 1.5, # Vướng thực hành/code (1.5)
    "broad_curiosity": 0.5,                 # Khác (0.5)
    "procedural_administrative": 0.5        # Khác (0.5)
}
MAX_WEIGHT = 3.0

# Sĩ số mặc định nếu không có trong DB (Hardcoded N theo yêu cầu)
DEFAULT_CLASS_SIZE_N = 450


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Kết nối tới SQLite vlearn.db."""
    if not db_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, "data/vlearn.db")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Không tìm thấy database tại: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def calculate_normalized_heatmap(
    lecture_code: str = "D02",
    cohort: str = "all",
    course_id: Optional[str] = None,
    class_size_n: int = DEFAULT_CLASS_SIZE_N,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tính toán Heatmap và phân ô 2 chiều theo đúng công thức trong notes.md.
    """
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    target_lecture = "D02" if (not lecture_code or lecture_code.upper() == "ALL") else lecture_code

    # 1. Truy vấn toàn bộ turns có gắn slide_page của bài giảng
    query = """
        SELECT 
            slide_page,
            student_id,
            intent
        FROM tutor_turns
        WHERE lecture_code = ? AND slide_page IS NOT NULL AND slide_page > 0
    """
    params: List[Any] = [target_lecture]

    if cohort and cohort.lower() != "all":
        query += " AND cohort_hint = ?"
        params.append(cohort.upper())
    if course_id and course_id.lower() != "all":
        query += " AND course_id = ?"
        params.append(course_id)

    cur.execute(query, params)
    rows = cur.fetchall()

    if not rows:
        # Fallback toàn hệ thống nếu chưa có phân bổ
        cur.execute("""
            SELECT slide_page, student_id, intent
            FROM tutor_turns
            WHERE lecture_code = ? AND slide_page IS NOT NULL AND slide_page > 0
        """, (target_lecture,))
        rows = cur.fetchall()

    conn.close()

    if not rows:
        return {
            "status": "NOT_FOUND",
            "lecture_code": target_lecture,
            "message": f"Không có dữ liệu slide cho bài {target_lecture}"
        }

    # 2. Gom nhóm theo slide_page
    slides_data: Dict[int, List[Dict[str, Any]]] = {}
    for r in rows:
        p = r["slide_page"]
        if p not in slides_data:
            slides_data[p] = []
        slides_data[p].append({
            "student_id": r["student_id"],
            "intent": r["intent"] or "procedural_administrative"
        })

    # 3. Tính toán 5 chỉ số cho từng slide
    slides_metrics: List[Dict[str, Any]] = []
    all_depths = []
    all_breadths = []

    for page in sorted(slides_data.keys()):
        turns = slides_data[page]
        q_s = len(turns)
        students = set(t["student_id"] for t in turns)
        u_s = len(students)
        i_s = q_s / u_s if u_s > 0 else 1.0

        # Tính C_s: tổng trọng số chia cho (3.0 * Q_s)
        total_w = sum(BLOOM_INTENT_WEIGHTS.get(t["intent"], 0.5) for t in turns)
        c_s = total_w / (MAX_WEIGHT * q_s) if q_s > 0 else 0.0

        # Chuẩn hóa Breadth = U_s / N
        breadth = u_s / class_size_n

        # Chuẩn hóa Depth = 0.7 * C_s + 0.3 * (1 - 1 / I_s)
        repeat_ratio = 1.0 - (1.0 / i_s)
        depth = (0.7 * c_s) + (0.3 * repeat_ratio)

        # Đếm số lượng ngộ nhận
        mis_count = sum(1 for t in turns if t["intent"] == "explicit_misconception")

        metric = {
            "slide_page": page,
            "Q_s": q_s,
            "U_s": u_s,
            "I_s": round(i_s, 2),
            "misconception_count": mis_count,
            "C_s": round(c_s, 3),
            "Breadth": round(breadth, 3),
            "Depth": round(depth, 3)
        }
        slides_metrics.append(metric)
        all_depths.append(depth)
        all_breadths.append(breadth)

    # 4. Tính toán 2 Ngưỡng phân cách động (Thresholds)
    med_depth = statistics.median(all_depths) if all_depths else 0.30
    med_breadth = statistics.median(all_breadths) if all_breadths else 0.05

    theta_depth = max(0.30, med_depth)
    theta_breadth = max(0.05, med_breadth)

    # 5. Phân chia 4 Ô (4 Quadrants)
    for s in slides_metrics:
        is_high_depth = s["Depth"] > theta_depth
        is_high_breadth = s["Breadth"] > theta_breadth

        if is_high_depth and is_high_breadth:
            s["quadrant"] = "GÓC 1: ĐIỂM NGHẼN BÀI GIẢNG"
            s["quadrant_code"] = "Q1"
            s["action"] = "Giảng viên giảng lại 15 phút đầu giờ"
            s["priority_color"] = "RED"
        elif is_high_depth and not is_high_breadth:
            s["quadrant"] = "GÓC 2: CẦN KÈM RIÊNG"
            s["quadrant_code"] = "Q2"
            s["action"] = "Bàn giao danh sách cho TA hỗ trợ 1-1"
            s["priority_color"] = "ORANGE"
        elif not is_high_depth and is_high_breadth:
            s["quadrant"] = "GÓC 3: SỬA SLIDE / BỔ SUNG VÍ DỤ"
            s["quadrant_code"] = "Q3"
            s["action"] = "Sửa lại nội dung slide, bổ sung ví dụ minh họa"
            s["priority_color"] = "YELLOW"
        else:
            s["quadrant"] = "GÓC 4: BÌNH THƯỜNG"
            s["quadrant_code"] = "Q4"
            s["action"] = "Tiếp thu tốt, không cần can thiệp"
            s["priority_color"] = "GREEN"

    # 6. XẾP HẠNG PARETO FRONTIER (Non-dominated Sorting)
    # Slide A dominate Slide B nếu: Breadth_A >= Breadth_B VÀ Depth_A >= Depth_B (có ít nhất 1 dấu >)
    remaining_slides = list(slides_metrics)
    current_rank = 1

    while remaining_slides:
        frontier = []
        for candidate in remaining_slides:
            is_dominated = False
            for other in remaining_slides:
                if other == candidate:
                    continue
                # Kiểm tra xem other có áp đảo candidate không
                if (other["Breadth"] >= candidate["Breadth"] and other["Depth"] >= candidate["Depth"]) and \
                   (other["Breadth"] > candidate["Breadth"] or other["Depth"] > candidate["Depth"]):
                    is_dominated = True
                    break
            if not is_dominated:
                frontier.append(candidate)

        for s in frontier:
            s["pareto_rank"] = current_rank
            remaining_slides.remove(s)

        current_rank += 1

    # Sắp xếp danh sách slide ưu tiên theo Pareto Rank, sau đó đến Depth
    sorted_by_priority = sorted(slides_metrics, key=lambda x: (x["pareto_rank"], -x["Depth"], -x["Breadth"]))

    return {
        "status": "SUCCESS",
        "lecture_code": target_lecture,
        "class_size_N": class_size_n,
        "thresholds": {
            "theta_depth": round(theta_depth, 3),
            "theta_breadth": round(theta_breadth, 3),
            "median_depth": round(med_depth, 3),
            "median_breadth": round(med_breadth, 3)
        },
        "top_bottlenecks_pareto": sorted_by_priority[:3],
        "slides_metrics": sorted(slides_metrics, key=lambda x: x["slide_page"])
    }


# ==============================================================================
# DEMO KIỂM THỬ TRỰC TIẾP TRÊN DỮ LIỆU BÀI D02
# ==============================================================================
if __name__ == "__main__":
    print("=" * 85)
    print("🚀 TÍNH TOÁN HEATMAP 2D BLOOM & PARETO CHO BÀI GIẢNG D02:")
    print("=" * 85)

    res = calculate_normalized_heatmap(lecture_code="D02", class_size_n=450)

    if res.get("status") == "SUCCESS":
        t = res["thresholds"]
        print(f"📌 Sĩ số giả định (Hardcoded N): {res['class_size_N']} học viên")
        print(f"📌 Ngưỡng phân cách động: θ_Depth = {t['theta_depth']} | θ_Breadth = {t['theta_breadth']}")
        print("\n🏆 TOP 3 ĐIỂM NGHẼN THEO ĐƯỜNG BIÊN PARETO FRONTIER:")
        for idx, s in enumerate(res["top_bottlenecks_pareto"], 1):
            print(f"  Top {idx}: Slide {s['slide_page']} (Rank Pareto {s['pareto_rank']})")
            print(f"       • Số câu hỏi: {s['Q_s']} | Số người hỏi: {s['U_s']} | I_s: {s['I_s']} câu/người")
            print(f"       • Tọa độ: Breadth = {s['Breadth']} | Depth = {s['Depth']} (C_s = {s['C_s']})")
            print(f"       • Phân loại: [{s['quadrant']}] -> {s['action']}\n")

        print("=" * 85)
        print("📋 BẢNG THỐNG KÊ CHI TIẾT CÁC SLIDE (TRÍCH 10 SLIDE ĐẦU TIÊN):")
        print(f"{'Slide':<6} | {'Q_s':<5} | {'U_s':<5} | {'I_s':<5} | {'C_s':<6} | {'Breadth':<8} | {'Depth':<6} | {'Rank':<5} | {'Ô Hành Động'}")
        print("-" * 85)
        for s in res["slides_metrics"][:12]:
            print(f"{s['slide_page']:<6} | {s['Q_s']:<5} | {s['U_s']:<5} | {s['I_s']:<5} | {s['C_s']:<6.3f} | {s['Breadth']:<8.3f} | {s['Depth']:<6.3f} | {s['pareto_rank']:<5} | {s['quadrant_code']} ({s['quadrant'].split(':')[1].strip()})")
        print("=" * 85)
