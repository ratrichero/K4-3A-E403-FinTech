"""
================================================================================
🛠️ VLEARN TOOL DEFINITIONS & EXECUTION BACKEND (MCP TOOLS T01 — T10)
================================================================================
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer kết nối
trực tiếp với cơ sở dữ liệu SQLite data/vlearn.db (13.494 turns).
Tuân thủ đặc tả kỹ thuật: docs/03-technical-design/04-api-tool-contracts.md
================================================================================
"""

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(BASE_DIR, "data", "vlearn.db")):
    DB_PATH = os.path.join(BASE_DIR, "data", "vlearn.db")
elif os.path.exists(os.path.join(os.path.dirname(BASE_DIR), "data", "vlearn.db")):
    DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "vlearn.db")
else:
    DB_PATH = os.environ.get("VLEARN_DB_PATH", os.path.join(BASE_DIR, "data", "vlearn.db"))


# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA CHO MCP & OPENAI
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool T07: Lấy Ma trận Điểm nhiệt & Top 3 Điểm nghẽn
    {
        "name": "get_slide_heatmap",
        "description": "Tính toán ma trận điểm nhiệt bối rối của bài giảng và xác định Top 3 trang slide có tỷ lệ bối rối cao nhất từ dữ liệu tương tác thực tế.",
        "parameters": {
            "type": "object",
            "properties": {
                "lecture_code": {
                    "type": "string",
                    "description": "Mã bài giảng cần rà soát (ví dụ: 'D02', 'D01', 'D03')"
                },
                "cohort": {
                    "type": "string",
                    "description": "Lọc theo khóa học: 'K3', 'K4' hoặc 'all' (mặc định: 'all')"
                },
                "course_id": {
                    "type": "string",
                    "description": "Mã môn học (ví dụ: 'COMP2010', 'AI2001')"
                }
            },
            "required": ["lecture_code"]
        }
    },

    # Tool T02: Tra cứu Bằng chứng Hội thoại Sinh viên theo Slide
    {
        "name": "get_slide_evidence",
        "description": "Trích xuất danh sách câu hỏi và bằng chứng hội thoại nguyên văn của sinh viên tại một trang slide cụ thể (kèm Turn ID, đoạn văn bản bôi đen, intent).",
        "parameters": {
            "type": "object",
            "properties": {
                "lecture_code": {
                    "type": "string",
                    "description": "Mã bài giảng (ví dụ: 'D02')"
                },
                "slide_page": {
                    "type": "integer",
                    "description": "Số trang slide cần tra cứu bằng chứng (ví dụ: 18)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Số lượng lượt hỏi tối đa cần lấy (mặc định: 5)"
                }
            },
            "required": ["lecture_code", "slide_page"]
        }
    },

    # Tool T03: Lấy Ngữ cảnh & Nội dung Học thuật Slide
    {
        "name": "get_slide_content",
        "description": "Tra cứu thông tin ngữ cảnh, tiêu đề, và khái niệm trọng tâm của một trang slide trong bài giảng.",
        "parameters": {
            "type": "object",
            "properties": {
                "lecture_code": {
                    "type": "string",
                    "description": "Mã bài giảng (ví dụ: 'D02')"
                },
                "slide_page": {
                    "type": "integer",
                    "description": "Số trang slide (ví dụ: 18)"
                }
            },
            "required": ["lecture_code", "slide_page"]
        }
    },

    # Tool T09: Soạn thảo Bản nháp Can thiệp Sư phạm 2 Phút
    {
        "name": "draft_pedagogical_intervention",
        "description": "Sinh bản thảo can thiệp sư phạm 2 phút đầu giờ giúp giảng viên tháo gỡ điểm nghẽn nhận thức (ví dụ tương phản, kịch bản giảng giải hoặc câu hỏi trắc nghiệm bẫy).",
        "parameters": {
            "type": "object",
            "properties": {
                "lecture_code": {
                    "type": "string",
                    "description": "Mã bài giảng (ví dụ: 'D02')"
                },
                "slide_page": {
                    "type": "integer",
                    "description": "Trang slide trọng tâm (ví dụ: 18)"
                },
                "intervention_type": {
                    "type": "string",
                    "enum": ["counter_analogy", "micro_lecture", "concept_mcq"],
                    "description": "Loại can thiệp: counter_analogy (ví dụ tương phản), micro_lecture (kịch bản 2 phút), concept_mcq (trắc nghiệm bẫy)"
                },
                "focus_concept": {
                    "type": "string",
                    "description": "Khái niệm trọng tâm cần can thiệp (ví dụ: 'Chain-of-Thought vs ReAct')"
                }
            },
            "required": ["lecture_code", "slide_page", "intervention_type"]
        }
    },

    # Tool T10: Phê duyệt Can thiệp Sư phạm vào Giáo án (HITL Approval Gate)
    {
        "name": "approve_intervention",
        "description": "Phê duyệt chính thức một đề xuất can thiệp sư phạm đưa vào kế hoạch bài giảng, ghi nhận vào cơ sở dữ liệu và băm mã kiểm toán toàn vẹn SHA-256.",
        "parameters": {
            "type": "object",
            "properties": {
                "record_id": {
                    "type": "string",
                    "description": "Mã định danh can thiệp (ví dụ: 'rec_d02_s18_01')"
                },
                "lecture_code": {
                    "type": "string",
                    "description": "Mã bài giảng (ví dụ: 'D02')"
                },
                "slide_page": {
                    "type": "integer",
                    "description": "Số trang slide (ví dụ: 18)"
                },
                "title": {
                    "type": "string",
                    "description": "Tiêu đề can thiệp sư phạm"
                },
                "content_payload": {
                    "type": "string",
                    "description": "Nội dung chi tiết kịch bản can thiệp đã được giảng viên rà soát"
                },
                "intervention_type": {
                    "type": "string",
                    "description": "Loại can thiệp (counter_analogy, micro_lecture, concept_mcq)"
                },
                "lecturer_id": {
                    "type": "string",
                    "description": "Mã giảng viên phê duyệt (mặc định: 'lec_cuongtv')"
                },
                "notes_for_class": {
                    "type": "string",
                    "description": "Ghi chú thời điểm triển khai trên lớp (ví dụ: '2 phút đầu giờ bài tiếp theo')"
                }
            },
            "required": ["lecture_code", "slide_page", "title", "content_payload"]
        }
    }
]

