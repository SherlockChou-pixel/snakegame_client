import json
import threading

import protocol
from game_ui import GameUI
from network import NetworkManager


class Client:
    def __init__(self, host, port):
        self.network_manager = NetworkManager(host, port)
        self.running = True
        self.ui = GameUI(on_action=self.handle_ui_action)

    def connect(self):
        def on_connect():
            print("已连接到服务器")

        def on_error(error):
            print(f"连接服务器失败: {error}")

        self.network_manager.set_receive_callback(self.handle_server_data)
        return self.network_manager.connect(on_connect=on_connect, on_error=on_error)

    def stop(self):
        self.running = False
        self.ui.running = False

    def handle_server_data(self, data):
        result = protocol.Protocol.parse_data(None, str(data))
        if not result:
            return

        if result.get("cmd") == 2:
            map_data = result.get("data", {})
            print(map_data)

            width = map_data.get("width")
            height = map_data.get("height")
            if width is not None and height is not None:
                self.ui.set_map_size(width, height)
                print(f"已更新地图显示: {width} x {height}")

    def send(self, message):
        return self.network_manager.send(message)

    def close(self):
        self.network_manager.disconnect()

    def request_map(self):
        send_data = protocol.Protocol.get_map()
        ok = self.send(json.dumps(send_data) + "\n")
        if ok:
            print("已发送地图请求")
        else:
            print("地图请求发送失败")

    def handle_ui_action(self, action):
        action_map = {
            "get_map": self.request_map,
        }

        handler = action_map.get(action)
        if handler:
            handler()
        else:
            print(f"未处理的界面动作: {action}")

    def handle_user_input(self):
        while self.running:
            try:
                user_input = input().strip().lower()
                if user_input in ["quit", "exit", "q"]:
                    print("正在退出程序...")
                    self.stop()
                    break

                if user_input == "2":
                    self.request_map()
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n正在退出程序...")
                self.stop()
                break

    def run(self):
        if not self.connect():
            return

        print("连接已建立，输入 'quit'、'exit' 或 'q' 退出程序")

        input_thread = threading.Thread(target=self.handle_user_input, daemon=True)
        input_thread.start()

        try:
            self.ui.run()
        except Exception as e:
            print(f"运行过程中出现异常: {e}")
        finally:
            self.stop()
            self.close()
            input_thread.join(timeout=1)
            print("程序已退出")


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888)
    client.run()
