# GitHub 发布指南

本指南将帮助你将这个 YouTube 视频 URL 抓取工具发布到 GitHub。

## 📋 发布前检查清单

### ✅ 1. 代码清理
- [x] 已创建 `.gitignore` 文件，排除敏感信息和临时文件
  - [x] 排除输出文件（`output/*.txt`, `output/*.xlsx`, `output/*.xls`）
  - [x] 排除日志文件（`logs/*.log`）
  - [x] 排除 Python 缓存（`__pycache__/`）
- [x] 已创建 `LICENSE` 文件
- [x] 已创建 `README.md` 文件（包含完整的使用说明）
- [x] 已创建 `.gitkeep` 文件确保目录结构被跟踪

### ✅ 2. 敏感信息检查
在发布前，请检查以下文件是否包含敏感信息：
- `main.py` - 检查是否有硬编码的频道 URL（示例 URL 可以保留）
- `core/config.py` - 检查是否有 API 密钥或其他敏感配置
- 日志文件 - 已通过 `.gitignore` 排除

### ✅ 3. 文档完整性
- [x] README.md - 包含项目介绍、安装说明、使用方法
- [x] requirements.txt - 包含所有依赖
- [x] 使用说明.md - 详细的使用文档
- [x] 性能说明.md - 性能相关说明
- [x] 抓取方式说明.md - 技术实现说明

## 🚀 发布步骤

### 第一步：初始化 Git 仓库（如果还没有）

```bash
cd "/Volumes/工作/AI 个人成长"

# 初始化 git 仓库
git init

# 检查当前状态
git status
```

### 第二步：添加所有文件

```bash
# 添加所有文件到暂存区
git add .

# 查看将要提交的文件
git status
```

**注意**：确保以下文件被正确忽略（不会出现在 `git status` 中）：
- `output/*.txt` - 文本格式输出文件
- `output/*.xlsx` - Excel 格式输出文件
- `output/*.xls` - Excel 格式输出文件（旧格式）
- `logs/*.log` - 日志文件
- `__pycache__/` - Python 缓存
- `.DS_Store` - macOS 系统文件

**重要**：所有生成的输出文件（包括 Excel 和 TXT）都保存在 `output/` 目录下，这些文件**不会**被提交到 GitHub，只保存在本地。这是正确的行为，因为：
- 输出文件是用户运行工具后生成的，属于用户数据
- 不同用户会有不同的输出文件
- 避免仓库体积过大

### 第三步：创建首次提交

```bash
# 创建首次提交
git commit -m "Initial commit: YouTube video URL scraper tool

- Add YouTube channel video URL scraper
- Add web interface with Flask
- Add command-line interface
- Add comprehensive documentation
- Add MIT License"
```

### 第四步：在 GitHub 上创建仓库

1. 登录 GitHub
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `youtube-url-scraper`（或你喜欢的名称）
   - **Description**: `A fast and easy-to-use tool to scrape YouTube channel video URLs with web interface and CLI support`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
4. 点击 "Create repository"

### 第五步：连接本地仓库到 GitHub

```bash
# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/youtube-url-scraper.git

# 或者使用 SSH（如果你配置了 SSH 密钥）
# git remote add origin git@github.com:YOUR_USERNAME/youtube-url-scraper.git

# 验证远程仓库
git remote -v
```

### 第六步：推送代码到 GitHub

```bash
# 推送代码到 GitHub（首次推送）
git branch -M main
git push -u origin main
```

如果遇到认证问题：
- **HTTPS 方式**：GitHub 现在使用 Personal Access Token 而不是密码
  - 访问 https://github.com/settings/tokens
  - 生成新的 token（选择 `repo` 权限）
  - 使用 token 作为密码
- **SSH 方式**：需要配置 SSH 密钥
  - 参考：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### 第七步：验证发布结果

1. 访问你的 GitHub 仓库页面
2. 检查以下内容是否正确显示：
   - ✅ README.md 内容
   - ✅ 项目文件结构
   - ✅ LICENSE 文件
   - ✅ requirements.txt

## 📝 后续维护

### 更新代码并推送

```bash
# 1. 查看更改
git status

# 2. 添加更改的文件
git add .

# 3. 提交更改
git commit -m "描述你的更改"

# 4. 推送到 GitHub
git push
```

### 创建 Release（可选）

如果你想创建版本发布：

1. 在 GitHub 仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: 描述新版本的功能
4. 点击 "Publish release"

### 添加 GitHub Actions（可选）

可以创建 `.github/workflows/ci.yml` 来自动化测试和检查：

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests (if any)
        run: |
          # 添加测试命令
          echo "Tests would run here"
```

## 🔒 安全建议

1. **不要提交敏感信息**：
   - API 密钥
   - 个人频道 URL（示例可以保留）
   - 密码或令牌

2. **使用环境变量**：
   如果将来需要 API 密钥，使用环境变量而不是硬编码：
   ```python
   import os
   API_KEY = os.getenv('YOUTUBE_API_KEY', '')
   ```

3. **定期更新依赖**：
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

## 📚 有用的 Git 命令

```bash
# 查看提交历史
git log

# 查看文件更改
git diff

# 撤销未提交的更改
git checkout -- filename

# 创建新分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature
```

## 🎯 发布后的推广建议

1. **添加项目标签（Topics）**：
   - `youtube`
   - `scraper`
   - `python`
   - `flask`
   - `web-scraping`
   - `youtube-dl`
   - `yt-dlp`

2. **编写项目简介**：
   在 GitHub 仓库的 "About" 部分添加简短描述

3. **添加徽章（可选）**：
   可以在 README.md 中添加一些徽章，例如：
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
   ![License](https://img.shields.io/badge/license-MIT-green.svg)
   ```

## ❓ 常见问题

### Q: 推送时提示 "remote: Support for password authentication was removed"
**A**: GitHub 不再支持密码认证，需要使用 Personal Access Token 或 SSH 密钥。

### Q: 如何更新 README.md 中的仓库链接？
**A**: 在 README.md 中搜索并替换所有包含路径的地方，改为相对路径或 GitHub 链接。

### Q: 如何添加贡献指南？
**A**: 创建 `CONTRIBUTING.md` 文件，说明如何贡献代码。

### Q: 如何添加问题模板？
**A**: 在 GitHub 仓库设置中，可以创建 Issue 和 Pull Request 模板。

---

**提示**：发布前建议先在本地测试所有功能，确保代码可以正常运行。

