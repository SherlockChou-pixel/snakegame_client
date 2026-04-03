# 贪吃蛇远程游戏客户端

这是一个基于 Pygame 开发的贪吃蛇游戏客户端，支持远程多人游戏和自动化打包。

## 📋 项目概述

- **语言**: Python 3.9+
- **主要依赖**: Pygame, Socket
- **功能**: 连接远程服务器，支持多人实时对战
- **打包工具**: PyInstaller

## 📁 项目结构

```
snakegameClient/
├── main.py                 # 主程序入口
├── game_ui.py             # 游戏UI模块
├── network.py             # 网络通信模块
├── protocol.py            # 通信协议定义
├── config.json            # 服务器配置文件
├── simhei.ttf             # 中文字体文件
│
├── build_script.py        # 自动打包脚本 ⭐
├── setup_build_env.py     # 环境初始化脚本 ⭐
│
├── SnakeGameClient.spec   # PyInstaller配置文件
├── BUILD_README.md        # 打包详细说明
├── README.md              # 本文件
│
├── main.py.spec           # PyInstaller生成的spec（可忽略）
├── main.spec              # PyInstaller生成的spec（可忽略）
├── .gitignore            # Git忽略配置
├── .git/                 # Git仓库信息
├── build/                # PyInstaller临时文件（打包时生成）
├── dist/                 # 打包输出目录（包含最终的exe）
└── __pycache__/          # Python缓存文件
```

## � 下载打包好的程序

如果你只想运行游戏，不需要安装 Python 和依赖，可以直接下载编译好的版本：

### ⚡ 快速下载

**[查看所有版本](../../releases)**  |  **[下载最新版本](../../releases/latest)**

最新版本会在 Releases 页面发布，下载后双击 `SnakeGameClient.exe` 即可运行。

> 💡 **提示**: 根据你的项目实际情况，将上面的链接替换为实际的 GitHub 仓库链接

## �🚀 快速开始

### 1. 环境初始化（首次使用）

首先创建专用的打包环境：

```bash
python setup_build_env.py
```

这个脚本会创建一个名为 `snake_build` 的 conda 环境，包含所有打包所需的工具。
**初始化时间**: 约 2-5 分钟（取决于网络速度）

### 2. 直接运行客户端

```bash
python main.py
```

需要确保：
- 配置了正确的服务器IP和端口在 `config.json` 中
- 安装了依赖包：`pip install pygame`

### 3. 打包成exe

```bash
python build_script.py
```

打包成功后，会在 `dist/` 目录中生成 `SnakeGameClient.exe` 文件，双击即可运行。

## ⚙️ 配置说明

### config.json

```json
{
    "server_ip": "127.0.0.1",
    "server_port": 8888
}
```

**配置项**:
- `server_ip`: 游戏服务器的 IP 地址
- `server_port`: 游戏服务器的端口号

**修改方法**:
1. 用文本编辑器打开 `config.json`
2. 修改为实际的服务器地址
3. **上传仓库前**: 请改为测试地址（如 `127.0.0.1`）以隐藏真实服务器地址

### main.py 中的连接

客户端会自动从 `config.json` 加载服务器配置：

```python
def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('server_ip', '127.0.0.1'), config.get('server_port', 8888)
    except (FileNotFoundError, json.JSONDecodeError):
        print("配置文件加载失败，使用默认配置")
        return '127.0.0.1', 8888
```

## 📦 打包说明

### 打包流程

1. **清理旧文件**: 删除之前的 `build/` 和 `dist/` 目录
2. **使用snake_build环境**: 在隔离环境中运行 PyInstaller
3. **生成exe**: 输出 `dist/SnakeGameClient.exe`

### 打包配置 (SnakeGameClient.spec)

关键配置项：
- `name`: 输出exe的名称（`SnakeGameClient`）
- `console`: 是否显示控制台窗口（设为 `False` - 关闭）
- `datas`: 打包时包含的数据文件（包含 `config.json`）
- `upx`: UPX压缩（设为 `False` - 避免兼容性问题）

### 打包环境说明

**为什么使用 `snake_build` 环境**:

- ✅ **隔离性**: 不会与其他Python环境产生版本冲突
- ✅ **稳定性**: 保证打包的可重复性
- ✅ **干净性**: 不会污染主环境
- ✅ **兼容性**: Python 3.9 与 PyInstaller 完全兼容

这解决了在不同Python版本间出现的 `is_py314` 等属性错误问题。

## ⚠️ 关于打包过程中的警告

