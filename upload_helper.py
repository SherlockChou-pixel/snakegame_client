"""
自动上传脚本（可选）

如果你有服务器或想手动上传，可以使用这个脚本快速打包和准备文件。

使用方法:
    python upload_helper.py

这会生成一个带时间戳的版本文件夹，方便管理和上传。
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime


def get_version_info():
    """获取版本信息"""
    # 从git标签获取最新版本
    try:
        result = subprocess.run(['git', 'describe', '--tags'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 如果没有标签，使用时间戳
    return f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def build_package():
    """打包应用"""
    print("开始打包应用...")
    
    result = subprocess.run(['python', 'build_script.py'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ 打包失败!")
        print(result.stderr)
        return False
    
    print("✓ 打包成功")
    return True


def create_release_folder(version):
    """创建发布文件夹"""
    release_folder = f"releases/{version}"
    
    # 清理旧文件夹
    if os.path.exists(release_folder):
        shutil.rmtree(release_folder)
    
    # 创建新文件夹
    os.makedirs(release_folder, exist_ok=True)
    
    # 复制exe文件
    if os.path.exists('dist/SnakeGameClient.exe'):
        shutil.copy('dist/SnakeGameClient.exe', 
                   f'{release_folder}/SnakeGameClient.exe')
        print(f"✓ 文件已保存到: {release_folder}/")
        return release_folder
    else:
        print("❌ 找不到dist/SnakeGameClient.exe")
        return None


def create_manifest(version, release_folder):
    """创建文件清单"""
    manifest = f"""{version} 版本文件清单

打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

文件列表:
- SnakeGameClient.exe (游戏程序)

安装说明:
1. 下载 SnakeGameClient.exe
2. 双击运行即可
3. 修改 config.json 设置服务器地址（如需要）

"""
    
    manifest_path = f'{release_folder}/README.txt'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest)
    
    print(f"✓ 已生成清单文件")


def main():
    print("=" * 50)
    print("打包并准备上传")
    print("=" * 50)
    print()
    
    # 获取版本信息
    version = get_version_info()
    print(f"版本: {version}\n")
    
    # 打包
    if not build_package():
        sys.exit(1)
    
    print()
    
    # 创建发布文件夹
    release_folder = create_release_folder(version)
    if not release_folder:
        sys.exit(1)
    
    print()
    
    # 创建清单
    create_manifest(version, release_folder)
    
    print()
    print("=" * 50)
    print("✅ 准备完成!")
    print("=" * 50)
    print(f"\n文件位置: {release_folder}/")
    print("\n后续操作:")
    print("1. 手动上传此文件夹到服务器/网盘")
    print("2. 或者使用 Git tag 和 GitHub Actions 自动发布")
    print()
    print("更多信息: 查看 RELEASE.md")


if __name__ == "__main__":
    main()
