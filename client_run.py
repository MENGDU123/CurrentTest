from client_main import BannerClient
from client_main import IPv4Check
import time, sys

interval = 15 #可以修改此数值来控制扫描间隔
targets = [ #将被监控的地址列表，可以自由增加与删除目标地址与端口。
    ("127.0.0.1", 7800),
    ("192.168.200.128", 7800),
]

if __name__ == "__main__":
    print("执行IP正确性检查:")
    for ip, port in targets:
        checker = IPv4Check(ip, port)
        is_valid = checker.ipv4_test_1() and checker.ipv4_test_2() and checker.port_test()

        if not is_valid:
            print(f"× 错误：{ip}:{port} 不合法！程序终止。")
            sys.exit(1)
        else:
            print(f"✓ {ip}:{port} - 合法")
    print("✓ 所有IP地址检查通过，开始扫描...")
    print(sep="\n")

    client = BannerClient(targets, timeout=2.0)

    while True:
        print(time.ctime())
        client.run()
        time.sleep(interval)
