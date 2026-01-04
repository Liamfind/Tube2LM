# 常见问题解答 (FAQ)

## 📤 关于文件存储

### Q1: 其他人使用这个工具时，生成的 Excel 文件会存储到哪里？

**A**: Excel 文件**只保存在他们的本地电脑**，绝对不会上传到你的 GitHub 仓库。

**详细说明**：
- ✅ 文件保存在他们本地 `output/` 目录
- ✅ 每个用户都有自己的输出文件，互不干扰
- ✅ `.gitignore` 已经配置好，这些文件不会被 Git 跟踪
- ✅ 即使他们想提交，也提交不了（除非修改 `.gitignore`）
- ✅ 即使他们修改 `.gitignore` 并提交，也只会提交到他们自己的 Fork，不会影响你的原始仓库

**示例场景**：
```
用户 A 克隆仓库 → 运行工具 → 生成 Excel → 保存在本地
用户 B 克隆仓库 → 运行工具 → 生成 Excel → 保存在本地（不同位置）
你的 GitHub 仓库 → 始终保持干净，没有任何 Excel 文件
```

### Q2: 如果其他人 Fork 了我的仓库，他们的 Excel 文件会出现在哪里？

**A**: 仍然只保存在他们的本地，不会出现在 GitHub 上。

**说明**：
- 如果他们 Fork 了仓库，Excel 文件仍然保存在他们本地
- 即使他们修改 `.gitignore` 并强制提交，也只会提交到**他们自己的 Fork**
- **绝对不会影响你的原始仓库**

### Q3: 如何确保 Excel 文件不会被意外提交？

**A**: 已经通过 `.gitignore` 配置好了，你可以通过以下方式验证：

```bash
# 1. 检查 .gitignore
cat .gitignore | grep xlsx
# 应该看到：output/*.xlsx

# 2. 尝试添加 Excel 文件（应该失败）
git add output/*.xlsx
git status
# Excel 文件不会出现在暂存区

# 3. 检查当前状态
git status
# 应该看不到任何 Excel 文件
```

### Q4: 如果我想分享示例 Excel 文件怎么办？

**A**: 可以创建一个 `examples/` 目录专门存放示例文件：

```bash
# 1. 创建 examples 目录
mkdir examples

# 2. 将示例文件放在这里
cp output/example.xlsx examples/

# 3. 更新 .gitignore（如果需要）
# 在 .gitignore 中排除 output/ 但保留 examples/
```

## 🔧 关于工具使用

### Q5: Web 界面下载的 Excel 文件保存在哪里？

**A**: 保存在服务器运行目录的 `output/` 目录中。

**说明**：
- 如果你在本地运行 `python3 web_app.py`，文件保存在本地 `output/` 目录
- 如果你部署到服务器，文件保存在服务器的 `output/` 目录
- 用户通过浏览器下载时，文件会下载到他们的**下载文件夹**，而不是服务器

### Q6: 命令行模式生成的 Excel 文件在哪里？

**A**: 保存在项目根目录的 `output/` 目录中。

**示例**：
```bash
# 项目目录
/Users/username/youtube-url-scraper/

# Excel 文件位置
/Users/username/youtube-url-scraper/output/频道名_20240104_120000.xlsx
```

## 🔒 关于隐私和安全

### Q7: Excel 文件包含什么信息？是否安全？

**A**: Excel 文件包含：
- 视频 URL（公开信息）
- 发布时间（公开信息）
- 视频 ID（公开信息）

**安全性**：
- ✅ 这些都是 YouTube 上的公开信息
- ✅ 不包含任何个人隐私信息
- ✅ 不包含 API 密钥或密码
- ⚠️ 但可能反映你关注的频道，建议不要公开分享

### Q8: 如果我不小心提交了 Excel 文件怎么办？

**A**: 可以这样处理：

```bash
# 1. 从 Git 历史中删除文件（但保留本地文件）
git rm --cached output/*.xlsx

# 2. 提交更改
git commit -m "Remove Excel files from repository"

# 3. 推送到 GitHub
git push

# 4. 确保 .gitignore 已更新
# 检查 .gitignore 是否包含 output/*.xlsx
```

## 📝 关于 GitHub 发布

### Q9: 发布到 GitHub 后，我需要做什么来保护仓库？

**A**: 已经配置好了，你不需要做任何额外的事情：

- ✅ `.gitignore` 已经排除所有输出文件
- ✅ 目录结构通过 `.gitkeep` 保留
- ✅ 其他人无法提交 Excel 文件到你的仓库

### Q10: 如何验证发布后的配置是否正确？

**A**: 按照以下步骤验证：

```bash
# 1. 克隆你的仓库到新位置（模拟其他用户）
cd /tmp
git clone https://github.com/YOUR_USERNAME/youtube-url-scraper.git
cd youtube-url-scraper

# 2. 运行工具生成 Excel 文件
python3 main.py

# 3. 检查 Git 状态
git status
# 应该看不到 output/*.xlsx 文件

# 4. 尝试添加（应该失败）
git add output/*.xlsx
git status
# Excel 文件仍然不会出现在暂存区
```

## 🚀 关于部署

### Q11: 如果部署到服务器，Excel 文件存储在哪里？

**A**: 保存在服务器的项目目录的 `output/` 目录中。

**注意事项**：
- 服务器上的 Excel 文件不会自动同步到 GitHub
- 如果服务器重启或清理，文件可能会丢失
- 建议定期备份重要文件

### Q12: 可以配置 Excel 文件保存到其他位置吗？

**A**: 可以，修改 `core/config.py`：

```python
# 修改输出目录
OUTPUT_DIR = Path("/path/to/your/custom/output")
OUTPUT_DIR.mkdir(exist_ok=True)
```

---

**提示**：如果还有其他问题，可以在 GitHub Issues 中提问。

