# 📦 发布与分享指南

## 🎯 你有以下几种方式提供下载链接

### 方案 1️⃣：GitHub Releases（推荐 ⭐⭐⭐）

**适用于**: 项目在 GitHub 上

**优点**:
- ✅ 自动化发布（GitHub Actions）
- ✅ 官方平台，用户信任度高
- ✅ 版本管理方便
- ✅ 发布说明和更新日志清晰

**使用方式**:

```bash
# 1. 创建版本标签
git tag -a v1.0.0 -m "初始发布"

# 2. 推送标签
git push origin v1.0.0

# 3. 自动打包并发布（GitHub Actions 自动完成）
# 2-3 分钟后在 Releases 页面下载

# 4. 分享链接
https://github.com/你的用户名/你的仓库/releases/latest
```

📖 [详见 RELEASE.md](./RELEASE.md)

**快速命令** (从 [QUICK_RELEASE.md](./QUICK_RELEASE.md)):
```bash
git tag -a v1.0.0 -m "描述"
git push origin v1.0.0
# 等待 2-3 分钟...完成！
```

---

### 方案 2️⃣：自建服务器/网盘

**适用于**: 有自己的服务器或想用云盘

**支持的平台**:
- 🌐 自己的网站
- ☁️ 百度云盘 / 阿里云盘 / 微云
- 📦 腾讯cos / OSS 对象存储
- 📁 GitLab / Gitee

**使用方式**:

```bash
# 快速准备打包文件
python upload_helper.py

# 生成 releases/v1.0.0/ 文件夹
# 包含:
# - SnakeGameClient.exe
# - README.txt
```

然后手动上传到你的服务器或网盘。

📖 [使用 upload_helper.py](#upload_helper)

---

### 方案 3️⃣：直接分发

**适用于**: 小范围分发（朋友、同学、测试）

只需分享 `dist/SnakeGameClient.exe` 文件：

```bash
# 打包一次
python build_script.py

# 将 dist/SnakeGameClient.exe 发送给用户
# 用户直接双击运行即可
```

---

## 📋 文件说明

| 文件 | 用途 |
|------|------|
| **README.md** | 完整的项目文档 |
| **RELEASE.md** | 发布流程详细说明 |
| **QUICK_RELEASE.md** | 快速发布参考 |
| **upload_helper.py** | 打包辅助工具 |
| **.github/workflows/release.yml** | GitHub Actions 自动化脚本 |

---

## 🚀 推荐流程

### 场景1：第一次发布

```bash
# 1. 确保代码已commit
git status

# 2. 创建标签（格式: v主.次.修）
git tag -a v1.0.0 -m "首次发布
- 功能: 贪吃蛇游戏
- 支持多人对战
- 自动重连"

# 3. 推送
git push origin v1.0.0

# 4. 等待（GitHub Actions 自动打包，2-3分钟）

# 5. 分享
# 在 Releases 页面找到新版本，分享下载链接
```

### 场景2：修复bug后发布

```bash
# 1. 修改代码
# ...

# 2. 提交
git commit -am "修复xx问题"

# 3. 创建新标签（版本号+1）
git tag -a v1.0.1 -m "修复连接问题"

# 4. 推送
git push origin v1.0.1
```

### 场景3：想在网盘分享

```bash
# 1. 使用helper脚本打包
python upload_helper.py

# 2. 上传 releases/ 文件夹到网盘

# 3. 分享网盘链接
```

---

## 🔗 下载链接示例

### GitHub Releases 链接

发布后，用户可以通过以下链接下载：

```
# 查看所有版本
https://github.com/你的用户名/你的仓库/releases

# 下载最新版本
https://github.com/你的用户名/你的仓库/releases/latest

# 下载特定版本
https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/SnakeGameClient.exe

# 直接下载最新exe
https://github.com/你的用户名/你的仓库/releases/latest/download/SnakeGameClient.exe
```

### 在项目页面添加下载链接

编辑项目的 `README.md`，在顶部添加：

```markdown
## 📥 下载

[📦 下载最新版](https://github.com/你的用户名/你的仓库/releases/latest)

或查看 [所有版本](https://github.com/你的用户名/你的仓库/releases)
```

---

## 🔧 helper脚本使用

### upload_helper.py

自动打包并准备上传所需的文件。

**使用**:

```bash
python upload_helper.py
```

**输出**:
```
releases/
├── v1.0.0/
│   ├── SnakeGameClient.exe
│   └── README.txt
└── build_20240403_143022/
    ├── SnakeGameClient.exe
    └── README.txt
```

然后可以上传 `releases/` 文件夹到你的服务器。

---

## 💡 最佳实践

### ✅ 正确做法

```bash
# 清晰的版本号
git tag -a v1.0.0 -m "..."

# 详细的发布说明
git tag -a v1.0.0 -m "功能:
- 新增房间列表
- 优化连接稳定性
修复:
- 修复掉线重连问题
- 修复UI显示问题"

# 只在特定分支发布
git tag -a v1.0.0 -m "..." # 在main分支上

# 定期发布版本
# 不是每次commit都发版本
```

### ❌ 避免做法

```bash
# 不要用不清晰的版本号
git tag random_build

# 不要在测试分支上发布
git checkout test
git tag v1.0.0

# 不要修改已发布的标签
git tag -f v1.0.0  # 会导致用户混淆

# 不要在exe中硬编码真实服务器地址
# 要使用 config.json 存储配置
```

---

## 📞 常见问题

**Q: GitHub Actions 失败了怎么办？**
A: 检查 Actions 标签页的日志，通常是依赖问题。

**Q: 可以同时支持多个版本吗？**
A: 可以，每个标签都是一个版本，历史版本也能下载。

**Q: 如何删除错误发布的版本？**
A: `git tag -d v1.0.0 && git push origin --delete v1.0.0`

**Q: 发布前如何测试？**
A: 本地运行 `python build_script.py` 测试，确保能打包成功exe。

---

## 📚 相关文档

- [完整发布指南](./RELEASE.md)
- [快速发布参考](./QUICK_RELEASE.md)
- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
