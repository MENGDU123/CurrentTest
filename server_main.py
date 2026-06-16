"""
此程序应当部署于被监听端，也就是服务端。
默认端口为7800，使用TCP协议（国内Qos严重，UDP不易存活）。
"""
import socket
import signal
import psutil
import sys


class BannerServer:
    def __init__(self, listen_ip="0.0.0.0", port=7800):
        self.listen_ip = listen_ip
        self.port = port
        self.server_socket = None
        self.running = True

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.listen_ip, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)

            print(f"[*] Banner Server is running on {self.listen_ip}:{self.port}")
            print("[*] Press Ctrl+C to stop")

            while self.running:
                try:
                    client, addr = self.server_socket.accept()
                    print(f"[+] Heartbeat received from: {addr}")
                    cpu = psutil.cpu_percent(interval=0.1)
                    mem = psutil.virtual_memory().percent
                    swap = psutil.swap_memory().percent
                    banner = (
                        f"200 OK - Heartbeat acknowledged\n"
                        f"CPU: {cpu}%\n"
                        f"Memory: {mem}%\n"
                        f"Swap: {swap}%\n"
                    )
                    client.send(banner.encode())
                    client.close()
                except socket.timeout:
                    continue
                except OSError:
                    break

        except PermissionError:
            print(f"[-] Permission denied.")
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[*] Server stopped")


#此函数用于解决Windows下Ctrl+C失效的问题。
def signal_handler(*args):
    print("\n[*] Shutting down...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    server = BannerServer(listen_ip="127.0.0.1", port=7800)
    server.start()