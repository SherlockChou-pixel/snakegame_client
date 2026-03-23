#此文件用于指定协议
import json
CMD_START = 1    # 开始命令
CMD_MAP = 2      # 地图数据命令
CMD_MOVE = 3     # 移动命令 


class ClientProtocolData:
    """客户端协议数据结构"""
    def __init__(self):
        self.valid = False              # 是否有效
        self.cmd_id = 0                 # 命令ID
        self.status = ""                # 状态（"success", "error", "info"）
        self.data = {}                  # 数据载荷
        self.msg = ""                   # 消息（通常用于错误信息）
        self.error_msg = "" 
class Protocol:
    @staticmethod
    def parse_data(self, data):
        """解析数据"""
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return None
        if not isinstance(data, dict):  # 检查数据是否为字典
            print("数据格式错误，请检查数据格式是否正确")
        # 创建协议数据对象
        protocol_data = ClientProtocolData()

        # 解析数据
        # protocol_data.cmd_id = data.get("cmd_id", 0)

        return data


    @staticmethod
    def get_map():
        """获取地图数据"""
        send_data={
                    "cmd": 2,
                    "data": {}
                    }
        return send_data