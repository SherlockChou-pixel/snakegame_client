# 贪吃蛇客户端自动打包脚本

## 快速开始

### 首次使用（初始化打包环境）

首先需要初始化打包环境，只需运行一次：

```bash
python setup_build_env.py
```

这会创建一个独立的 conda 环境 `snake_build`，包含所有打包所需的工具。

### 打包应用

初始化完成后，直接运行打包脚本：

```bash
python build_script.py
```

## 使用方法

运行以下命令来自动打包客户端：

```bash
python build_script.py
```

脚本会：
1. 清理旧的build和dist目录
2. 使用独立的打包环境执行PyInstaller
3. 生成 `dist/SnakeGameClient.exe` 文件
4. 输出打包结果

## 配置

- `config.json`: 服务器配置，包含IP和端口
- `SnakeGameClient.spec`: PyInstaller配置文件
- `snake_build`: 专用打包环境（由 setup_build_env.py 创建）

## 打包环境说明

使用独立的 `snake_build` conda 环境打包有以下优势：
- ✅ 避免与其他Python环境产生版本冲突
- ✅ 确保打包的稳定性和可重复性
- ✅ 不会污染主环境

如果需要重新初始化环境，可以运行：
```bash
conda env remove -n snake_build
python setup_build_env.py
```

## 上传到仓库前注意事项

1. **检查敏感信息**: 确保 `config.json` 中的服务器IP不是真实的服务器地址，或者设置为本地测试地址
2. **清理build文件**: 不要上传 `build/` 和 `dist/` 目录
3. **配置文件**: 可以考虑将 `config.json` 添加到 `.gitignore` 中，避免上传敏感配置

## 运行打包后的程序

打包后的exe文件位于 `dist/` 目录中，双击即可运行。

## 故障排除

**问题：无法找到snake_build环境**
- 解决：重新运行 `python setup_build_env.py` 初始化环境

**问题：打包失败**
- 检查 `SnakeGameClient.spec` 中的文件路径是否正确
- 确保 `config.json` 和 `simhei.ttf` 文件存在