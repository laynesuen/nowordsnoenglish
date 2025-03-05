import openai
import requests
import os
from fastapi import FastAPI, UploadFile, File
from pydub import AudioSegment
from uuid import uuid4

# 配置 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your-elevenlabs-api-key")

# FastAPI 实例
app = FastAPI()

# 创建文件存储目录
os.makedirs("uploads", exist_ok=True)
os.makedirs("responses", exist_ok=True)

# 语音转文本（Whisper API）
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
    return response["text"]

# AI 生成智能回复（ChatGPT）
def chat_with_ai(user_input):
    prompt = f"""
    你是一个英语口语老师，帮助用户练习英语：
    1. 先回答用户的问题
    2. 如果语法错误，帮用户纠正
    3. 评分（流利度 / 准确度 / 词汇）
    
    用户：{user_input}
    AI：
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# AI 语音合成（ElevenLabs）
def text_to_speech(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "voice": "Rachel"}
    
    response = requests.post(url, json=data, headers=headers)
    audio_filename = f"responses/{uuid4()}.mp3"
    
    with open(audio_filename, "wb") as f:
        f.write(response.content)
    
    return audio_filename

# API 端点：上传用户语音
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # 保存用户上传的音频
    file_path = f"uploads/{uuid4()}.mp3"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 语音转文本
    transcript = transcribe_audio(file_path)

    # 生成 AI 回复
    ai_response = chat_with_ai(transcript)

    # AI 语音合成
    ai_audio = text_to_speech(ai_response)

    return {
        "transcript": transcript,
        "aiResponse": ai_response,
        "aiAudioUrl": ai_audio
    }

# 运行 FastAPI 服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
