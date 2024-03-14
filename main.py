import socket
import subprocess

# IPPROTO_IPプロトコルを使用したrawソケットを作成します
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

# ソケットをネットワークインターフェースにバインドします
sock.bind(("0.0.0.0", 5640))

# ソケットをプロミスキャスモードに設定します
sock.ioctl(socket.SIO_SET_PMQ, 1)

while True:
    # パケットを受信します
    packet, addr = sock.recvfrom(1024)

    # パケットの宛先IPアドレスが192.168.1.200であるか確認します
    if addr[0] == '192.168.1.200':
        # パケットが空のUDPパケットかどうかを確認します
        if packet[16:20] == b"\x00\x00\x00\x00" and addr[1] == 5640:
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=", "BlockEmptyUDP", "protocol=", "udp", "dir=", "in", "action=", "block", "remoteip=" + addr[0]])
            print("空のUDPパケットが", addr[0], "から検出されました")
