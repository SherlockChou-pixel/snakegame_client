import socket
import json
import threading
import time


class NetworkManager:
    """
    网络管理器，负责处理与服务器的通信
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.on_receive_callback = None
        self.connected = False

    def connect(self, on_connect=None, on_error=None):
        """
        连接到服务器
        :param on_connect: 连接成功的回调函数
        :param on_error: 连接失败的回调函数
        """
        try:
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(1.0)  # 设置超时
            self.running = True
            self.connected = True
            
            if on_connect:
                on_connect()
            
            # 启动接收数据的线程
            receive_thread = threading.Thread(target=self._receive_loop)
            receive_thread.daemon = True
            receive_thread.start()
            
        except Exception as e:
            self.connected = False
            if on_error:
                on_error(e)

    def disconnect(self):
        """断开连接"""
        self.running = False
        self.connected = False
        self.socket.close()

    def send(self, data):
        """发送数据到服务器"""
        if self.connected:
            try:
                self.socket.send(data.encode())
                return True
            except Exception as e:
                print(f"发送数据失败: {e}")
                self.connected = False
                return False
        return False

    def set_receive_callback(self, callback):
        """设置接收数据的回调函数"""
        self.on_receive_callback = callback

    def _receive_loop(self):
        """接收数据的循环，运行在独立线程中"""
        buffer = ""
        
        while self.running:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if data:
                    buffer += data
                    
                    # 处理可能的多个JSON对象粘包情况
                    while buffer:
                        try:
                            obj, idx = json.JSONDecoder().raw_decode(buffer)
                            # 解析出一个完整的JSON对象
                            if self.on_receive_callback:
                                self.on_receive_callback(obj)
                            
                            # 移除已处理的部分
                            buffer = buffer[idx:].lstrip()
                        except ValueError:
                            # 没有找到完整的JSON对象，等待更多数据
                            break
            except socket.timeout:
                # 超时是正常的，继续循环
                continue
            except Exception as e:
                if self.running:
                    print(f"接收数据时出错: {e}")
                    self.connected = False
                break