### 常见警告信息

在打包过程中可能会看到以下警告信息：

```
WARNING: Library not found: could not resolve 'msmpi.dll'
WARNING: Library not found: could not resolve 'pgmath.dll'
```

**这些警告**:
- ❌ 不会影响最终的打包结果
- ❌ 是 PyInstaller 在分析数学库依赖时的正常输出
- ❌ 游戏运行不需要这些库
- ✅ 最后显示"打包成功"就表示打包完成了

### 如果看到错误来自 `test` 环环境

这说明你在错误的环境中运行了打包脚本。解决方法：

```bash
# 确保使用正确的环境
conda activate snake_build    # 可选
python build_script.py        # 脚本会自动在snake_build中运行
```

## 🎮 游戏操作

### 游戏界面控制

- **上/W**: 蛇向上移动
- **下/S**: 蛇向下移动
- **左/A**: 蛇向左移动
- **右/D**: 蛇向右移动

### 游戏程序流程

1. 启动程序，等待连接服务器
2. 点击"加入房间"按钮
3. 点击"开始游戏"按钮
4. 使用方向键控制蛇的移动
5. 吃到食物获得分数

## 📝 模块说明

### main.py (主程序)

- 实现 `Client` 类处理游戏逻辑
- 管理与服务器的连接
- 处理UI事件和用户输入
- 自动重连机制

**核心功能**:
- 连接管理
- 消息解析
- 游戏状态同步
- 自动重连

### game_ui.py (游戏UI)

使用 Pygame 实现游戏界面：
- 主菜单场景
- 游戏场景
- 玩家列表
- 分数显示

**支持**:
- 中文界面（使用 `simhei.ttf` 字体）
- 打包环境下的字体自动获取

### network.py (网络通信)

管理与服务器的 Socket 连接：
- TCP连接处理
- 数据接收/发送
- 连接状态管理
- 异常处理

### protocol.py (通信协议)

定义客户端与服务器的通信协议：

```
命令码:
1 - 加入房间 (join_room)
2 - 开始游戏 (start_game)
3 - 移动指令 (move)
4 - 获取地图 (get_map)
6 - 房间玩家列表
```

## 🔧 故障排除

### 问题：打包时出现"FileNotFoundError"

**原因**: config.json 或 simhei.ttf 文件缺失

**解决**:
```bash
# 检查文件是否存在
dir config.json
dir simhei.ttf

# 如果缺失，从备份复制或重新创建 config.json
```

### 问题：打包成功但运行exe时找不到config.json

**原因**: exe运行时找不到配置文件

**解决**: 确保 `SnakeGameClient.spec` 中包含了 `config.json`:
```python
datas=[('config.json', '.')],
```

### 问题：无法连接到服务器

**原因**: 
1. 服务器地址或端口错误
2. 服务器未启动
3. 防火墙阻止连接

**解决**:
1. 检查 `config.json` 中的 IP 和端口
2. 确保服务器在线运行
3. 检查防火墙设置

### 问题：游戏界面显示不正确

**原因**: 缺少中文字体文件

**解决**: 确保 `simhei.ttf` 在同目录下

## 📤 上传到仓库前的检查清单

- [ ] 将 `config.json` 中的服务器IP改为测试地址（如 `127.0.0.1`）
- [ ] 删除 `build/` 和 `dist/` 目录
- [ ] 删除 `__pycache__/` 目录
- [ ] 确保 `.gitignore` 配置正确
- [ ] 所有 `*.spec` 文件路径正确
- [ ] `simhei.ttf` 和 `config.json` 已包含

## 🔄 环境管理

### 查看现有环境

```bash
conda env list
```

### 重新初始化环境

如果遇到环境问题，可以重新初始化：

```bash
# 删除旧环境
conda env remove -n snake_build

# 重新创建
python setup_build_env.py
```

### 激活/停用环境

```bash
# 激活环境
conda activate snake_build

# 停用环境
conda deactivate
```

## 📚 相关文件

- [PyInstaller官方文档](https://pyinstaller.org/)
- [Pygame官方网站](https://www.pygame.org/)
- [Python官方文档](https://docs.python.org/3.9/)

## 📝 许可证

该项目为学习和测试用途。

## 👤 作者

贪吃蛇游戏客户端开发

## 🐛 问题反馈

遇到问题时，请检查：
1. Python版本是否为 3.9+
2. 是否正确初始化了环境
3. 是否所有依赖文件都完整
4. 网络连接是否正常
