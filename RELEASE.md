# 软件发布指南

这个文档说明如何发布新版本并让用户下载。

## 🚀 发布流程

### 方式一：自动发布（推荐）

使用 GitHub Actions 的自动化工作流：

#### 第1步：准备版本

确保你的代码已经提交并且一切就绪：

```bash
# 确认所有改动已commit
git status

# 查看提交日志
git log --oneline -5
```

#### 第2步：创建版本标签

使用语义化版本命名（遵循 Semantic Versioning）：

```bash
# 创建标签并添加说明
git tag -a v1.0.0 -m "首次发布版本

- 支持远程多人游戏
- 完整的UI界面
- 自动重连功能"

# 或者不带说明
git tag v1.0.0
```

**版本命名约定**：
- `v1.0.0` - 主版本.次版本.修订版本
- `v1.1.0` - 添加新功能
- `v1.0.1` - 修复bug
- `v2.0.0` - 重大改动

#### 第3步：推送标签

```bash
# 推送此标签
git push origin v1.0.0

# 或推送所有标签
git push origin --tags
```

#### 第4步：自动构建和发布

GitHub Actions 会自动：
1. 获取代码
2. 设置 Python 3.9 环境
3. 安装依赖包
4. 打包成 `.exe` 文件
5. 创建 Release 并上传文件

**查看进度**.
- 访问你的GitHub仓库
- 点击 "Actions" 标签页
- 查看 "打包并发布版本" 工作流的运行状态

完成后，你会在 "Releases" 页面看到新版本！

### 方式二：手动发布

如果自动化失败，可以手动发布：

#### 第1步：本地打包

```bash
cd snakegameClient
python build_script.py
```

生成 `dist/SnakeGameClient.exe` 文件。

#### 第2步：创建 Release

GitHub 网页界面操作：

1. 访问仓库的 "Releases" 页面
2. 点击 "Draft a new release"
3. 选择标签（或创建新标签）：`v1.0.0`
4. 填写发布标题和说明
5. 上传 `SnakeGameClient.exe` 文件
6. 点击 "Publish release"

## 📥 用户下载

### 下载链接格式

发布后，用户可以通过以下方式下载：

**GitHub Releases 页面**:
```
https://github.com/你的用户名/你的仓库/releases
```

**直接下载最新版本**:
```
https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/SnakeGameClient.exe
```

### 在 README 中添加下载链接

在 `README.md` 的快速开始部分添加：

```markdown
## 📥 快速下载

### 不想自己编译？直接下载编译好的版本：

**[下载 SnakeGameClient.exe](https://github.com/你的用户名/你的仓库/releases/latest/download/SnakeGameClient.exe)**

最新版本: v1.0.0
```

## 📋 发布前检查清单

在发布新版本前，务必检查：

- [ ] 所有bug已修复
- [ ] 代码已测试
- [ ] `config.json` 中的服务器IP设置为测试地址
- [ ] 所有改动已提交到 git
- [ ] 版本号符合语义化版本规范
- [ ] CHANGELOG 已更新

## 🔄 常见场景

### 场景1：发布版本后发现问题

```bash
# 撤销标签
git tag -d v1.0.0
git push origin --delete v1.0.0

# 修复问题后，重新发布
git tag -a v1.0.1 -m "修复xxx问题"
git push origin v1.0.1
```

### 场景2：测试版本

使用 `beta` 标签：

```bash
git tag v1.0.0-beta
git push origin v1.0.0-beta
```

### 场景3：紧急热修补

```bash
git tag v1.0.1 -m "紧急修复更新"
git push origin v1.0.1
```

## 📊 版本号含义

| 版本 | 说明 | 用途 |
|------|------|------|
| v1.0.0 | 主版本.次版本.修订版本 | 标准版本 |
| v1.1.0 | 添加新功能 | 新功能发布 |
| v1.0.1 | 修复bug | 补丁更新 |
| v2.0.0 | 重大改动 | 大版本升级 |
| v1.0.0-alpha | 试验版/内测版 | 开发版本 |
| v1.0.0-beta | 测试版 | 即将正式版 |

## 🔐 权限说明

要让 GitHub Actions 能够创建 Release，需要配置权限：

1. 访问仓库设置 → Settings
2. 找到 "Actions" → "General"
3. 在 "Workflow permissions" 中：
   - 选择 "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"
4. 保存

## 📞 故障排除

### 问题：Actions 工作流失败

**检查日志**:
1. 仓库 → Actions
2. 找到失败的工作流
3. 点击查看详细日志
4. 常见原因：
   - 依赖安装失败 → 检查网络
   - 打包失败 → 检查源代码
   - 权限不足 → 检查 workflow permissions

### 问题：Release 后没有文件

确保 `.exe` 文件成功生成。在 Actions 日志中查看打包步骤的输出。

### 问题：如何修改 workflow

编辑 `.github/workflows/release.yml` 文件：

1. GitHub 网页编辑器打开文件
2. 修改参数
3. Commit 变更
4. 下次推送标签时使用新的 workflow

## 📚 参考资源

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/lang/zh-CN/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
