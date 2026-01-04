# GitHub 发布步骤（快速指南）

## 步骤 1：在 GitHub 网页上创建仓库

✅ 已完成：
- Repository name: `Tube2LM`
- Description: 已填写
- Public 仓库
- 不要勾选 README、.gitignore、License（我们已经有了）

点击 "Create repository" 按钮

## 步骤 2：在本地终端执行以下命令

### 2.1 进入项目目录

```bash
cd "/Volumes/工作/AI 个人成长"
```

### 2.2 初始化 Git 仓库（如果还没有）

```bash
# 检查是否已有 .git 目录
ls -la .git

# 如果没有，初始化
git init
```

### 2.3 添加所有文件

```bash
# 添加所有文件
git add .

# 检查状态（确认 Excel 文件不会被添加）
git status
```

**重要检查**：运行 `git status` 后，应该**看不到**：
- `output/*.xlsx`
- `output/*.txt`
- `logs/*.log`

如果看到了这些文件，说明 `.gitignore` 没有生效，请检查 `.gitignore` 文件。

### 2.4 创建首次提交

```bash
git commit -m "Initial commit: YouTube video URL scraper tool

- Add YouTube channel video URL scraper
- Add web interface with Flask
- Add command-line interface
- Add comprehensive documentation
- Add MIT License"
```

### 2.5 连接远程仓库

```bash
# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名，应该是 "Liamfind"）
git remote add origin https://github.com/Liamfind/Tube2LM.git

# 验证远程仓库
git remote -v
```

### 2.6 推送代码到 GitHub

```bash
# 设置主分支名称
git branch -M main

# 推送到 GitHub（首次推送）
git push -u origin main
```

**注意**：如果遇到认证问题：
- GitHub 现在使用 Personal Access Token 而不是密码
- 如果提示输入密码，需要：
  1. 访问 https://github.com/settings/tokens
  2. 生成新的 token（选择 `repo` 权限）
  3. 使用 token 作为密码

### 2.7 验证发布结果

1. 访问你的仓库：`https://github.com/Liamfind/Tube2LM`
2. 检查以下内容是否正确显示：
   - ✅ README.md 内容
   - ✅ 项目文件结构
   - ✅ LICENSE 文件
   - ✅ requirements.txt
   - ✅ 所有代码文件

## 步骤 3：发布后的优化（可选）

### 3.1 添加仓库描述和标签

在仓库页面点击 "⚙️ Settings" → "General" → "Topics"，添加标签：
- `youtube`
- `scraper`
- `python`
- `flask`
- `web-scraping`
- `yt-dlp`
- `notebooklm`

### 3.2 创建第一个 Release（可选）

1. 在仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. 填写：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: 描述主要功能

## 常见问题

### Q: 推送时提示 "remote: Support for password authentication was removed"
**A**: 需要使用 Personal Access Token：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 `repo` 权限
4. 生成后复制 token
5. 推送时使用 token 作为密码

### Q: 如何确认 Excel 文件不会被提交？
**A**: 运行 `git status`，应该看不到 `output/*.xlsx` 文件。

### Q: 推送后看不到文件？
**A**: 刷新浏览器页面，或检查是否推送到了正确的分支。

---

**提示**：如果遇到任何问题，请查看终端输出的错误信息。

