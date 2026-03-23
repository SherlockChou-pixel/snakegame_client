import protocol
import sys
import threading
import time
from network import NetworkManager


class Client:
    def __init__(self, host, port):
        self.network_manager = NetworkManager(host, port)
        self.running = True

    def connect(self):
        def on_connect():
            print("已连接到服务器")
        
        def on_error(error):
            print(f"连接服务器失败: {error}")
        
        self.network_manager.set_receive_callback(self.handle_server_data)
        self.network_manager.connect(on_connect=on_connect, on_error=on_error)

    def handle_server_data(self, data):
        """处理从服务器接收到的数据"""
        protocol.Protocol.parse_data(None, str(data))
        print(data)

    def send(self, message):
        return self.network_manager.send(message)

    def close(self):
        self.network_manager.disconnect()

    def handle_user_input(self):
        """处理用户输入的线程函数"""
        while self.running:
            try:
                user_input = input().strip().lower()
                if user_input in ['quit', 'exit', 'q', 'Q']:
                    print("正在退出程序...")
                    self.running = False
                    self.network_manager.disconnect()
                    break
            except EOFError:
                # 输入流结束
                break
            except KeyboardInterrupt:
                print("\n正在退出程序...")
                self.running = False
                self.network_manager.disconnect()
                break

    def run(self):
        self.connect()
        print("连接已建立，输入 'quit'、'exit' 或 'q' 退出程序")
        
        # 启动用户输入处理线程
        input_thread = threading.Thread(target=self.handle_user_input)
        input_thread.daemon = True
        input_thread.start()
        
        # 主循环 - 监控运行状态
        while self.running:
            time.sleep(0.1)  # 短暂休眠，减少CPU使用

        # 等待输入线程结束
        input_thread.join(timeout=1)  # 最多等待1秒
        self.close()


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888)
    client.run()