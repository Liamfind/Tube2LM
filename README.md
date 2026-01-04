# YouTube 视频 URL 抓取工具

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-red.svg)

这是一个简单易用的 YouTube 频道视频链接抓取工具，可以快速获取指定频道最新发布的 200-300 条视频链接。

## ✨ 特性

- 🚀 **极速抓取**：8-10 秒即可抓取 300 条视频链接
- 🌐 **Web 界面**：美观易用的浏览器界面，无需命令行操作
- 💻 **命令行支持**：也支持命令行模式，方便集成到其他脚本
- 📊 **多种输出格式**：支持 TXT 和 Excel 格式
- 🔄 **自动排序**：严格按照发布时间从近到远排序
- 🛡️ **稳定可靠**：使用 yt-dlp，绕过 YouTube 反爬虫机制
- 🔍 **智能排重**：支持上传已抓取的 Excel 文件，自动排除重复视频


## 🚀 快速开始

### 方式一：从 GitHub 克隆（推荐）

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/youtube-url-scraper.git

# 进入项目目录
cd youtube-url-scraper
```

### 方式二：直接下载

1. 访问 GitHub 仓库页面
2. 点击 "Code" → "Download ZIP"
3. 解压到本地目录

### 安装步骤

#### 第一步：安装 Python

如果你还没有安装 Python，请按照以下步骤操作：

#### macOS 用户：
1. 打开终端（Terminal）
2. 检查是否已安装 Python：
   ```bash
   python3 --version
   ```
3. 如果没有安装，访问 [Python 官网](https://www.python.org/downloads/) 下载并安装 Python 3.8 或更高版本

#### Windows 用户：
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.8 或更高版本
3. 安装时**务必勾选** "Add Python to PATH" 选项

#### 第二步：安装依赖库

1. 打开终端（macOS）或命令提示符（Windows）
2. 进入项目目录（如果使用方式一克隆，目录名是 `youtube-url-scraper`）
3. 安装所需的库：
   ```bash
   pip3 install -r requirements.txt
   ```
   
   如果 `pip3` 命令不工作，可以尝试：
   ```bash
   python3 -m pip install -r requirements.txt
   ```
   
   或者在 Windows 上：
   ```bash
   pip install -r requirements.txt
   ```

#### 第三步：配置频道 URL（仅命令行模式需要）

1. 用文本编辑器打开 `main.py` 文件
2. 找到这一行：
   ```python
   CHANNEL_URL = "https://www.youtube.com/@example/videos"
   ```
3. 将 `@example` 替换为你要抓取的频道名称，例如：
   ```python
   CHANNEL_URL = "https://www.youtube.com/@MrBeast/videos"
   ```
   
   **支持的 URL 格式：**
   - `https://www.youtube.com/@频道名/videos`
   - `https://www.youtube.com/channel/频道ID/videos`
   - `https://www.youtube.com/c/频道名/videos`
   - `https://www.youtube.com/user/用户名/videos`

#### 第四步：运行工具

#### 方式一：使用 Web 界面（推荐，更简单）

1. 在终端中执行：
   ```bash
   python3 web_app.py
   ```
   
   或者在 Windows 上：
   ```bash
   python web_app.py
   ```

2. 打开浏览器，访问：`http://127.0.0.1:8080` 或 `http://localhost:8080`

3. 在网页中输入频道 URL
   - **可选**：上传已抓取的 Excel 文件进行排重（新抓取将自动排除已存在的视频）
4. 点击"开始抓取"按钮

5. 等待抓取完成，可以直接在网页上下载结果文件

#### 方式二：使用命令行

1. 用文本编辑器打开 `main.py` 文件
2. 找到这一行并填入频道 URL：
   ```python
   CHANNEL_URL = "https://www.youtube.com/@你的频道名/videos"
   ```
3. **可选**：如果需要排重，设置排重文件路径：
   ```python
   EXCLUDE_FILE = "/path/to/existing_videos.xlsx"  # 已抓取的 Excel 文件路径
   ```
   如果不需要排重，保持为 `None`：
   ```python
   EXCLUDE_FILE = None
   ```
4. 在终端中执行：
   ```bash
   python3 main.py
   ```
   
   或者在 Windows 上：
   ```bash
   python main.py
   ```

## 📁 项目结构

```
youtube-url-scraper/
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── config.py           # 配置文件
│   └── logger.py            # 日志模块
├── modules/                 # 功能模块
│   └── youtube/            # YouTube 抓取模块
│       ├── __init__.py
│       └── scraper.py      # 抓取逻辑
├── templates/               # Web 界面模板
│   └── index.html          # 前端页面
├── output/                  # 输出目录（自动生成）
│   └── urls_snapshot_*.txt # 抓取结果文件
├── logs/                    # 日志目录（自动生成）
├── main.py                  # 命令行入口文件
├── web_app.py              # Web 界面入口文件
├── start_web.sh            # Web 界面启动脚本（macOS/Linux）
├── requirements.txt         # 依赖清单
├── LICENSE                 # MIT 许可证
├── README.md               # 本文件
├── GITHUB_PUBLISH.md       # GitHub 发布指南
├── 使用说明.md             # 详细使用说明
├── 性能说明.md             # 性能相关说明
└── 抓取方式说明.md         # 技术实现说明
```

