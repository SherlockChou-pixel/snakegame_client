import json
import threading
import time

import protocol
from game_ui import GameUI
from network import NetworkManager


class Client:
    def __init__(self, host, port):
        self.network_manager = NetworkManager(host, port)
        self.running = True
        self.ui = GameUI(on_action=self.handle_ui_action)
        self.ui.set_connection_status(False)
        self.reconnect_interval = 3

        self.room_id = None
        self.score = 0
        self.snake = []

    def show_disconnected_message(self):
        self.ui.set_connection_status(False)
        self.ui.show_message("服务器未连接", color=(220, 60, 60), duration=2500)

    def connect(self, show_success_tip=True, success_message="已连接到服务器", show_error_tip=True):
        def on_connect():
            self.ui.set_connection_status(True)
            print(success_message)
            if show_success_tip:
                self.ui.show_message(success_message, color=(60, 160, 90), duration=1800)

        def on_error(error):
            self.ui.set_connection_status(False)
            print(f"连接服务器失败: {error}")
            if show_error_tip:
                self.show_disconnected_message()

        self.network_manager.set_receive_callback(self.handle_server_data)
        return self.network_manager.connect(on_connect=on_connect, on_error=on_error)

    def auto_reconnect_loop(self):
        while self.running:
            if not self.network_manager.connected:
                self.ui.set_connection_status(False)
                connected = self.connect(
                    show_success_tip=True,
                    success_message="已自动连接到服务器",
                    show_error_tip=False,
                )
                if connected:
                    print("自动重连成功")
            time.sleep(self.reconnect_interval)

    def stop(self):
        self.running = False
        self.ui.running = False

    def _decode_messages(self, raw_data):
        text = str(raw_data).strip()
        if not text:
            return []

        messages = []
        decoder = json.JSONDecoder()
        index = 0

        while index < len(text):
            while index < len(text) and text[index].isspace():
                index += 1

            if index >= len(text):
                break

            try:
                message, end_index = decoder.raw_decode(text, index)
                messages.append(message)
                index = end_index
            except json.JSONDecodeError:
                messages = []
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    parsed = protocol.Protocol.parse_data(None, line)
                    if parsed:
                        messages.append(parsed)
                break

        return messages

    def _handle_join_room(self, result):
        data = result.get("data", {})
        self.room_id = data.get("room_id")
        self.score = int(data.get("score", 0) or 0)
        self.snake = data.get("snake", []) or []

        self.ui.update_room(self.room_id, score=self.score, snake=self.snake)
        self.ui.show_message(f"已进入房间 {self.room_id}", color=(60, 160, 90), duration=1800)
        print(f"房间号: {self.room_id}")

    def _handle_map_data(self, result):
        data = result.get("data", {})
        width = data.get("width")
        height = data.get("height")

        if width is not None and height is not None:
            self.ui.set_map_size(width, height)

        if "snake" in data:
            self.snake = data.get("snake", []) or self.snake

        if "score" in data:
            self.score = int(data.get("score", 0) or 0)

        self.ui.set_snake(self.snake)
        self.ui.set_score(self.score)

    def handle_server_data(self, data):
        self.ui.set_connection_status(True)

        for result in self._decode_messages(data):
            print(result)
            if not isinstance(result, dict):
                continue

            cmd = result.get("cmd")
            status = result.get("status")
            msg = result.get("msg") or result.get("message")

            if status == "error":
                self.ui.show_message(msg or "服务器返回错误", color=(220, 60, 60), duration=2500)
                continue

            if cmd == 1:
                self._handle_join_room(result)
            elif cmd == 2:
                self._handle_map_data(result)
            elif msg:
                self.ui.show_message(msg, color=(70, 70, 70), duration=1800)

    def send(self, message):
        ok = self.network_manager.send(message)
        if not ok:
            self.ui.set_connection_status(False)
        return ok

    def close(self):
        self.ui.set_connection_status(False)
        self.network_manager.disconnect()

    def request_map(self, show_feedback=True):
        send_data = protocol.Protocol.get_map()
        ok = self.send(json.dumps(send_data) + "\n")
        if ok:
            print("已发送地图请求")
            if show_feedback:
                self.ui.show_message("已发送地图请求", color=(70, 70, 70), duration=1500)
        else:
            print("地图请求发送失败")
            self.ui.show_message("地图请求发送失败", color=(220, 60, 60), duration=2200)

    def join_room(self):
        send_data = protocol.Protocol.join_room()
        ok = self.send(json.dumps(send_data) + "\n")
        if ok:
            print("已发送加入房间请求")
            self.ui.show_message("正在加入房间...", color=(70, 70, 70), duration=1500)
        else:
            print("加入房间请求发送失败")
            self.ui.show_message("加入房间请求发送失败", color=(220, 60, 60), duration=2500)

    def start_game(self):
        if self.room_id is None:
            print("请先加入房间")
            self.ui.show_message("请先加入房间", color=(220, 60, 60), duration=2500)
            return

        send_data = protocol.Protocol.start_game(self.room_id)
        ok = self.send(json.dumps(send_data) + "\n")
        if ok:
            print("已发送开始游戏请求")
            self.ui.enter_game_scene()
            self.ui.set_snake(self.snake)
            self.ui.set_score(self.score)
            self.ui.show_message("开始游戏，正在加载地图...", color=(70, 70, 70), duration=1800)
            self.request_map(show_feedback=False)
        else:
            print("开始游戏请求发送失败")
            self.ui.show_message("开始游戏请求发送失败", color=(220, 60, 60), duration=2200)

    def handle_ui_action(self, action):
        action_map = {
            "join_room": self.join_room,
            "start_game": self.start_game,
        }

        if not self.network_manager.connected:
            print(f"点击动作 {action} 时服务器未连接")
            self.show_disconnected_message()
            return

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
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n正在退出程序...")
                self.stop()
                break

    def run(self):
        connected = self.connect(show_success_tip=False)
        if connected:
            print("连接已建立，输入 'quit'、'exit' 或 'q' 退出程序")
        else:
            print("未连接到服务器，界面将继续打开，可稍后重试")
            self.show_disconnected_message()

        input_thread = threading.Thread(target=self.handle_user_input, daemon=True)
        reconnect_thread = threading.Thread(target=self.auto_reconnect_loop, daemon=True)
        input_thread.start()
        reconnect_thread.start()

        try:
            self.ui.run()
        except Exception as e:
            print(f"运行过程中出现异常: {e}")
        finally:
            self.stop()
            self.close()
            input_thread.join(timeout=1)
            reconnect_thread.join(timeout=1)
            print("程序已退出")


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888)
    client.run()
