# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（yt-dlp 可能需要）
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p output logs uploads

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 暴露端口（Cloud Run 会使用 PORT 环境变量）
EXPOSE 8080

# 启动命令
# 使用 gunicorn 作为生产服务器（推荐）
# 如果需要使用 Flask 开发服务器，可以使用：CMD ["python3", "web_app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "300", "web_app:app"]

