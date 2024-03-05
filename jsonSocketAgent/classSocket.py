import socket

class Socket:

    def __init__(self, ipaddress):
        self.ipaddress = ipaddress
        self.sock = None

    def sockInit(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)