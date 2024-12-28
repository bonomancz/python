import socket
import ssl
import time
from socket_class import Socket
from thread_class import Thread
from data_class import Data


class Httpd:
    def __init__(self):
        self.__server_host = None
        self.__server_port = None
        self.__private_key = None
        self.__server_cert = None
        self.__sock = Socket()
        self.__thread = Thread()
        self.__data = Data()

    def initialize(self, server_host, server_port, private_key, server_cert) -> None:
        self.__server_host = server_host
        self.__server_port = server_port
        self.__sock.set_server_host(self.__server_host)
        self.__sock.set_server_port(self.__server_port)
        self.__private_key = private_key
        self.__server_cert = server_cert
        self.__sock.initialize()
        self.__sock.setup()
        self.__sock.bind()
        self.__sock.listen()

    def start(self):
        try:
            client_socket = None
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(certfile=self.__server_cert, keyfile=self.__private_key)
            while True:
                try:
                    if client_socket := self.__sock.accept()[0]:
                        ''' detecting SSL client connection '''
                        data = client_socket.recv(1, socket.MSG_PEEK)
                        if data and (data[0] == 0x16):
                            client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
                        self.__thread.start_new_thread(self.handle_client, (client_socket,))
                        self.__thread.remove_finished_threads()
                        #print(self.__thread.get_thread_pool_statistics())
                    else:
                        time.sleep(0.1)
                except Exception as ssl_ex:
                    print(f"Httpd::start(): Exception: {ssl_ex}")
                    if client_socket:
                        self.__sock.close(client_socket)
        except Exception as ex:
            print(f"Httpd::start(): Exception: {ex}")

    def handle_client(self, client_socket):
        try:
            self.__sock.receive(client_socket, self.received_message_handler)
        except Exception  as ex:
            print(f"Httpd::handle_client(): Exception: {ex}")
        finally:
            if client_socket:
                self.__sock.close(client_socket)

    def received_message_handler(self, client_socket, client_received_message):
        if self.__data.is_http_request(client_received_message):
            client_ip_address = self.__sock.get_client_ipaddress(client_socket)
            print(self.__data.get_client_connection_info(client_received_message, client_ip_address))
            self.__sock.send(client_socket, self.__data.get_server_response(client_received_message))
            thread_id = self.__thread.get_current_thread_id()
            self.__thread.set_thread_finished(thread_id)
