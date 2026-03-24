import socket
import threading


class NetworkManager:
    """负责与服务器通信。"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.on_receive_callback = None
        self.connected = False
        self._lock = threading.Lock()
        self._create_socket()

    def _create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, on_connect=None, on_error=None):
        """连接到服务器。"""
        with self._lock:
            if self.connected:
                return True

            try:
                try:
                    self.socket.close()
                except OSError:
                    pass

                self._create_socket()
                self.socket.settimeout(3.0)
                self.socket.connect((self.host, self.port))
                self.socket.settimeout(1.0)
                self.running = True
                self.connected = True
            except Exception as e:
                self.running = False
                self.connected = False
                if on_error:
                    on_error(e)
                return False

        if on_connect:
            on_connect()

        receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        receive_thread.start()
        return True

    def disconnect(self):
        """断开连接。"""
        with self._lock:
            self.running = False
            self.connected = False
            try:
                self.socket.close()
            except OSError:
                pass

    def send(self, data):
        """发送数据到服务器。"""
        if not self.connected:
            return False

        try:
            self.socket.send(data.encode())
            return True
        except Exception as e:
            print(f"发送数据失败: {e}")
            self.connected = False
            self.running = False
            return False

    def set_receive_callback(self, callback):
        """设置收到数据时的回调函数。"""
        self.on_receive_callback = callback

    def _receive_loop(self):
        """后台接收数据。"""
        while self.running:
            try:
                data = self.socket.recv(4096).decode("utf-8")
                if not data:
                    self.connected = False
                    self.running = False
                    break

                if self.on_receive_callback:
                    self.on_receive_callback(data)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"接收数据时出错: {e}")
                self.connected = False
                self.running = False
                break
