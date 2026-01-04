# 如何从 GitHub 使用这个工具

## 📌 重要说明

**这个工具需要在本地运行，不能直接在 GitHub 网页上使用。**

GitHub 只是代码仓库，你需要：
1. 下载代码到本地
2. 安装 Python 和依赖
3. 在本地运行工具

## 🚀 完整使用流程

### 步骤 1：访问 GitHub 仓库

打开浏览器，访问：**https://github.com/Liamfind/Tube2LM**

### 步骤 2：下载代码

有两种方式：

#### 方式 A：使用 Git（推荐）

如果你已经安装了 Git：

```bash
# 在终端中执行
git clone https://github.com/Liamfind/Tube2LM.git
cd Tube2LM
```

#### 方式 B：下载 ZIP 文件

1. 在 GitHub 仓库页面，点击绿色的 **"Code"** 按钮
2. 选择 **"Download ZIP"**
3. 下载完成后，解压 ZIP 文件
4. 进入解压后的 `Tube2LM` 文件夹

### 步骤 3：安装 Python

如果还没有安装 Python：

- **macOS**: 访问 https://www.python.org/downloads/ 下载安装
- **Windows**: 访问 https://www.python.org/downloads/ 下载安装（安装时勾选 "Add Python to PATH"）

验证安装：
```bash
python3 --version
# 应该显示 Python 3.8 或更高版本
```

### 步骤 4：安装依赖

在项目目录下执行：

```bash
# macOS/Linux
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt
```

### 步骤 5：运行工具

#### 使用 Web 界面（推荐）

```bash
# 启动 Web 服务器
python3 web_app.py
```

然后在浏览器中打开：**http://127.0.0.1:8080**

#### 使用命令行

1. 编辑 `main.py`，填入频道 URL
2. 运行：
   ```bash
   python3 main.py
   ```

## 📋 快速检查清单

- [ ] 已从 GitHub 下载代码
- [ ] 已安装 Python 3.8+
- [ ] 已安装依赖库（`pip install -r requirements.txt`）
- [ ] 已进入项目目录
- [ ] 已运行 `python3 web_app.py` 或 `python3 main.py`

## ❓ 常见问题

### Q: 为什么不能在 GitHub 网页上直接使用？

**A**: 这是一个 Python 应用程序，需要：
- 在本地安装 Python 环境
- 安装依赖库（yt-dlp, Flask 等）
- 运行 Python 代码

GitHub 只是代码托管平台，不提供运行环境。

### Q: 有没有在线版本？

**A**: 目前没有。如果你需要在线版本，可以考虑：
- 部署到云服务器（如 Heroku, Vercel, Railway 等）
- 使用 GitHub Codespaces（需要配置）

### Q: 如何更新到最新版本？

**A**: 如果使用 Git 克隆：
```bash
cd Tube2LM
git pull
```

如果使用 ZIP 下载，需要重新下载最新版本。

## 🎯 使用示例

### 示例 1：使用 Web 界面

```bash
# 1. 进入项目目录
cd Tube2LM

# 2. 启动 Web 服务器
python3 web_app.py

# 3. 打开浏览器访问 http://127.0.0.1:8080
# 4. 在网页中输入频道 URL，点击"开始抓取"
# 5. 等待完成，下载 Excel 文件
```

### 示例 2：使用命令行

```bash
# 1. 编辑 main.py，填入频道 URL
# CHANNEL_URL = "https://www.youtube.com/@频道名/videos"

# 2. 运行
python3 main.py

# 3. 结果保存在 output/ 目录
```

## 📚 更多帮助

- 详细使用说明：查看 [README.md](README.md)
- 常见问题：查看 [FAQ.md](FAQ.md)
- 文件存储说明：查看 [STORAGE_INFO.md](STORAGE_INFO.md)

---

**提示**：如果遇到问题，可以在 [GitHub Issues](https://github.com/Liamfind/Tube2LM/issues) 中提问。

