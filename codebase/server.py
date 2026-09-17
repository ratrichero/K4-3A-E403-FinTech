"""
================================================================================
VLEARN CLASS CONFUSION COPILOT — BACKEND SERVER & CORE SERVICES
================================================================================
Tích hợp trực tiếp với Service Layer (tools.py) và cơ sở dữ liệu SQLite (vlearn.db).
Cung cấp REST API đầy đủ theo đặc tả docs/03-technical-design/04-api-tool-contracts.md:
  - GET  /api/heatmap     : Tính toán ma trận điểm nhiệt tất định (Tool T07)
  - GET  /api/evidence    : Lấy bằng chứng Turn ID sinh viên theo slide (Tool T02)
  - GET  /api/approved    : Lấy danh sách can thiệp giáo án đã duyệt từ SQLite
  - POST /api/chat        : Tư vấn sư phạm Copilot thời gian thực (Dual-Mode)
  - POST /api/draft       : Soạn bản nháp can thiệp sư phạm 2 phút (Tool T09)
  - POST /api/approve     : Phê duyệt can thiệp vào giáo án & băm SHA-256 (Tool T10)
  - GET  /*               : Phục vụ Web UI Cockpit (index.html, static assets)
================================================================================
"""

import os
import sys
import json
import functools
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Reconfigure stdout for UTF-8 logging on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure Provider and tools can be imported
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Provider.llm import get_llm
from Provider.config import get_settings
from prompts import (
    PEDAGOGICAL_COPILOT_SYSTEM_PROMPT,
    ROOT_CAUSE_REASONER_SYSTEM_PROMPT,
    INTERVENTION_DRAFTER_SYSTEM_PROMPT
)
from langchain_core.messages import SystemMessage, HumanMessage

# Import trực tiếp từ Service & Tool Layer (tools.py)
from tools import (
    execute_get_slide_heatmap,
    execute_get_slide_evidence,
    execute_get_slide_content,
    execute_draft_pedagogical_intervention,
    execute_approve_intervention,
    execute_get_filters_catalog,
    get_db_connection
)
from agent import execute_copilot_workflow

# Initialize LLM instance once
print("[Server] Initializing LLM Provider fallback chain...", flush=True)
try:
    llm_instance = get_llm()
    current_model = get_settings().model_name
    print(f"[Server] LLM Provider active: {current_model} (Ready for CP3)", flush=True)
except Exception as e:
    llm_instance = None
    print(f"[Server] Warning: Failed to pre-initialize LLM: {e}", flush=True)


class VLearnHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler serving static frontend and VLearn API services."""

    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for static files and REST APIs."""
        parsed = urllib.parse.urlparse(self.path)
        clean_path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        # 1. API: Lấy Ma trận Điểm nhiệt (Tool T07)
        if clean_path == "/api/heatmap":
            lesson = qs.get("lesson", qs.get("lecture_code", ["D02"]))[0]
            cohort = qs.get("cohort", ["all"])[0]
            course = qs.get("course", qs.get("course_id", [None]))[0]
            result_str = execute_get_slide_heatmap(lesson, cohort, course)
            self._send_json(200, json.loads(result_str))
            return

        # 2. API: Lấy Bằng chứng Turn ID học viên theo Slide (Tool T02)
        elif clean_path == "/api/evidence":
            lesson = qs.get("lesson", qs.get("lecture_code", ["D02"]))[0]
            slide = int(qs.get("slide", qs.get("slide_page", [18]))[0])
            limit = int(qs.get("limit", [5])[0])
            result_str = execute_get_slide_evidence(lesson, slide, limit)
            self._send_json(200, json.loads(result_str))
            return

        # 3. API: Lấy danh sách Can thiệp Giáo án đã phê duyệt từ SQLite
        elif clean_path == "/api/approved":
            lesson = qs.get("lesson", [None])[0]
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                if lesson:
                    cur.execute(
                        "SELECT * FROM curriculum_adaptations WHERE lecture_code = ? ORDER BY created_at DESC",
                        (lesson,)
                    )
                else:
                    cur.execute("SELECT * FROM curriculum_adaptations ORDER BY created_at DESC")
                rows = [dict(r) for r in cur.fetchall()]
                conn.close()
                self._send_json(200, {"status": "SUCCESS", "count": len(rows), "adaptations": rows})
                return
            except Exception as ex:
                self._send_json(500, {"status": "ERROR", "message": str(ex)})
        # 4. API: Lấy Danh mục Bộ lọc Phân cấp Chuẩn xác từ SQLite
        elif clean_path == "/api/filters":
            result_str = execute_get_filters_catalog()
            self._send_json(200, json.loads(result_str))
            return

        # 5. Phục vụ file tĩnh thông thường (index.html, CSS, JS)
        super().do_GET()

    def do_POST(self):
        """Handle POST requests for Copilot, Drafting, and Approval."""
        parsed = urllib.parse.urlparse(self.path)
        clean_path = parsed.path

        # 1. API: Copilot Chat Sư phạm Thời gian thực
        if clean_path == "/api/chat":
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            try:
                payload = json.loads(post_data.decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "Invalid JSON body"})
                return

            user_msg = payload.get("message", "").strip()
            slide = int(payload.get("slide", 18))
            lesson = payload.get("lesson", "D02")
            cohort = payload.get("cohort", "K4")
            course = payload.get("course", "COMP2010")

            try:
                print(f"[Server] Routing chat to LangGraph StateGraph (agent.py): '{user_msg[:50]}...'", flush=True)
                result = execute_copilot_workflow(
                    user_query=user_msg,
                    lesson_id=lesson,
                    slide_page=slide,
                    cohort=cohort,
                    course=course
                )
                self._send_json(200, result)
            except Exception as ex:
                print(f"[Server] Copilot workflow execution error: {ex}", flush=True)
                self._send_json(500, {
                    "status": "error",
                    "error": str(ex),
                    "reply": f"Xin lỗi Thầy/Cô, hệ thống gặp gián đoạn tạm thời khi phân tích: {ex}"
                })
            return

        # 2. API: Soạn Bản nháp Can thiệp 2 Phút (Tool T09)
        elif clean_path == "/api/draft":
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            try:
                payload = json.loads(post_data.decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "Invalid JSON body"})
                return

            draft_type = payload.get("type", "counter_analogy")
            slide = int(payload.get("slide", 18))
            lesson = payload.get("lesson", "D02")
            focus = payload.get("concept", None)

            # Gọi Tool T09 trong tools.py
            draft_res = execute_draft_pedagogical_intervention(
                lecture_code=lesson,
                slide_page=slide,
                intervention_type=draft_type,
                focus_concept=focus,
                use_llm=True
            )
            self._send_json(200, json.loads(draft_res))
            return

        # 3. API: Phê duyệt Can thiệp vào Giáo án & Băm SHA-256 (Tool T10 - HITL Gate)
        elif clean_path == "/api/approve":
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len)
            try:
                payload = json.loads(post_data.decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "Invalid JSON body"})
                return

            lesson = payload.get("lesson", payload.get("lecture_code", "D02"))
            slide = int(payload.get("slide", payload.get("slide_page", 18)))
            title = payload.get("title", "Can thiệp sư phạm")
            content = payload.get("content", payload.get("content_payload", ""))
            inter_type = payload.get("type", payload.get("intervention_type", "counter_analogy"))
            lecturer = payload.get("lecturer_id", payload.get("owner", "lec_cuongtv"))
            notes = payload.get("notes", "Đã duyệt vào kế hoạch giảng dạy")

            # Gọi Tool T10 ghi nhận vào SQLite và băm SHA-256
            approve_res = execute_approve_intervention(
                lecture_code=lesson,
                slide_page=slide,
                title=title,
                content_payload=content,
                intervention_type=inter_type,
                lecturer_id=lecturer,
                notes_for_class=notes
            )
            self._send_json(200, json.loads(approve_res))
            return

        # Default POST handler
        super().do_POST()


def run_server(port: int = 8080):
    """Start threaded HTTP server on specified port."""
    server_address = ("", port)
    ThreadingHTTPServer.allow_reuse_address = True
    handler_class = functools.partial(VLearnHandler, directory=BASE_DIR)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    current_model_name = get_settings().model_name
    print(f"\n========================================================", flush=True)
    print(f"  VLearn Class Confusion Copilot Server", flush=True)
    print(f"  Serving at http://localhost:{port}/index.html", flush=True)
    print(f"  LLM Provider: {current_model_name} (Ready for CP3)", flush=True)
    print(f"  Service Layer: tools.py (Integrated)", flush=True)
    print(f"========================================================\n", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down gracefully.", flush=True)
        httpd.shutdown()


if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
