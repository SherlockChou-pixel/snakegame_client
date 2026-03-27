import json


CMD_JOIN_ROOM = 1
CMD_START_GAME = 2
CMD_GET_MAP = 4
CMD_MOVE = 3


class Protocol:
    @staticmethod
    def parse_data(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError as error:
            print(f"JSON 解析错误: {error}")
            return None

    @staticmethod
    def get_map():
        return {
            "cmd": 3,
            "data": {},
        }

    @staticmethod
    def join_room():
        return {
            "cmd": 1,
            "data": {},
        }

    @staticmethod
    def start_game(room_id):
        return {
            "cmd": 2,
            "data": {"room_id": room_id},
        }

    @staticmethod
    def move(room_id, player_id, direction):
        return {
            "cmd": 3,
            "data": {
                "room_id": room_id,
                "player_id": player_id,
                "direction": direction,
            },
        }
