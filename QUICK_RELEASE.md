# 快速发布指南

这是一个简明版本。完整说明请查看 [RELEASE.md](./RELEASE.md)

## 📤 三步发布新版本

### 1️⃣ 标记版本

```bash
git tag -a v1.0.0 -m "描述此版本的内容"
```

### 2️⃣ 推送标签

```bash
git push origin v1.0.0
```

### 3️⃣ 等待完成

GitHub Actions 会自动打包并发布到 Releases 页面（大约需要 2-3 分钟）

✅ 完成！用户可以在 Releases 页面下载

---

## 📋 版本号约定

- `v1.0.0` - 新功能或重要版本
- `v1.0.1` - 修复bug
- `v1.1.0` - 添加功能

## 🔗 分享链接

```
最新版本下载:
https://github.com/你的用户名/你的仓库/releases/latest

所有版本列表:
https://github.com/你的用户名/你的仓库/releases
```

## ⚠️ 注意

- 确保本地代码已 commit 并且测试通过
- `config.json` 中不要提交真实的服务器地址
- 第一次发布前检查 [RELEASE.md](./RELEASE.md) 中的完整说明
