# 🌐 在线使用指南

本工具支持多种在线使用方式，无需在本地安装！

## 🎯 推荐方式：GitHub Codespaces（最简单）

### ✨ 优势
- ✅ **零配置**：点击按钮即可使用
- ✅ **浏览器运行**：无需安装任何软件
- ✅ **自动安装依赖**：环境自动配置
- ✅ **免费使用**：GitHub 提供免费额度

### 📋 使用步骤

1. **访问仓库**
   - 打开：https://github.com/Liamfind/Tube2LM

2. **启动 Codespace**
   - 点击绿色的 **"Code"** 按钮
   - 选择 **"Codespaces"** 标签
   - 点击 **"Create codespace on main"**
   - 等待启动（约 1-2 分钟）

3. **运行工具**
   ```bash
   # Codespace 启动后，在终端中运行：
   python3 web_app.py
   ```

4. **访问 Web 界面**
   - 点击终端中出现的 **"Open in Browser"** 链接
   - 或访问 Codespace 提供的端口转发 URL

5. **开始使用**
   - 在网页中输入 YouTube 频道 URL
   - 点击"开始抓取"
   - 等待完成并下载结果

### 🎬 视频教程（文字版）

```
1. 访问 GitHub 仓库
   ↓
2. 点击 "Code" → "Codespaces" → "Create codespace"
   ↓
3. 等待环境启动（自动安装依赖）
   ↓
4. 运行：python3 web_app.py
   ↓
5. 点击 "Open in Browser" 链接
   ↓
6. 使用 Web 界面抓取视频
```

## 🔄 其他在线部署方式

### 方式二：部署到 Google Cloud Run（推荐用于长期使用）

Google Cloud Run 提供免费额度，可以部署为永久在线服务。

#### 快速部署步骤：

1. **安装 Google Cloud SDK**
   ```bash
   # macOS
   brew install --cask google-cloud-sdk
   
   # 或访问：https://cloud.google.com/sdk/docs/install
   ```

2. **初始化并部署**
   ```bash
   gcloud auth login
   gcloud projects create tube2lm-project
   gcloud config set project tube2lm-project
   
   # 构建并部署
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tube2lm
   gcloud run deploy tube2lm \
     --image gcr.io/YOUR_PROJECT_ID/tube2lm \
     --platform managed \
     --region asia-east1 \
     --allow-unauthenticated
   ```

详细步骤请查看：[Google Cloud 部署指南](GOOGLE_CLOUD_DEPLOY.md)

### 方式三：部署到 Railway（推荐用于长期使用）

Railway 提供免费额度，可以部署为永久在线服务。

#### 步骤：

1. **创建 Railway 账户**
   - 访问：https://railway.app
   - 使用 GitHub 账户登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择 `Liamfind/Tube2LM` 仓库

3. **配置环境**
   - Railway 会自动检测 Python 项目
   - 自动运行 `pip install -r requirements.txt`

4. **设置启动命令**
   - 在 Settings → Deploy 中设置：
   ```
   Start Command: python3 web_app.py
   ```

5. **获取访问链接**
   - Railway 会自动分配一个 URL
   - 例如：`https://tube2lm.railway.app`

#### 需要创建的文件：

创建 `Procfile`（用于 Railway）：
```
web: python3 web_app.py
```

### 方式三：部署到 Render

类似 Railway，也是免费的云服务。

### 方式四：部署到 Heroku

需要信用卡验证，但有免费额度。

## 📊 方案对比

| 方案 | 难度 | 费用 | 适用场景 |
|------|------|------|----------|
| **GitHub Codespaces** | ⭐ 简单 | 免费（有额度） | 临时使用、测试 |
| **Google Cloud Run** | ⭐⭐ 中等 | 免费（有额度） | 长期在线服务，推荐 |
| **Railway** | ⭐⭐ 中等 | 免费（有额度） | 长期在线服务 |
| **Render** | ⭐⭐ 中等 | 免费（有额度） | 长期在线服务 |
| **Heroku** | ⭐⭐⭐ 复杂 | 免费（需信用卡） | 企业级应用 |

## 🎯 推荐选择

- **临时使用/测试**：使用 GitHub Codespaces
- **长期在线服务**：使用 **Google Cloud Run**（推荐）或 Railway/Render
- **本地使用**：下载到本地运行

## 📝 注意事项

### GitHub Codespaces
- 每月 60 小时免费额度
- 30 分钟无活动会自动停止
- 数据保存在 Codespace 中

### Railway/Render
- 需要配置环境变量（如果有）
- 可能需要修改端口配置
- 免费额度有限制

## 🔧 如果需要修改配置

### 修改端口（用于 Railway/Render）

编辑 `web_app.py`，修改最后几行：

```python
# 原代码
app.run(debug=False, host='127.0.0.1', port=8080)

# 修改为（Railway/Render）
import os
port = int(os.environ.get('PORT', 8080))
app.run(debug=False, host='0.0.0.0', port=port)
```

## 🚀 快速开始

**推荐新手使用 GitHub Codespaces**，只需：
1. 访问仓库
2. 点击 "Code" → "Codespaces" → "Create codespace"
3. 运行 `python3 web_app.py`
4. 点击链接访问

就这么简单！

---

**提示**：如果遇到问题，可以在 [GitHub Issues](https://github.com/Liamfind/Tube2LM/issues) 中提问。

