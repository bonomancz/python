from httpd_class import Httpd


def main():
    try:
        httpd = Httpd()
        server_host = "0.0.0.0"
        server_port = 8443
        private_key = "./private.key"
        server_cert = "./server.crt"
        httpd.initialize(server_host, server_port, private_key, server_cert)
        httpd.start()
    except RuntimeError as ex:
        print("fmain(): Exception: {ex}")


if __name__ == "__main__":
    main()