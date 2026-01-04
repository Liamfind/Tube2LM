# Google Cloud 快速部署指南

## 🚀 5 分钟快速部署

### 前置要求

1. Google 账户
2. 安装 Google Cloud SDK（可选，也可以使用网页界面）

### 方法一：使用命令行（推荐）

#### 步骤 1：安装 Google Cloud SDK

**macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Windows/Linux:**
访问：https://cloud.google.com/sdk/docs/install

#### 步骤 2：登录和初始化

```bash
# 登录 Google Cloud
gcloud auth login

# 创建新项目（或使用现有项目）
gcloud projects create tube2lm-project --name="Tube2LM"

# 设置当前项目
gcloud config set project tube2lm-project

# 启用必要的 API
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### 步骤 3：构建和部署

```bash
# 进入项目目录
cd Tube2LM

# 构建 Docker 镜像并部署（一条命令完成）
gcloud run deploy tube2lm \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300
```

**说明：**
- `--source .`：自动构建 Docker 镜像（使用当前目录的 Dockerfile）
- `--region asia-east1`：选择区域（可选：us-central1, us-east1, europe-west1）
- `--allow-unauthenticated`：允许公开访问
- `--memory 1Gi`：内存限制
- `--timeout 300`：请求超时时间（秒）

#### 步骤 4：获取访问 URL

部署完成后，会显示服务 URL：
```
Service URL: https://tube2lm-xxxxx-xx.a.run.app
```

### 方法二：使用 Google Cloud Console（网页界面）

#### 步骤 1：访问 Cloud Run

1. 访问：https://console.cloud.google.com/run
2. 选择或创建项目

#### 步骤 2：创建服务

1. 点击 **"Create Service"**
2. 选择 **"Deploy one revision from a source repository"**
3. 连接 GitHub 仓库：`Liamfind/Tube2LM`
4. 配置：
   - **Service name**: `tube2lm`
   - **Region**: `asia-east1`
   - **Authentication**: `Allow unauthenticated invocations`
   - **Memory**: `1 GiB`
   - **CPU**: `1`
   - **Timeout**: `300 seconds`

#### 步骤 3：部署

1. 点击 **"Create"**
2. 等待部署完成（约 5-10 分钟）
3. 获取服务 URL

## 📝 部署后验证

### 1. 访问服务

在浏览器中打开服务 URL，应该能看到 Web 界面。

### 2. 测试功能

1. 输入一个 YouTube 频道 URL
2. 点击"开始抓取"
3. 等待完成并下载结果

### 3. 查看日志

```bash
# 查看实时日志
gcloud run services logs read tube2lm --region asia-east1 --limit 50
```

## 🔄 更新部署

### 更新代码后重新部署

```bash
# 方法一：使用 --source（自动构建）
gcloud run deploy tube2lm \
  --source . \
  --region asia-east1

# 方法二：手动构建
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tube2lm
gcloud run deploy tube2lm \
  --image gcr.io/YOUR_PROJECT_ID/tube2lm \
  --region asia-east1
```

## 💰 费用

### 免费额度（每月）

- ✅ **200 万次请求**
- ✅ **180,000 vCPU 秒**
- ✅ **360,000 GiB 秒内存**
- ✅ **1 GB 出站流量**

### 典型使用

- **轻度使用**（每天 10 次）：**完全免费**
- **中度使用**（每天 100 次）：约 **$5-10/月**
- **重度使用**（每天 1000 次）：约 **$50-100/月**

## ⚙️ 配置优化

### 增加资源（如果抓取大量视频）

```bash
gcloud run services update tube2lm \
  --memory 2Gi \
  --cpu 2 \
  --timeout 600 \
  --region asia-east1
```

### 设置最小实例数（避免冷启动）

```bash
gcloud run services update tube2lm \
  --min-instances 1 \
  --region asia-east1
```

**注意**：设置最小实例数会增加费用。

## 🛠️ 故障排查

### 部署失败

```bash
# 查看构建日志
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

### 服务无法访问

1. 检查是否设置了 `--allow-unauthenticated`
2. 查看服务日志
3. 检查防火墙规则

### 内存不足

```bash
gcloud run services update tube2lm \
  --memory 2Gi \
  --region asia-east1
```

## 📚 更多信息

详细部署指南请查看：[GOOGLE_CLOUD_DEPLOY.md](GOOGLE_CLOUD_DEPLOY.md)

---

**提示**：首次部署可能需要 5-10 分钟。部署成功后，你的工具就可以通过 HTTPS URL 访问了！

