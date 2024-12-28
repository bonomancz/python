import socket
import select

class Socket:
    def __init__(self):
        self.__server_socket = None
        self.__server_host = None
        self.__server_port = None

    def initialize(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup(self):
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self):
        self.__server_socket.bind((self.__server_host, self.__server_port))

    def listen(self):
        self.__server_socket.listen()

    def accept(self):
        return self.__server_socket.accept()

    def receive(self, client_socket, on_message_received):
        with (client_socket):
            buffer_size = 8192
            buffer = ""
            while True:
                try:
                    sock_ready_to_read, _, _ = select.select([client_socket], [], [], 0.5)
                    if sock_ready_to_read:
                        if not (received := client_socket.recv(buffer_size)):
                            break
                        try:
                            received_data = received.decode("UTF-8")
                            buffer = buffer.join(received_data.strip())
                            if "\r\n\r\n" in received_data:
                                if "User-Agent:" in received_data:
                                    on_message_received(client_socket, received_data)
                                else:
                                    raise RuntimeError("Received not an http request.")

                        except Exception as ex:
                            print(f"Client probably forcibly disconnected.\nInvalid utf-8 data received. Exception: {ex}")
                            break

                except ConnectionAbortedError:
                    print("Client forcibly closed the connection")
                    break

    def send(self, client_socket, send_message) -> None:
        try:
            client_socket.sendall(send_message.encode("UTF-8"))
        except socket.error as se:
            print(f"Socket::send(): Exception: {se}")

    def close(self, client_socket) -> None:
        client_socket.close()

    def get_client_ipaddress(self, client_socket) -> str:
        return str(client_socket.getpeername()[0])

    def set_server_host(self, server_host):
        self.__server_host = server_host

    def set_server_port(self, server_port):
        self.__server_port = server_port
