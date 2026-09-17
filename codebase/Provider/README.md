# 📦 LLMExtract — Module Cấu Hình & Tích Hợp LLM Provider Độc Lập

Module trích xuất dùng để đóng gói cấu hình và khởi tạo LLM Provider (LangChain Runnable), hỗ trợ **tự động chuyển đổi dự phòng (Multi-tier Fallbacks)**, tương thích hoàn toàn với OpenAI và mọi API chuẩn OpenAI-compatible (Groq, DeepSeek, OpenRouter, Ollama, vLLM, v.v.).

Bạn có thể dễ dàng sao chép thư mục này hoặc các file bên trong sang **bất kỳ dự án Python nào** (FastAPI, LangGraph, LangChain, Streamlit, Flask, CLI bot,...).

---

## 📂 Cấu trúc thư mục

```text
LLMExtract/
├── .env.example        # Mẫu biến môi trường đầy đủ (Primary, Fallbacks, Groq, DeepSeek, Ollama...)
├── config.py           # Quản lý cấu hình bằng Pydantic BaseSettings (tự động đọc .env)
├── llm.py              # Factory khởi tạo LLM (get_llm, create_chat_model) với cơ chế with_fallbacks
├── example_usage.py    # Script demo chạy thực tế (Sync, Async, Streaming)
├── requirements.txt    # Danh sách thư viện tối thiểu cần thiết
├── __init__.py         # Package entrypoint tiện lợi cho việc import
└── tests/
    ├── __init__.py
    └── test_llm.py     # Bộ unit test pytest kiểm tra cấu hình & cơ chế tự động fallback
```

---

## 🚀 Hướng dẫn nhanh (Quickstart)

### 1. Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### 2. Cấu hình file `.env`

Sao chép file `.env.example` thành `.env`:

```bash
cp .env.example .env
# Hoặc trên Windows PowerShell:
Copy-Item .env.example .env
```

Mở file `.env` và điền API key của bạn:

```env
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-4o-mini
LLM_TEMPERATURE=0.7
```

### 3. Chạy thử ví dụ

```bash
python example_usage.py
```

### 4. Chạy Unit Test

```bash
pytest tests/
```

---

## 💡 Hướng dẫn cấu hình các Provider phổ biến

Nhờ sử dụng giao thức chuẩn **OpenAI-Compatible**, bạn có thể dùng một interface duy nhất `ChatOpenAI` để kết nối tới nhiều dịch vụ khác nhau bằng cách thay đổi `OPENAI_BASE_URL` và `MODEL_NAME`:

| Provider | `OPENAI_BASE_URL` | `MODEL_NAME` gợi ý | Đặc điểm |
| :--- | :--- | :--- | :--- |
| **OpenAI (Mặc định)** | *(để trống)* | `gpt-4o-mini`, `gpt-4o` | Ổn định, thông minh, hỗ trợ đầy đủ tính năng |
| **Groq** | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` | Tốc độ cực nhanh, có gói miễn phí |
| **DeepSeek** | `https://api.deepseek.com/v1` | `deepseek-chat`, `deepseek-reasoner` | Chi phí rẻ, khả năng lập trình & suy luận xuất sắc |
| **OpenRouter** | `https://openrouter.ai/api/v1` | `anthropic/claude-3.5-sonnet`, `meta-llama/llama-3.1-8b-instruct` | Một API key duy nhất truy cập hơn 100+ models |
| **Ollama (Local)** | `http://localhost:11434/v1` | `llama3.2`, `mistral`, `qwen2.5` | Chạy trên máy tính cá nhân, 100% offline, miễn phí |
| **vLLM / LM Studio** | `http://localhost:8000/v1` | Tên model đã load trên server | Dành cho private server triển khai mã nguồn mở |

---

## 🛡️ Cơ chế Tự Động Chuyển Đổi Dự Phòng (Multi-tier Fallbacks)

Trong các ứng dụng production, API của nhà cung cấp chính có thể gặp sự cố:
- Hết hạn ngạch / Bị giới hạn tần suất gọi (**HTTP 429 Rate Limit**)
- Lỗi máy chủ (**HTTP 500, 502, 503 Server Error**)
- Mất kết nối mạng tạm thời (**Timeout / Connection Error**)

`LLMExtract` tích hợp sẵn phương thức `with_fallbacks(...)` của LangChain:

```
[User Request] 
      │
      ▼
┌──────────────┐     Thất bại (429 / 5xx)
│ Primary LLM  │ ─────────────────────────► ┌──────────────┐
│ (VD: OpenAI) │                            │ Fallback 1   │
└──────────────┘                            │ (VD:DeepSeek)│
      │ Thành công                          └──────────────┘
      ▼                                            │ Thất bại (429 / 5xx)
[Kết quả trả về]                                   ▼
      ▲                                     ┌──────────────┐
      └──────────────────────────────────── │ Fallback 2   │
                   Thành công               │ (VD: Groq)   │
                                            └──────────────┘
```

Chỉ cần cấu hình thêm trong `.env`:

```env
# Primary LLM
OPENAI_API_KEY=sk-primary-key
MODEL_NAME=gpt-4o-mini

# Fallback 1
FALLBACK_OPENAI_API_KEY=sk-deepseek-key
FALLBACK_OPENAI_BASE_URL=https://api.deepseek.com/v1
FALLBACK_MODEL_NAME=deepseek-chat

# Fallback 2
FALLBACK2_OPENAI_API_KEY=gsk_groq_key
FALLBACK2_OPENAI_BASE_URL=https://api.groq.com/openai/v1
FALLBACK2_MODEL_NAME=llama-3.3-70b-versatile
```

Khi gọi `get_llm()`, LangChain sẽ tự động bọc chuỗi fallback:
```python
from LLMExtract import get_llm

llm = get_llm()
# Tự động chuyển fallback khi primary gặp lỗi:
response = llm.invoke("Hello!")
```

---

## 🔌 Cách tích hợp vào dự án khác

### Cách 1: Sử dụng như một Package con trong dự án

1. Copy toàn bộ thư mục `LLMExtract/` vào thư mục gốc của dự án mới.
2. Thêm các dependencies từ `LLMExtract/requirements.txt` vào `requirements.txt` của dự án mới.
3. Thêm các biến cấu hình từ `LLMExtract/.env.example` vào `.env` của dự án mới.
4. Trong code Python của dự án mới, import và sử dụng:

```python
from LLMExtract import get_llm, get_settings

llm = get_llm()
response = llm.invoke("Câu hỏi của bạn...")
```

### Cách 2: Tích hợp vào cấu trúc `src/services` có sẵn

Nếu dự án của bạn có cấu trúc `src/services/` và `src/config.py`:
- Sao chép logic `LLMSettings` trong `LLMExtract/config.py` ghép vào `src/config.py`.
- Đặt file `llm.py` vào `src/services/llm.py`.
- Cập nhật dòng import trong `src/services/llm.py`:
  ```python
  from src.config import get_settings
  ```
