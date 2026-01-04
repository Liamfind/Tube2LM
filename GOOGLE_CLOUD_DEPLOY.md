# Google Cloud 部署指南

本指南将帮助你将这个 YouTube 视频 URL 抓取工具部署到 Google Cloud。

## 🎯 推荐方案：Google Cloud Run

**为什么选择 Cloud Run？**
- ✅ **无服务器**：按使用付费，不用不花钱
- ✅ **自动扩缩容**：根据流量自动调整
- ✅ **免费额度**：每月 200 万请求免费
- ✅ **容器化部署**：使用 Docker，环境一致
- ✅ **HTTPS 自动配置**：自动提供 SSL 证书

## 📋 部署前准备

### 1. 安装 Google Cloud SDK

#### macOS:
```bash
# 使用 Homebrew 安装
brew install --cask google-cloud-sdk

# 或下载安装包
# https://cloud.google.com/sdk/docs/install
```

#### Windows:
下载并安装：https://cloud.google.com/sdk/docs/install

### 2. 初始化 Google Cloud

```bash
# 登录
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

### 3. 配置 Docker 认证

```bash
# 配置 Docker 使用 gcloud 作为凭证助手
gcloud auth configure-docker
```

## 🚀 部署步骤

### 方法一：使用 gcloud 命令行快速部署（最简单）

```bash
# 进入项目目录
cd Tube2LM

# 一条命令完成构建和部署
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
- `--source .`：自动使用 Dockerfile 构建镜像
- 无需手动构建和推送镜像
- 最简单快捷的方式

### 方法二：使用 gcloud 命令行（分步操作）

#### 步骤 1：构建并推送镜像

```bash
# 进入项目目录
cd Tube2LM

# 构建 Docker 镜像
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tube2lm

# 替换 YOUR_PROJECT_ID 为你的实际项目 ID
```

#### 步骤 2：部署到 Cloud Run

```bash
# 部署服务
gcloud run deploy tube2lm \
  --image gcr.io/YOUR_PROJECT_ID/tube2lm \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10
```

**参数说明：**
- `--region asia-east1`: 选择离你最近的区域（可选：us-central1, us-east1, europe-west1 等）
- `--allow-unauthenticated`: 允许公开访问（无需登录）
- `--memory 1Gi`: 内存限制（抓取大量视频可能需要更多）
- `--cpu 1`: CPU 核心数
- `--timeout 300`: 请求超时时间（秒），抓取可能需要较长时间
- `--max-instances 10`: 最大实例数

#### 步骤 3：获取访问 URL

部署完成后，会显示服务 URL，例如：
```
Service URL: https://tube2lm-xxxxx-xx.a.run.app
```

### 方法二：使用 Cloud Build（自动化部署）

#### 步骤 1：推送代码到 GitHub

确保代码已推送到 GitHub 仓库。

#### 步骤 2：配置 Cloud Build

1. 在 Google Cloud Console 中，进入 **Cloud Build** → **Triggers**
2. 点击 **Create Trigger**
3. 连接你的 GitHub 仓库
4. 配置触发条件（例如：推送到 main 分支）
5. 构建配置选择 `cloudbuild.yaml`

#### 步骤 3：自动部署

每次推送到 main 分支时，Cloud Build 会自动：
1. 构建 Docker 镜像
2. 推送到 Container Registry
3. 部署到 Cloud Run

## 🔧 配置优化

### 增加内存和超时时间

如果抓取大量视频，可能需要更多资源：

```bash
gcloud run services update tube2lm \
  --memory 2Gi \
  --cpu 2 \
  --timeout 600 \
  --region asia-east1
```

### 设置环境变量

如果需要配置特定设置：

```bash
gcloud run services update tube2lm \
  --set-env-vars "MAX_VIDEOS=300,MIN_VIDEOS=200" \
  --region asia-east1
```

### 配置自定义域名

1. 在 Cloud Run 服务中，点击 **Manage Custom Domains**
2. 添加你的域名
3. 按照提示配置 DNS

## 💰 费用估算

### Cloud Run 免费额度（每月）

- **请求数**：200 万次
- **CPU 时间**：180,000 vCPU 秒
- **内存**：360,000 GiB 秒
- **出站流量**：1 GB

### 典型使用场景

- **轻度使用**（每天 10 次抓取）：**完全免费**
- **中度使用**（每天 100 次抓取）：约 **$5-10/月**
- **重度使用**（每天 1000 次抓取）：约 **$50-100/月**

## 📝 验证部署

### 1. 检查服务状态

```bash
gcloud run services describe tube2lm --region asia-east1
```

### 2. 测试访问

在浏览器中打开服务 URL，应该能看到 Web 界面。

### 3. 查看日志

```bash
# 查看实时日志
gcloud run services logs read tube2lm --region asia-east1 --limit 50

# 或访问 Cloud Console
# https://console.cloud.google.com/run
```

## 🔄 更新部署

### 更新代码后重新部署

```bash
# 方法一：重新构建和部署
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tube2lm
gcloud run deploy tube2lm \
  --image gcr.io/YOUR_PROJECT_ID/tube2lm \
  --region asia-east1

# 方法二：如果使用 Cloud Build，直接推送代码到 GitHub
git push origin main
```

## 🛠️ 故障排查

### 问题 1：部署失败

**检查：**
```bash
# 查看构建日志
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

### 问题 2：服务无法访问

**检查：**
- 确认 `--allow-unauthenticated` 已设置
- 检查防火墙规则
- 查看服务日志

### 问题 3：内存不足

**解决：**
```bash
gcloud run services update tube2lm \
  --memory 2Gi \
  --region asia-east1
```

### 问题 4：超时错误

**解决：**
```bash
gcloud run services update tube2lm \
  --timeout 600 \
  --region asia-east1
```

## 🔐 安全建议

### 1. 限制访问（可选）

如果需要限制访问，可以移除 `--allow-unauthenticated`：

```bash
gcloud run services update tube2lm \
  --no-allow-unauthenticated \
  --region asia-east1
```

然后使用 IAM 控制访问权限。

### 2. 设置请求限制

在 Cloud Run 中配置：
- 最大并发请求数
- 最大实例数
- 最小实例数（保持服务常驻）

## 📊 监控和日志

### 查看指标

1. 访问 Cloud Console
2. 进入 **Cloud Run** → **tube2lm** → **Metrics**
3. 查看请求数、延迟、错误率等

### 设置告警

1. 在 Cloud Console 中，进入 **Monitoring** → **Alerting**
2. 创建告警策略
3. 设置条件（例如：错误率 > 5%）

## 🎯 备选方案：App Engine

如果不想使用容器，也可以使用 App Engine：

```bash
# 部署到 App Engine
gcloud app deploy app.yaml

# 查看应用
gcloud app browse
```

**注意**：App Engine 需要修改 `web_app.py` 以适配 App Engine 的 WSGI 服务器。

## 📚 相关资源

- [Cloud Run 文档](https://cloud.google.com/run/docs)
- [Cloud Run 定价](https://cloud.google.com/run/pricing)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)

## ❓ 常见问题

### Q: 免费额度够用吗？
**A**: 对于个人使用和小规模使用，免费额度通常足够。每月 200 万请求相当于每天约 6.6 万次请求。

### Q: 如何降低成本？
**A**: 
- 使用最小内存配置（512Mi）
- 设置最小实例数为 0（冷启动）
- 优化代码减少执行时间

### Q: 可以部署到其他区域吗？
**A**: 可以，选择离用户最近的区域以获得更好的性能。

---

**提示**：首次部署可能需要 5-10 分钟。部署成功后，你的工具就可以通过 HTTPS URL 访问了！