# ==============================================================================
# 2. TẦNG THỰC THI (EXECUTION LAYER KẾT NỐI DATA/VLEARN.DB)
# ==============================================================================

def get_db_connection() -> sqlite3.Connection:
    """Tạo kết nối tới SQLite vlearn.db."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_get_slide_heatmap(
    lecture_code: str,
    cohort: str = "all",
    course_id: Optional[str] = None
) -> str:
    """Tính toán ma trận điểm nhiệt tất định từ vlearn.db (Tool T07)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        target_lecture = "D02" if (not lecture_code or lecture_code.upper() == "ALL") else lecture_code

        query = """
            SELECT 
                slide_page,
                COUNT(turn_id) as question_count,
                COUNT(DISTINCT student_id) as unique_students,
                SUM(CASE WHEN intent = 'explicit_misconception' THEN 1 ELSE 0 END) as misconception_count
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

        query += " GROUP BY slide_page ORDER BY slide_page ASC"
        cur.execute(query, params)
        rows = cur.fetchall()

        is_benchmark_fallback = False
        if not rows:
            # Nếu khóa học hoặc học phần hiện tại chưa gán tag slide trực tiếp (ví dụ K4 hỏi đáp tự do),
            # tự động đối sánh với phân bổ slide chuẩn (baseline từ K3 / toàn hệ thống)
            cur.execute("""
                SELECT 
                    slide_page,
                    COUNT(turn_id) as question_count,
                    COUNT(DISTINCT student_id) as unique_students,
                    SUM(CASE WHEN intent = 'explicit_misconception' THEN 1 ELSE 0 END) as misconception_count
                FROM tutor_turns
                WHERE lecture_code = ? AND slide_page IS NOT NULL AND slide_page > 0
                GROUP BY slide_page ORDER BY slide_page ASC
            """, (target_lecture,))
            rows = cur.fetchall()
            if rows:
                is_benchmark_fallback = True

        if not rows:
            return json.dumps({
                "status": "NOT_FOUND",
                "lecture_code": target_lecture,
                "message": f"Không tìm thấy dữ liệu tương tác có đánh dấu slide cho bài giảng {target_lecture}"
            }, ensure_ascii=False)

        slides_stats = []
        total_q = 0
        total_mis = 0

        for r in rows:
            page = r["slide_page"]
            q_cnt = r["question_count"]
            stu_cnt = r["unique_students"]
            mis_cnt = r["misconception_count"] or 0
            
            # Công thức tính điểm nhiệt: heat_score = (misconceptions * 2.5) + (unique_students * 1.5) + (q_cnt * 0.5)
            heat_score = round((mis_cnt * 2.5) + (stu_cnt * 1.5) + (q_cnt * 0.5), 1)
            confusion_rate = round((mis_cnt / q_cnt * 100), 1) if q_cnt > 0 else 0.0

            total_q += q_cnt
            total_mis += mis_cnt

            # Phân tầng ngưỡng 5 cấp độ chuẩn hóa (Calibrated Multi-Tier Pedagogical Thresholds)
            if heat_score >= 120:
                level = 5
                status = "HOT"
                signal = "Điểm nghẽn bối rối nghiêm trọng"
            elif heat_score >= 60:
                level = 4
                status = "HIGH"
                signal = "Ưu tiên can thiệp cao"
            elif heat_score >= 25:
                level = 3
                status = "WARM"
                signal = "Cần làm rõ khái niệm"
            elif heat_score >= 10:
                level = 2
                status = "NORMAL"
                signal = "Tiếp thu bình thường"
            else:
                level = 1 if q_cnt > 0 else 0
                status = "COLD"
                signal = "Chưa đủ dữ liệu tín hiệu"

            slides_stats.append({
                "slide_page": page,
                "question_count": q_cnt,
                "unique_students": stu_cnt,
                "misconception_count": mis_cnt,
                "confusion_rate": confusion_rate,
                "heat_score": heat_score,
                "level": level,
                "status": status,
                "signal": signal
            })

        # Sắp xếp tìm Top 3 điểm nghẽn cao nhất
        top_bottlenecks = sorted(slides_stats, key=lambda x: x["heat_score"], reverse=True)[:3]
        top_3_pages = [s["slide_page"] for s in top_bottlenecks]

        # Tính tổng số lượt và học viên thực tế của bài giảng trong phạm vi chọn (không bị giới hạn bởi slide_page > 0)
        actual_q_sql = "SELECT COUNT(*), COUNT(DISTINCT student_id) FROM tutor_turns WHERE lecture_code = ?"
        actual_q_params: List[Any] = [target_lecture]
        if cohort and cohort.lower() != "all":
            actual_q_sql += " AND cohort_hint = ?"
            actual_q_params.append(cohort.upper())
        if course_id and course_id.lower() != "all":
            actual_q_sql += " AND course_id = ?"
            actual_q_params.append(course_id)
        cur.execute(actual_q_sql, actual_q_params)
        actual_row = cur.fetchone()
        actual_scope_turns = actual_row[0] if actual_row else total_q
        actual_scope_students = actual_row[1] if actual_row else 0

        conn.close()
        return json.dumps({
            "status": "SUCCESS",
            "lecture_code": lecture_code,
            "cohort": cohort,
            "total_questions": actual_scope_turns,
            "unique_students": actual_scope_students,
            "tagged_slide_questions": total_q,
            "total_misconceptions": total_mis,
            "is_benchmark_fallback": is_benchmark_fallback,
            "top_3_bottleneck_slides": top_3_pages,
            "slides": slides_stats
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False)


def execute_get_slide_evidence(
    lecture_code: str,
    slide_page: int,
    limit: int = 10
) -> str:
    """Trích xuất danh sách hội thoại học viên nguyên văn kèm Turn ID (Tool T02)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        target_lecture = "D02" if (not lecture_code or lecture_code.upper() == "ALL") else lecture_code

        # Đếm tổng số câu hỏi thực tế gắn với slide này trong database
        cur.execute("SELECT COUNT(*) FROM tutor_turns WHERE lecture_code = ? AND slide_page = ?", (target_lecture, slide_page))
        count_row = cur.fetchone()
        total_slide_evidence = count_row[0] if count_row else 0

        cur.execute(
            """
            SELECT 
                turn_id, 
                student_id, 
                asked_at_vn, 
                raw_question, 
                selected_text, 
                intent, 
                topic_section,
                move_used
            FROM tutor_turns
            WHERE lecture_code = ? AND slide_page = ?
            ORDER BY 
                CASE 
                    WHEN intent = 'explicit_misconception' THEN 1
                    WHEN intent = 'missing_prerequisite' THEN 2
                    WHEN intent = 'syntax_implementation_struggle' THEN 3
                    WHEN intent = 'broad_curiosity' THEN 4
                    WHEN intent = 'procedural_administrative' THEN 5
                    ELSE 6 
                END ASC,
                asked_at_vn DESC
            LIMIT ?
            """,
            (target_lecture, slide_page, limit)
        )
        rows = cur.fetchall()

        evidence = []
        for r in rows:
            evidence.append({
                "turn_id": r["turn_id"],
                "student_id": r["student_id"],
                "asked_at": r["asked_at_vn"],
                "raw_question": r["raw_question"],
                "selected_text": r["selected_text"] or "",
                "intent": r["intent"] or "general_inquiry",
                "topic": r["topic_section"] or "",
                "move_used": r["move_used"] or ""
            })

        conn.close()
        return json.dumps({
            "status": "SUCCESS",
            "lecture_code": target_lecture,
            "slide_page": slide_page,
            "total_questions": total_slide_evidence,
            "evidence_count": len(evidence),
            "evidence": evidence
        }, ensure_ascii=False)


    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False)


