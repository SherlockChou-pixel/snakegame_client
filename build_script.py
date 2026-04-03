import os
import subprocess
import shutil
import sys

"""
贪吃蛇客户端自动打包脚本

依赖环境: 需要专用的 conda 环境 'snake_build'
初始化: 首次使用前，运行 python setup_build_env.py
使用: python build_script.py
"""

def clean_build_dirs():
    """清理build和dist目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理 {dir_name} 目录")

def run_pyinstaller(spec_file=None):
    """运行PyInstaller打包"""
    if spec_file and os.path.exists(spec_file):
        cmd = ['conda', 'run', '-n', 'snake_build', 'python', '-m', 'PyInstaller', spec_file]
    else:
        # 默认打包main.py为单文件exe
        cmd = ['conda', 'run', '-n', 'snake_build', 'python', '-m', 'PyInstaller', '--onefile', '--windowed', 'main.py']

    print(f"运行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 打印标准输出（包含pygame的欢迎信息和打包信息）
    if result.stdout:
        print(result.stdout)
    
    # 检查返回码
    if result.returncode == 0:
        print("\n✓ 打包成功!")
    else:
        print("\n✗ 打包失败!")
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        sys.exit(1)

def main():
    # 切换到项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    print("开始自动打包贪吃蛇客户端...")

    # 清理旧的build文件
    clean_build_dirs()

    # 选择spec文件，如果存在的话
    spec_file = 'SnakeGameClient.spec'
    if os.path.exists(spec_file):
        print(f"使用spec文件: {spec_file}")
        run_pyinstaller(spec_file)
    else:
        print("未找到spec文件，使用默认配置打包")
        run_pyinstaller()

    print("打包完成!")
    print("\n注意事项:")
    print("1. 请检查 config.json 中的服务器IP和端口是否正确")
    print("2. 如果要上传到仓库，请确保 config.json 中的敏感信息已移除或设置为默认值")
    print("3. 打包后的exe文件在 dist/ 目录中")

if __name__ == "__main__":
    main()