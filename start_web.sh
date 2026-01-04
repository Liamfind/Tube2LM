#!/bin/bash
# Web 界面启动脚本

cd "$(dirname "$0")"

echo "=========================================="
echo "启动 YouTube 视频 URL 抓取工具 - Web 界面"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install flask || {
        echo "❌ Flask 安装失败，请手动运行：pip3 install flask"
        exit 1
    }
}

python3 -c "import yt_dlp" 2>/dev/null || {
    echo "⚠️  yt-dlp 未安装，正在安装..."
    echo "   如果遇到 SSL 证书错误，请先运行："
    echo "   /Applications/Python\\ 3.*/Install\\ Certificates.command"
    echo ""
    pip3 install yt-dlp || {
        echo "❌ yt-dlp 安装失败"
        echo "   如果是 SSL 证书错误，请先运行证书安装脚本："
        echo "   /Applications/Python\\ 3.*/Install\\ Certificates.command"
        exit 1
    }
}

# 启动服务器
echo ""
echo "正在启动服务器..."
echo "服务器启动后，请在浏览器中打开："
echo "  http://127.0.0.1:8080"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "=========================================="
echo ""

python3 web_app.py