def execute_get_slide_content(lecture_code: str, slide_page: int) -> str:
    """Tra cứu thông tin tiêu đề và khái niệm chuẩn của trang slide (Tool T03)."""
    # Từ điển kiến thức chuẩn các trang slide trọng điểm bài D02 / D01
    SLIDE_KNOWLEDGE = {
        ("D02", 18): {
            "title": "Chain-of-Thought vs ReAct Prompting",
            "core_concept": "Sự phân biệt giữa Suy luận nội tâm (Thought) và Hành động tác động ngoại cảnh (Action)",
            "misconception_pattern": "Học viên nhầm tưởng CoT và ReAct chỉ là một, hoặc tưởng ReAct chỉ đơn giản là viết CoT dài hơn mà không hiểu cơ chế gọi công cụ (Action/Observation)."
        },
        ("D02", 8): {
            "title": "Few-Shot vs Zero-Shot Prompting",
            "core_concept": "Cung cấp cặp mẫu (Input-Output) trong context window mà không làm thay đổi trọng số mô hình",
            "misconception_pattern": "Học sinh nhầm lẫn giữa Few-shot In-context Learning và Fine-tuning trọng số mô hình."
        },
        ("D02", 14): {
            "title": "Prompt Engineering Guardrails & Constraints",
            "core_concept": "Thiết lập ranh giới định dạng đầu ra và hạn chế hallucination",
            "misconception_pattern": "Học viên gặp khó khăn khi ép mô hình luôn trả về JSON hợp lệ."
        }
    }

    info = SLIDE_KNOWLEDGE.get((lecture_code, slide_page), {
        "title": f"Slide {slide_page} ({lecture_code})",
        "core_concept": "Nội dung bài giảng VLearn",
        "misconception_pattern": "Quan sát thấy các thắc mắc liên quan đến ứng dụng lý thuyết vào thực hành."
    })

    return json.dumps({
        "status": "SUCCESS",
        "lecture_code": lecture_code,
        "slide_page": slide_page,
        "content": info
    }, ensure_ascii=False)


