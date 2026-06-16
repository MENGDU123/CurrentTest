"""
注意，此脚本还在开发阶段。
由于是初次编写邮件脚本，部分内容由AI生成，请谨慎参考。
"""
from client_main import BannerClient, IPv4Check
import time
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ================== 邮件配置（请根据实际情况修改）==================
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = ""
SENDER_PASSWORD = ""
RECEIVER_EMAIL = ""
# ================================================================

interval = 60  # 扫描间隔（秒）
targets = [  # 被监控的地址列表
    ("127.0.0.1", 7800),
    ("192.168.200.128", 7800)
]


def send_mail(subject: str, content: str):
    """发送邮件通知"""
    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # 启用 TLS 加密
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        print("[Mail] 邮件发送成功")
    except Exception as e:
        print(f"[Mail] 邮件发送失败: {e}")


class MailNotifyingBannerClient(BannerClient):
    def __init__(self, targets, timeout=5.0):
        super().__init__(targets, timeout)
        self.failed_targets = []  # 记录本次扫描失败的目标列表

    def fetch_banner(self, target_ip: str, target_port: int):
        """重写父类方法，捕获失败信息并记录"""
        result = super().fetch_banner(target_ip, target_port)
        if result is None:
            self.failed_targets.append((target_ip, target_port))
        return result

    def run(self):
        """重写 run 方法，在扫描完成后若有失败目标则发送邮件"""
        self.failed_targets.clear()  # 清空上次记录
        super().run()
        if self.failed_targets: #邮件内容
            failed_details = "\n".join([f"{ip}:{port}" for ip, port in self.failed_targets])
            subject = f"[扫描失败] 共 {len(self.failed_targets)} 个目标不可达"
            content = f"以下目标在本次扫描中未能获取 banner：\n{failed_details}"
            send_mail(subject, content)
        else:
            print("[Mail] 本次扫描全部成功，无需发送邮件")


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
    print()

    client = MailNotifyingBannerClient(targets, timeout=2.0)

    while True:
        print(time.ctime())
        client.run()
        time.sleep(interval)