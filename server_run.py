from server_main import BannerServer

listen_ip = "127.0.0.1"
port = 7800

if __name__ == "__main__":
    server = BannerServer(listen_ip, port)
    server.start()