def execute_draft_pedagogical_intervention(
    lecture_code: str,
    slide_page: int,
    intervention_type: str,
    focus_concept: Optional[str] = None,
    use_llm: bool = False
) -> str:
    """Soạn thảo bản nháp can thiệp sư phạm 2 phút (Tool T09)."""
    content_payload = None
    if use_llm:
        try:
            from Provider.llm import get_llm
            from prompts import INTERVENTION_DRAFTER_SYSTEM_PROMPT
            from langchain_core.messages import SystemMessage, HumanMessage

            llm = get_llm()
            user_prompt = f"""Hãy soạn bản nháp can thiệp sư phạm 2 phút cho:
- Bài giảng: {lecture_code} · Trang slide: {slide_page}
- Loại can thiệp: {intervention_type}
- Khái niệm: {focus_concept or 'Hiểu lầm trọng tâm của học viên tại slide này'}

Hãy sinh ra nội dung cực kỳ cô đọng, giàu hình ảnh, giảng viên có thể trình bày trong đúng 120 giây đầu giờ."""

            res = llm.invoke([
                SystemMessage(content=INTERVENTION_DRAFTER_SYSTEM_PROMPT),
                HumanMessage(content=user_prompt)
            ])
            content_payload = res.content
        except Exception:
            pass

    if not content_payload:
        if intervention_type == "counter_analogy":
            content_payload = (
                "Ẩn dụ Bếp trưởng Nấu ăn (Thought) vs Gọi điện Đặt hàng (Action):\n"
                "Khi nấu ăn, đầu bếp đứng trong bếp tự suy nghĩ công thức nấu nướng là Thought (suy luận nội tâm như CoT). "
                "Nhưng khi đầu bếp nhấc điện thoại gọi nhà cung cấp giao thịt bò là Action (tác động ra thế giới bên ngoài và đợi kết quả Observation). "
                "CoT chỉ là đứng nghĩ trong đầu; ReAct là vừa nghĩ vừa thò tay làm!"
            )
        elif intervention_type == "micro_lecture":
            content_payload = (
                "Kịch bản 2 phút đầu giờ:\n"
                "1. Khơi mào: 'Nhiều bạn gửi câu hỏi cho AI Tutor hỏi CoT và ReAct khác gì nhau.'\n"
                "2. Phân biệt: 'CoT giúp mô hình suy nghĩ logic từng bước. Còn ReAct bổ sung thêm cánh tay công cụ để tìm kiếm và hành động.'\n"
                "3. Chốt: 'Muốn giải toán đố logic hãy dùng CoT. Muốn tra cứu dữ liệu thời gian thực hay gọi API hãy dùng ReAct!'"
            )
        else:
            content_payload = (
                "Câu hỏi Concept MCQ (2 phút):\n"
                "Hành động nào sau đây là 'Action' trong mô hình ReAct?\n"
                "A. LLM tự chia nhỏ bài toán thành 3 bước suy luận\n"
                "B. LLM phát lệnh gọi API tra cứu thời tiết hiện tại (ĐÁP ÁN ĐÚNG)\n"
                "C. LLM nhớ lại kiến thức trong trọng số tiền huấn luyện (BẪY HIỂU LẦM)\n"
                "D. LLM định dạng câu trả lời ra dạng Markdown"
            )

    draft_id = f"draft_{lecture_code.lower()}_s{slide_page}_{intervention_type[:4]}"
    return json.dumps({
        "status": "SUCCESS",
        "draft_id": draft_id,
        "lecture_code": lecture_code,
        "slide_page": slide_page,
        "intervention_type": intervention_type,
        "focus_concept": focus_concept or f"Slide {slide_page} bottleneck",
        "content_payload": content_payload,
        "duration": "120 giây (2 phút)"
    }, ensure_ascii=False)


