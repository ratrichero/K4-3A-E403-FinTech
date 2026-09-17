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

        query = """
            SELECT 
                slide_page,
                COUNT(turn_id) as question_count,
                COUNT(DISTINCT student_id) as unique_students,
                SUM(CASE WHEN intent = 'explicit_misconception' THEN 1 ELSE 0 END) as misconception_count
            FROM tutor_turns
            WHERE lecture_code = ? AND slide_page IS NOT NULL AND slide_page > 0
        """
        params: List[Any] = [lecture_code]

        if cohort and cohort.lower() != "all":
            query += " AND cohort_hint = ?"
            params.append(cohort.upper())
        if course_id:
            query += " AND course_id = ?"
            params.append(course_id)

        query += " GROUP BY slide_page ORDER BY slide_page ASC"
        cur.execute(query, params)
        rows = cur.fetchall()

        if not rows:
            return json.dumps({
                "status": "NOT_FOUND",
                "lecture_code": lecture_code,
                "message": f"Không tìm thấy dữ liệu tương tác có đánh dấu slide cho bài giảng {lecture_code}"
            }, ensure_ascii=False)

        slides_stats = []
        total_q = 0
        total_mis = 0

        for r in rows:
            page = r["slide_page"]
            q_cnt = r["question_count"]
            stu_cnt = r["unique_students"]
            mis_cnt = r["misconception_count"] or 0
            
            # Công thức tính điểm nhiệt: heat_score = (misconceptions * 2.5) + (unique_students * 1.5) + q_cnt
            heat_score = round((mis_cnt * 2.5) + (stu_cnt * 1.5) + (q_cnt * 0.5), 1)
            confusion_rate = round((mis_cnt / q_cnt * 100), 1) if q_cnt > 0 else 0.0

            total_q += q_cnt
            total_mis += mis_cnt

            slides_stats.append({
                "slide_page": page,
                "question_count": q_cnt,
                "unique_students": stu_cnt,
                "misconception_count": mis_cnt,
                "confusion_rate": confusion_rate,
                "heat_score": heat_score,
                "status": "HOT" if heat_score >= 30 else ("WARM" if heat_score >= 15 else "COLD")
            })

        # Sắp xếp tìm Top 3 điểm nghẽn cao nhất
        top_bottlenecks = sorted(slides_stats, key=lambda x: x["heat_score"], reverse=True)[:3]
        top_3_pages = [s["slide_page"] for s in top_bottlenecks]

        conn.close()
        return json.dumps({
            "status": "SUCCESS",
            "lecture_code": lecture_code,
            "cohort": cohort,
            "total_questions": total_q,
            "total_misconceptions": total_mis,
            "top_3_bottleneck_slides": top_3_pages,
            "slides": slides_stats
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)}, ensure_ascii=False)


def execute_get_slide_evidence(
    lecture_code: str,
    slide_page: int,
    limit: int = 5
) -> str:
    """Trích xuất danh sách hội thoại học viên nguyên văn kèm Turn ID (Tool T02)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

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
                CASE WHEN intent = 'explicit_misconception' THEN 0 ELSE 1 END,
                asked_at_vn DESC
            LIMIT ?
            """,
            (lecture_code, slide_page, limit)
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
            "lecture_code": lecture_code,
            "slide_page": slide_page,
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


# ==============================================================================
# 3. ROUTER & DISPATCHER TRUNG CHUYỂN TOOL
# ==============================================================================

TOOL_ROUTER = {
    "get_slide_heatmap": execute_get_slide_heatmap,
    "get_slide_evidence": execute_get_slide_evidence,
    "get_slide_content": execute_get_slide_content,
    "draft_pedagogical_intervention": execute_draft_pedagogical_intervention,
    "approve_intervention": execute_approve_intervention
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
