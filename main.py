import ast
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

        self.player_id = None
        self.room_id = None
        self.score = 0
        self.snake = []
        self.food = None

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

    def _parse_message_text(self, text):
        text = str(text).strip()
        if not text:
            return None

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            pass

        parsed = protocol.Protocol.parse_data(None, text)
        if isinstance(parsed, dict):
            return parsed
        return None

    def _decode_messages(self, raw_data):
        text = str(raw_data).strip()
        if not text:
            return []

        messages = []

        parsed_whole = self._parse_message_text(text)
        if isinstance(parsed_whole, dict):
            return [parsed_whole]
        if isinstance(parsed_whole, list):
            return [item for item in parsed_whole if isinstance(item, dict)]

        for line in text.splitlines():
            parsed = self._parse_message_text(line)
            if isinstance(parsed, dict):
                messages.append(parsed)
            elif isinstance(parsed, list):
                messages.extend(item for item in parsed if isinstance(item, dict))

        return messages

    def _normalize_food(self, food):
        if not isinstance(food, dict):
            return None
        if "x" not in food or "y" not in food:
            return None
        return {"x": int(food["x"]), "y": int(food["y"])}

    def _sync_ui_player_state(self):
        self.ui.set_snake(self.snake)
        self.ui.set_score(self.score)
        self.ui.set_food(self.food)

    def _handle_join_room(self, result):
        data = result.get("data", {})

        self.player_id = data.get("id", self.player_id)
        self.room_id = data.get("room_id")
        self.score = int(data.get("score", 0) or 0)
        self.snake = data.get("snake", []) or []

        self.ui.update_room(self.room_id, score=self.score, snake=self.snake)
        self.ui.show_message(f"已进入房间 {self.room_id}", color=(60, 160, 90), duration=1800)
        print(f"房间号: {self.room_id}")
        print(f"玩家ID: {self.player_id}")

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

        if "food" in data:
            self.food = self._normalize_food(data.get("food"))

        self._sync_ui_player_state()

    def _extract_local_player_state(self, players):
        if not isinstance(players, list) or not players:
            return None

        if self.player_id is not None:
            for player in players:
                if isinstance(player, dict) and player.get("id") == self.player_id:
                    return player

        first_player = players[0]
        return first_player if isinstance(first_player, dict) else None

    def _handle_game_state_update(self, result):
        if self.room_id is None:
            self.room_id = result.get("room_id")

        player_state = self._extract_local_player_state(result.get("players"))
        if player_state:
            self.player_id = player_state.get("id", self.player_id)
            self.score = int(player_state.get("score", self.score) or 0)
            self.snake = player_state.get("snake_body", []) or []

        if "food" in result:
            self.food = self._normalize_food(result.get("food"))

        self._sync_ui_player_state()

    def _handle_cmd4_message(self, result):
        data = result.get("data", {})
        if not isinstance(data, dict):
            return

        if data.get("type") == "game_state_update":
            self._handle_game_state_update(data)

    def handle_server_data(self, data):
        self.ui.set_connection_status(True)

        for result in self._decode_messages(data):
            print(result)
            if not isinstance(result, dict):
                continue

            cmd = result.get("cmd")
            msg_type = result.get("type")
            status = result.get("status")
            msg = result.get("msg") or result.get("message")

            if status == "error":
                self.ui.show_message(msg or "服务器返回错误", color=(220, 60, 60), duration=2500)
                continue

            if cmd == 1:
                self._handle_join_room(result)
            elif cmd == 2:
                self._handle_map_data(result)
            elif cmd == 4:
                self._handle_cmd4_message(result)
            elif msg_type == "game_state_update":
                self._handle_game_state_update(result)
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
            self._sync_ui_player_state()
            self.ui.show_message("开始游戏，正在加载地图...", color=(70, 70, 70), duration=1800)
            self.request_map(show_feedback=False)
        else:
            print("开始游戏请求发送失败")
            self.ui.show_message("开始游戏请求发送失败", color=(220, 60, 60), duration=2200)

    def send_move(self, direction):
        if self.room_id is None or self.player_id is None:
            self.ui.show_message("房间或玩家信息未准备好", color=(220, 60, 60), duration=1500)
            return

        send_data = protocol.Protocol.move(self.room_id, self.player_id, direction)
        ok = self.send(json.dumps(send_data) + "\n")
        if not ok:
            print("移动指令发送失败")
            self.ui.show_message("移动指令发送失败", color=(220, 60, 60), duration=1500)

    def handle_ui_action(self, action, payload=None):
        if not self.network_manager.connected:
            print(f"点击动作 {action} 时服务器未连接")
            self.show_disconnected_message()
            return

        if action == "join_room":
            self.join_room()
        elif action == "start_game":
            self.start_game()
        elif action == "move":
            direction = None if not isinstance(payload, dict) else payload.get("direction")
            if direction is not None:
                self.send_move(int(direction))
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