## 📤 输出结果

抓取完成后，结果会保存在 `output/` 目录下，文件名格式为：
```
频道名_20231215_143022.xlsx  # Excel 格式（默认）
频道名_20231215_143022.txt   # TXT 格式（可选）
```

**Excel 格式**包含以下列：
- `URL`: 视频完整 URL
- `发布时间`: 视频上传日期（格式：YYYYMMDD）
- `视频ID`: YouTube 视频 ID

**TXT 格式**为每行一个视频 URL，例如：
```
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/watch?v=def456
https://www.youtube.com/watch?v=ghi789
...
```

> **💡 存储说明**：所有输出文件只保存在本地 `output/` 目录，不会提交到 GitHub。详细说明请参考 [文件存储说明](STORAGE_INFO.md)。

## 🔍 排重功能

### 使用场景
当你需要定期更新视频列表时，可以使用排重功能避免重复抓取已存在的视频。

### 使用方法

#### Web 界面
1. 在"排重文件（可选）"字段中，点击"选择文件"
2. 选择之前抓取的 Excel 文件（`.xlsx` 或 `.xls` 格式）
3. 输入频道 URL 并开始抓取
4. 系统会自动排除已存在的视频

#### 命令行
在 `main.py` 中设置 `EXCLUDE_FILE` 变量：
```python
EXCLUDE_FILE = "/path/to/existing_videos.xlsx"
```

### 排重原理
- 系统会从上传的 Excel 文件中提取视频 ID
- 支持从 `url` 列或 `video_id` 列提取
- 新抓取时会自动跳过这些已存在的视频
- 日志中会显示排除了多少条重复视频

## ⚙️ 配置说明

### 修改抓取数量

如果你想修改抓取的视频数量，可以编辑 `core/config.py` 文件：

```python
YOUTUBE_CONFIG = {
    "max_videos": 300,  # 最多抓取 300 条
    "min_videos": 200,  # 最少抓取 200 条
}
```

### 查看日志

程序运行时会自动生成日志文件，保存在 `logs/` 目录下，方便排查问题。

## ❓ 常见问题

### Q1: 提示 "请先在 main.py 中配置 CHANNEL_URL 变量"
**A:** 请确保在 `main.py` 中正确填写了频道 URL，并且 URL 中不包含 "example" 字样。

### Q2: 抓取失败或返回 0 条链接
**A:** 请检查：
- 频道 URL 是否正确
- 网络连接是否正常
- 频道是否为公开频道（私有频道无法抓取）

### Q3: 安装依赖时提示 "command not found"
**A:** 请确保：
- Python 已正确安装
- 已将 Python 添加到系统 PATH 环境变量
- 使用 `python3` 和 `pip3` 命令（macOS/Linux）

### Q4: 抓取速度慢
**A:** 本工具已配置为极速模式（只提取链接，不下载视频），如果仍然较慢，可能是：
- 网络连接问题
- 频道视频数量过多
- YouTube 服务器响应慢

## 🔧 技术说明

- **抓取库**: 使用 `yt-dlp`（YouTube-DL 的增强版）
- **排序逻辑**: YouTube 频道的上传列表默认按时间从近到远排序，本工具直接使用该顺序
- **极速模式**: 配置 `extract_flat=True`，只提取元数据，不下载视频文件

## 🤝 贡献

欢迎贡献代码！如果你发现 bug 或有新功能建议，请：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

或者直接提交 [Issue](https://github.com/YOUR_USERNAME/youtube-url-scraper/issues) 报告问题。

## 📝 更新日志

### v1.0.0 (2024-12-15)
- ✨ 初始版本发布
- ✅ 支持 YouTube 频道视频链接抓取
- ✅ Web 界面支持
- ✅ 命令行界面支持
- ✅ 支持多种 URL 格式
- ✅ 自动排序（从新到旧）
- ✅ 极速模式（8-10 秒抓取 300 条）

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

---

## 📚 相关文档

- [使用说明](使用说明.md) - 详细的使用文档
- [性能说明](性能说明.md) - 性能优化相关说明
- [抓取方式说明](抓取方式说明.md) - 技术实现细节
- [文件存储说明](STORAGE_INFO.md) - 输出文件存储方式和 GitHub 处理说明
- [常见问题](FAQ.md) - 常见问题解答（包括文件存储相关问题）
- [GitHub 发布指南](GITHUB_PUBLISH.md) - 如何发布到 GitHub

## ⚠️ 免责声明

本工具仅供学习和研究使用。使用本工具时，请遵守 YouTube 的服务条款和相关法律法规。作者不对使用本工具产生的任何后果负责。

---

**提示**: 如果遇到任何问题，请查看 `logs/` 目录下的日志文件，或检查终端输出的错误信息。你也可以在 [GitHub Issues](https://github.com/YOUR_USERNAME/youtube-url-scraper/issues) 中报告问题。

