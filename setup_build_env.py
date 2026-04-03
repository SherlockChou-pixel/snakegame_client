"""
初始化打包环境脚本
首次使用时运行此脚本来创建和配置打包环境
"""
import subprocess
import sys


def create_build_environment():
    """创建专用的打包环境"""
    print("正在创建打包环境 'snake_build'...")
    
    # 创建环境
    result = subprocess.run(
        ['conda', 'create', '-n', 'snake_build', '-y', 'python=3.9', 'pyinstaller'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("创建环境失败！")
        print(result.stderr)
        return False
    
    print("✓ 环境创建成功")
    
    # 安装pygame
    print("正在安装依赖包 pygame...")
    result = subprocess.run(
        ['conda', 'run', '-n', 'snake_build', 'pip', 'install', 'pygame'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⚠ pygame 安装可能失败，但这不会影响打包")
    else:
        print("✓ pygame 安装成功")
    
    print("\n✓ 打包环境配置完成！")
    print("现在可以运行: python build_script.py")
    return True


def main():
    print("=" * 50)
    print("贪吃蛇客户端 - 打包环境初始化")
    print("=" * 50)
    print()
    
    if create_build_environment():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
