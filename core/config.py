"""
核心配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 输出目录
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 日志配置
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# YouTube 抓取配置
YOUTUBE_CONFIG = {
    "max_videos": 300,  # 默认抓取最新 300 条视频（从新到旧排序）
    "min_videos": 200,  # 最少抓取 200 条
    "extract_flat": True,  # 只提取元数据，不下载视频（极速模式）
}