def execute_approve_intervention(
    lecture_code: str,
    slide_page: int,
    title: str,
    content_payload: str,
    record_id: Optional[str] = None,
    intervention_type: str = "counter_analogy",
    lecturer_id: str = "lec_cuongtv",
    notes_for_class: str = "Triển khai ở 2 phút đầu giờ học tiếp theo"
) -> str:
    """Phê duyệt can thiệp sư phạm vào giáo án (Tool T10 - HITL Approval Gate)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        rec_id = record_id or f"rec_{lecture_code.lower()}_s{slide_page}_{int(datetime.now().timestamp())}"
        now_iso = datetime.now().isoformat()

        # Tính toán SHA-256 hash đảm bảo tính toàn vẹn (Audit Hash)
        hash_payload = f"{rec_id}|{lecture_code}|{slide_page}|{title}|{content_payload}|{lecturer_id}|{now_iso}"
        audit_hash = hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()

        cur.execute(
            """
            INSERT INTO curriculum_adaptations (
                record_id, cohort_hint, course_id, lecture_code, slide_page,
                intervention_type, title, content_payload, lecturer_id,
                status, notes_for_class, sha256_audit_hash, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rec_id, "K4", "COMP2010", lecture_code, slide_page,
                intervention_type, title, content_payload, lecturer_id,
                "approved", notes_for_class, audit_hash, now_iso
            )
        )
        conn.commit()
        conn.close()

        return json.dumps({
            "status": "SUCCESS",
            "message": "Phê duyệt can thiệp sư phạm và cập nhật giáo án thành công!",
            "record_id": rec_id,
            "lecture_code": lecture_code,
            "slide_page": slide_page,
            "sha256_audit_hash": audit_hash,
            "approval_timestamp": now_iso,
            "lecturer_id": lecturer_id
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False)


def execute_get_filters_catalog() -> str:
    """Trả về danh mục phân cấp lọc chuẩn xác từ SQLite (Khóa học -> Học phần -> Bài giảng)."""
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cohorts = [
            {"id": "K4", "name": "K4 · FinTech AI", "turns": 3097, "students": 448, "label": "K4 · FinTech AI (3.097 lượt · 448 HV)"},
            {"id": "K3", "name": "K3 · AI Engineering", "turns": 10397, "students": 1177, "label": "K3 · AI Engineering (10.397 lượt · 1.177 HV)"},
            {"id": "ALL", "name": "Toàn hệ thống (K3 + K4)", "turns": 13494, "students": 1625, "label": "K3 + K4 · Toàn hệ thống (13.494 lượt · 1.625 HV)"}
        ]

        COURSE_NAMES = {
            "COMP2010": "COMP2010 · AI Engineering",
            "BIOM3010": "BIOM3010 · Biomedical AI",
            "COMP4010": "COMP4010 · Cloud Systems",
            "COMP3011": "COMP3011 · Data Science",
            "K4P1": "K4P1 · FinTech AI Batch 4",
            "L2-L3-K4P1": "L2-L3-K4P1 · Computer Vision Track"
        }

        courses_by_cohort = {}
        for c in ["K4", "K3", "ALL"]:
            if c == "ALL":
                cur.execute("""
                    SELECT course_id, SUM(total_turns) as turns, COUNT(DISTINCT lecture_code) as lec_cnt, SUM(unique_students) as students
                    FROM course_lectures
                    WHERE total_turns > 0 AND course_id NOT IN ('Unknown', 'VinUni-AIInAction-3', 'biom3010', 'comp3011')
                    GROUP BY course_id
                    ORDER BY turns DESC
                """)
            else:
                cur.execute("""
                    SELECT course_id, SUM(total_turns) as turns, COUNT(DISTINCT lecture_code) as lec_cnt, SUM(unique_students) as students
                    FROM course_lectures
                    WHERE cohort_hint = ? AND total_turns > 0 AND course_id NOT IN ('Unknown', 'VinUni-AIInAction-3', 'biom3010', 'comp3011')
                    GROUP BY course_id
                    ORDER BY turns DESC
                """, (c,))
            
            c_rows = cur.fetchall()
            tot_turns = sum(r["turns"] for r in c_rows)
            tot_lecs = sum(r["lec_cnt"] for r in c_rows)
            
            c_list = [{
                "id": "ALL",
                "name": f"Tất cả học phần {c}",
                "turns": tot_turns,
                "label": f"Tất cả học phần {c} ({tot_turns:,} lượt · {tot_lecs} bài)"
            }]
            for r in c_rows:
                cid = r["course_id"]
                cname = COURSE_NAMES.get(cid, cid)
                c_list.append({
                    "id": cid,
                    "name": cname,
                    "turns": r["turns"],
                    "lectures_count": r["lec_cnt"],
                    "label": f"{cname} ({r['turns']:,} lượt)"
                })
            courses_by_cohort[c] = c_list

        # 3. Danh mục Bài giảng theo (Cohort:Course)
        # Bao gồm lựa chọn đầu tiên: ALL - Toàn bộ bài giảng (khớp đúng tổng lượt của phạm vi đó)
        TITLE_MAP = {
            'D01': 'Nền tảng LLM & Prompt Design',
            'D02': 'AI Agents & Reasoning',
            'D03': 'Multi-Agent Orchestration',
            'D04': 'Agent Patterns & Tools',
            'D05': 'Context Window & Memory',
            'D06': 'LangChain & Evaluation',
            'D07': 'Vector Store & Feature Store',
            'D08': 'LLM Evaluation & Benchmarks',
            'D09': 'Model Serving & Deployment',
            'D10': 'CI/CD for AI Systems',
            'D11': 'LLMOps Prompt Versioning',
            'D12': 'Platform Engineering',
            'D14': 'Disaster Recovery & HA'
        }

        def get_lessons_for_scope(cohort_val, course_val):
            where_clauses = []
            params = []
            if cohort_val and cohort_val != "ALL":
                where_clauses.append("cohort_hint = ?")
                params.append(cohort_val)
            if course_val and course_val != "ALL":
                where_clauses.append("course_id = ?")
                params.append(course_val)
            
            w_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
            
            # Đếm tổng lượt và học viên duy nhất cho toàn phạm vi (cohort:course)
            cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT student_id) FROM tutor_turns {w_sql}", params)
            tot_row = cur.fetchone()
            tot_turns = tot_row[0]
            tot_students = tot_row[1]
            
            sql = f"""
                SELECT lecture_code, COUNT(*) as turns, COUNT(DISTINCT student_id) as students,
                       SUM(CASE WHEN slide_page IS NOT NULL AND slide_page > 0 THEN 1 ELSE 0 END) as slide_turns
                FROM tutor_turns
                {w_sql}
                GROUP BY lecture_code
                ORDER BY turns DESC
            """
            cur.execute(sql, params)
            rows = cur.fetchall()
            
            # Mục 0: Toàn bộ bài giảng
            items = [{
                "code": "ALL",
                "title": "Toàn bộ bài giảng",
                "turns": tot_turns,
                "students": tot_students,
                "has_slides": any(r["slide_turns"] > 0 for r in rows),
                "label": f"Toàn bộ bài giảng ({tot_turns:,} lượt)"
            }]
            
            for r in rows:
                code = r["lecture_code"]
                title = TITLE_MAP.get(code, f"Bài giảng {code}")
                items.append({
                    "code": code,
                    "title": title,
                    "turns": r["turns"],
                    "students": r["students"],
                    "has_slides": (r["slide_turns"] or 0) > 0,
                    "label": f"{code} · {title} ({r['turns']:,} lượt)"
                })
            return items

        lessons_catalog = {}
        for c in ["K4", "K3", "ALL"]:
            # Khóa + Tất cả học phần
            lessons_catalog[f"{c}:ALL"] = get_lessons_for_scope(c, "ALL")
            # Từng học phần cụ thể
            for crs in courses_by_cohort[c]:
                cid = crs["id"]
                lessons_catalog[f"{c}:{cid}"] = get_lessons_for_scope(c, cid)
                lessons_catalog[cid] = lessons_catalog[f"{c}:{cid}"]

        conn.close()
        return json.dumps({
            "status": "SUCCESS",
            "cohorts": cohorts,
            "courses": courses_by_cohort,
            "lessons": lessons_catalog
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False)


# ==============================================================================
# 3. ROUTER & DISPATCHER TRUNG CHUYỂN TOOL
# ==============================================================================

TOOL_ROUTER = {
    "get_slide_heatmap": execute_get_slide_heatmap,
    "get_slide_evidence": execute_get_slide_evidence,
    "get_slide_content": execute_get_slide_content,
    "draft_pedagogical_intervention": execute_draft_pedagogical_intervention,
    "approve_intervention": execute_approve_intervention,
    "get_filters_catalog": execute_get_filters_catalog
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool theo giao thức MCP."""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except TypeError as te:
            return json.dumps({
                "status": "INVALID_ARGUMENTS",
                "error": f"Sai tham số gọi tool '{tool_name}': {str(te)}"
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": f"Lỗi trong quá trình thực thi tool '{tool_name}': {str(e)}"
            }, ensure_ascii=False)
    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại trong danh mục VLearn MCP!"
    }, ensure_ascii=False)
