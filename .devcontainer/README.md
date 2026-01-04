# GitHub Codespaces 使用说明

## 🚀 一键在浏览器中使用

这个项目已配置 GitHub Codespaces，你可以直接在浏览器中使用，无需本地安装！

## 📋 使用步骤

### 方法一：使用 GitHub 网页（最简单）

1. 访问仓库：https://github.com/Liamfind/Tube2LM
2. 点击绿色的 **"Code"** 按钮
3. 选择 **"Codespaces"** 标签
4. 点击 **"Create codespace on main"**
5. 等待 Codespace 启动（约 1-2 分钟）
6. 启动后，终端会自动运行 `pip install -r requirements.txt`
7. 安装完成后，运行：
   ```bash
   python3 web_app.py
   ```
8. 点击终端中出现的 **"Open in Browser"** 链接，或访问提示的 URL

### 方法二：使用 Codespaces 网页

1. 访问：https://github.com/codespaces
2. 点击 **"New codespace"**
3. 选择仓库：`Liamfind/Tube2LM`
4. 点击 **"Create codespace"**
5. 等待启动后，按照上面的步骤 6-8 操作

## ⚡ 快速启动脚本

Codespace 启动后，你可以直接运行：

```bash
# 方式一：使用启动脚本
./start_web.sh

# 方式二：直接运行
python3 web_app.py
```

## 🌐 访问 Web 界面

启动后，Codespace 会自动转发端口 8080，你可以：
- 点击终端中出现的 **"Open in Browser"** 链接
- 或访问 Codespace 提供的端口转发 URL

## 💡 提示

- Codespaces 是免费的（每月有使用额度）
- 每次使用都会创建一个新的环境
- 数据会保存在 Codespace 中，直到你删除它
- 输出文件保存在 `output/` 目录，可以下载

## ❓ 常见问题

### Q: Codespaces 是免费的吗？
**A**: 是的，GitHub 为个人账户提供每月 60 小时的免费使用时间。

### Q: 如何保存输出文件？
**A**: 在 Codespace 中，你可以：
- 右键点击 `output/` 目录中的文件，选择 "Download"
- 或使用终端命令下载

### Q: Codespace 会一直运行吗？
**A**: 不会，如果 30 分钟没有活动，Codespace 会自动停止。你可以随时重新启动。

