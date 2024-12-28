import re
from time_class import Time


class Data:

    def __init__(self):
        self.__tm = Time()

    def is_http_request(self, input_string) -> bool:
        http_request_pattern = r"^(GET|POST|PUT|DELETE|PATCH|HEAD|TRACE|CONNECT|OPTIONS) .+ HTTP/\d\.\d"
        return re.match(http_request_pattern, input_string) is not None

    def get_client_connection_info(self, client_received_message, client_ip_address) -> str:
        client_data_list = client_received_message.split("\r\n")
        get_target = "".join(filter(lambda x: "GET" in x, client_data_list)).split()
        client_data_list = list(filter(lambda x: "Host" in x or "User-Agent" in x, client_data_list))
        client_data = {record[0]: "".join(record[1]).strip() for record in list(x.split(":") for x in client_data_list)}
        client_data["Action"] = get_target[0].strip()
        client_data["Target"] = get_target[1].strip()
        return f"{self.__tm.get_milliseconds_datetime()} Client connected ({str(client_ip_address)}, {client_data["User-Agent"]}). Action: {client_data["Action"]} {client_data["Target"]}"

    def get_server_response(self, client_received_message) -> str:
        client_data_list = client_received_message.split("\r\n")
        get_target = "".join(filter(lambda x: "GET" in x, client_data_list)).split()
        client_data_list = list(filter(lambda x: "Host" in x or "User-Agent" in x, client_data_list))
        client_data = {record[0]: "".join(record[1]).strip() for record in list(x.split(":") for x in client_data_list)}
        client_data["Action"] = get_target[0].strip()
        client_data["Target"] = get_target[1].strip()
        # ENDPOINTS
        http_response = lambda color, http_status: "<html><head><style>body{color: " + color + "; font-family: Tahoma; font-size: 14px;}</style></head><body><h1>HTTP server response: " + http_status + "</h1></body></html>"
        http_status = "HTTP/1.1 200 OK"
        if client_data["Target"] == "/":
            response_body = http_response("green", http_status)
        elif client_data["Target"] == "/test":
            response_body = http_response("green", http_status)
        elif client_data["Target"] == "/testjson" or client_data["Target"] == "/json":
            response_body = "{\"name\":\"John\", \"age\":30, \"car\":null}"
        else:
            http_status = "HTTP/1.1 404 Not Found"
            response_body = http_response("red", http_status)
        response = (
            f"{http_status}\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_body}"
        )
        return response