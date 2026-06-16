"""
BannerClient - 批量探测多个 BannerServer 服务端
支持传入目标列表，每个元素为 (ip, port) 元组
"""
from typing import List, Tuple, Optional
import socket
import sys



class BannerClient:
    def __init__(self, targets: List[Tuple[str, int]], timeout: float = 5.0):
        self.targets = targets
        self.timeout = timeout

    def fetch_banner(self, target_ip: str, target_port: int) -> Optional[str]:
        #banner探测模块
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((target_ip, target_port))
            data = sock.recv(1024)
            sock.close()
            return data.decode('utf-8', errors='ignore')
        except socket.timeout:
            print(f"[-] {target_ip}:{target_port} - 连接超时！ Timeout")
        except ConnectionRefusedError:
            print(f"[-] {target_ip}:{target_port} - 拒绝请求！ Connection refused")
        except Exception as e:
            print(f"[-] {target_ip}:{target_port} - 发生错误！ Error: {e}")
        return None

    def run(self):
        #依次扫描target列表中的IP地址与端口。
        if not self.targets:
            print("[!] No targets specified.")
            return
        print(f"[*] Starting scan for {len(self.targets)} target(s), timeout={self.timeout}s")
        for ip, port in self.targets:
            banner = self.fetch_banner(ip, port)
            if banner is not None:
                print(f"[+] {ip}:{port} -> {banner}")
        print("[*] 本轮扫描完成。 Scan finished.")

class IPv4Check:
    def __init__(self, ipaddress: str, port: int):
        self.ip = ipaddress
        self.port = port

    def ipv4_test_1(self):
        # 检查地址是否为点分十进制
        parts = self.ip.split(".")
        if len(parts) != 4:
            print("IP地址不合法，正确的形式应为‘x.x.x.x’!")
            return False
        return True

    def ipv4_test_2(self):
        # 检查地址是否符合IPv4范围（非网络地址或者广播）
        parts = self.ip.split(".")
        for part in parts:
            if not part.isdigit():
                print("IP地址不合法！正确的范围应为（1~254.1~254.1~254.1~254）")
                return False
            if int(part) > 254 or int(part) < 0:
                print("IP地址不合法！正确的范围应为（0~254.0~254.0~254.0~254）")
                return False
        return True

    def port_test(self):
        if self.port > 65535 or self.port < 0:
            return False
        return True

def main():
    #提示代码，翻译由AI提供。
    """
    示例：直接从命令行参数读取（单目标或手动解析多个）
    简单起见：如果提供了多个 ip:port 对（如 192.168.1.1:7800 192.168.1.2:7800）
    这里演示一个批量解析方法，也可以支持从文件读取。
    """
    if len(sys.argv) < 2:
        print("示例命令：")
        print("  检测单个IP地址: python banner_client.py 127.0.0.1 7800")
        print("  检测多个IP地址: python banner_client.py 192.168.1.1:7800 192.168.1.2:7800 ...")
        print("  或者你也可以通过创建client_run来持续检测。")
        print("Usage:")
        print("  Single target: python banner_client.py <ip> [port]")
        print("  Multiple targets: python banner_client.py ip1:port1 ip2:port2 ...")
        print("  Or edit the script to provide a list directly.")
        sys.exit(1)

    targets = []
    #此段代码用于读取参数中冒号的前后两部分，分割IP与端口。
    for arg in sys.argv[1:]:
        if ':' in arg:
            ip, port_str = arg.split(':', 1)
            try:
                port = int(port_str)
                targets.append((ip, port))
            except ValueError:
                print(f"[-] Invalid port in {arg}, skipping")
        else:
            targets.append((arg, 7800))

    if not targets:
        print("[-] No valid targets.")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2].isdigit():
        targets = [(sys.argv[1], int(sys.argv[2]))]

    client = BannerClient(targets, timeout=3.0)
    client.run()


if __name__ == "__main__":
    main()