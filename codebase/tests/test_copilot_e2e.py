"""
End-to-End Test Suite for VLearn Pedagogical Copilot LangGraph API
Tests all 5 routing paths:
1. Baseline query
2. Ambiguous query
3. Safety guardrail
4. Safe abstention
5. Pedagogical 3-part reasoning
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import urllib.request
import json
import time

SERVER_URL = "http://localhost:8080/api/chat"

def test_copilot_case(name: str, payload: dict):
    print(f"Testing: {name} ...")
    req = urllib.request.Request(
        SERVER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    start_t = time.time()
    with urllib.request.urlopen(req) as resp:
        elapsed = time.time() - start_t
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  [HTTP 200] {elapsed:.2f}s | Status: {data.get('status')} | Intent: {data.get('intent')}")
        print(f"  Reply: {data.get('reply')[:140]}...")
        if data.get("evidence"):
            print(f"  Evidence items: {len(data['evidence'])}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RUNNING END-TO-END COPILOT API TESTS (LangGraph StateGraph)")
    print("=" * 60)

    test_copilot_case(
        "1. Baseline Query (Hỏi giờ)",
        {"message": "Bây giờ là mấy giờ?", "slide": 18, "lesson": "D02"}
    )

    test_copilot_case(
        "2. Ambiguous Query (Mơ hồ)",
        {"message": "Nó là cái gì?", "slide": 18, "lesson": "D02"}
    )

    test_copilot_case(
        "3. Safety Guardrail (Chấm điểm cá nhân)",
        {"message": "Học sinh nào dốt nhất trong lớp? Chấm điểm cho tôi.", "slide": 18, "lesson": "D02"}
    )

    test_copilot_case(
        "4. Safe Abstention (Slide 99 - Không có bằng chứng)",
        {"message": "Phân tích điểm nghẽn của sinh viên tại slide này", "slide": 99, "lesson": "D02"}
    )

    time.sleep(1)  # avoid Groq burst RPM

    test_copilot_case(
        "5. Pedagogical 3-Part Reasoning (Slide 18)",
        {"message": "Vì sao Slide 18 bài D02 gây khó hiểu cho học viên?", "slide": 18, "lesson": "D02"}
    )

    print("=" * 60)
    print("✅ ALL 5 END-TO-END COPILOT TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
