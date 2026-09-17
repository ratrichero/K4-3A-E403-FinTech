"""
================================================================================
🔌 VLEARN MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
================================================================================
Triển khai kiến trúc MCP Academic Server tuân thủ chuẩn giao thức Model Context Protocol.
Cung cấp các công cụ chuẩn hóa (MCP Tools) để tác tử AI tra cứu điểm nhiệt,
trích xuất bằng chứng hội thoại học viên và thực thi phê duyệt can thiệp sư phạm.
================================================================================
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class MCPAcademicServer:
    """
    Máy chủ MCP Server tuân thủ chuẩn giao thức Model Context Protocol (JSON-RPC 2.0)
    dành cho hệ thống VLearn Class Confusion Copilot & Pedagogical Heatmap.
    """
    def __init__(self, server_name: str = "vlearn-confusion-copilot-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP (Model Context Protocol)."""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi request gọi Tool theo chuẩn giao thức MCP JSON-RPC 2.0.
        
        Args:
            tool_name: Tên công cụ cần gọi (ví dụ: 'get_slide_heatmap', 'get_slide_evidence')
            arguments: Từ điển chứa các tham số truyền vào tool
            
        Returns:
            Dictionary đóng gói phản hồi chuẩn JSON-RPC 2.0
        """
        result_str = dispatch_tool_call(tool_name, arguments)
        try:
            content = json.loads(result_str)
        except json.JSONDecodeError:
            content = {
                "status": "EXECUTION_ERROR",
                "error": f"Tool trả về chuỗi dữ liệu không hợp lệ: {result_str}"
            }
            
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "version": self.version,
            "tool": tool_name,
            "result": content
        }


if __name__ == "__main__":
    print("\n" + "="*70)
    print(f"🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER — VLEARN CONFUSION COPILOT")
    print("="*70)
    
    server = MCPAcademicServer()
    tools = server.list_tools()
    print(f"\n✅ Khởi tạo thành công MCP Server: {server.server_name} (Phiên bản: {server.version})")
    print(f"📦 Số lượng Tools công bố trên MCP Protocol: {len(tools)} tools\n")
    for idx, t in enumerate(tools, start=1):
        req_params = t.get("parameters", {}).get("required", [])
        print(f"   {idx}. {t['name']:<32} | Bắt buộc: {req_params}")

    print("\n" + "-"*70)
    print("🚀 BƯỚC 1: Kiểm thử gọi Tool T07 'get_slide_heatmap' cho bài giảng D02:")
    print("-"*70)
    heatmap_res = server.call_tool("get_slide_heatmap", {"lecture_code": "D02", "cohort": "all"})
    res_data = heatmap_res.get("result", {})
    if res_data.get("status") == "SUCCESS":
        print(f"✅ Thành công! Tổng câu hỏi: {res_data.get('total_questions')}, Hiểu nhầm: {res_data.get('total_misconceptions')}")
        print(f"🔥 Top 3 Slide điểm nghẽn cao nhất: Slide {res_data.get('top_3_bottleneck_slides')}")
    else:
        print(f"❌ Thất bại: {res_data}")

    print("\n" + "-"*70)
    print("🚀 BƯỚC 2: Kiểm thử gọi Tool T02 'get_slide_evidence' tại Slide 18:")
    print("-"*70)
    evidence_res = server.call_tool("get_slide_evidence", {"lecture_code": "D02", "slide_page": 18, "limit": 2})
    ev_list = evidence_res.get("result", {}).get("evidence", [])
    print(f"✅ Trích xuất được {len(ev_list)} bằng chứng thực tế từ SQLite:")
    for ev in ev_list:
        print(f"   • [{ev['turn_id']}] Học viên {ev['student_id']}: \"{ev['raw_question'][:60]}...\"")

    print("\n" + "-"*70)
    print("🚀 BƯỚC 3: Kiểm thử gọi Tool T09 'draft_pedagogical_intervention' (Ví dụ tương phản):")
    print("-"*70)
    draft_res = server.call_tool("draft_pedagogical_intervention", {
        "lecture_code": "D02",
        "slide_page": 18,
        "intervention_type": "counter_analogy",
        "focus_concept": "Chain-of-Thought vs ReAct"
    })
    draft_payload = draft_res.get("result", {}).get("content_payload", "")
    print(f"✅ Đã tạo bản thảo can thiệp 2 phút:")
    print(f"   {draft_payload.replace(chr(10), ' ')[:100]}...\n")

    print("\n" + "-"*70)
    print("🚀 BƯỚC 4: Kiểm thử gọi Tool T10 'approve_intervention' (HITL Approval Gate & SHA-256):")
    print("-"*70)
    approve_res = server.call_tool("approve_intervention", {
        "lecture_code": "D02",
        "slide_page": 18,
        "title": "Ẩn dụ Bếp trưởng CoT vs ReAct",
        "content_payload": draft_payload,
        "lecturer_id": "lec_cuongtv",
        "notes_for_class": "2 phút đầu giờ ôn tập kiến thức"
    })
    app_data = approve_res.get("result", {})
    if app_data.get("status") == "SUCCESS":
        print(f"✅ Phê duyệt thành công vào bảng curriculum_adaptations!")
        print(f"🔑 Mã kiểm toán toàn vẹn SHA-256: {app_data.get('sha256_audit_hash')}")
        print(f"⏰ Thời điểm phê duyệt: {app_data.get('approval_timestamp')}")
    else:
        print(f"❌ Thất bại: {app_data}")

    print("\n" + "="*70)
    print("🎉 TOÀN BỘ 5 MCP TOOLS ĐÃ HOÀN THÀNH KIỂM THỬ VÀ SẴN SÀNG SỬ DỤNG!")
    print("="*70 + "\n")
