# AI 语音聊天 API
这是一个基于 FastAPI 的 AI 语音聊天 API，支持：
- 语音识别（Whisper API）
- AI 对话（ChatGPT-4）
- AI 语音合成（ElevenLabs）

## 🚀 如何运行
### 1. 本地运行
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000