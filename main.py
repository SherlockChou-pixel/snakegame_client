import socket
import protocol
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, message):
        self.socket.send(message.encode())

    def receive(self):
        pass

    def close(self):
        self.socket.close()


    def run(self):
        self.connect()
        while True:
            data = self.socket.recv(4096).decode('utf-8')
            if not data:
                break
            protocol.Protocol.parse(data)
            print(data)
            
        self.close()
if __name__ == "__main__":
    client = Client("127.0.0.1", 8888)
    client.run()
