# 使用官方 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录的所有文件到容器内
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行 FastAPI 服务器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]