import socket
import subprocess
# Create a raw socket with IPPROTO_IP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

# Bind the socket to the network interface
sock.bind(("your_interface_ip", 0))

# Set the socket to promiscuous mode
sock.ioctl(socket.SIO_SET_PMQ, 1)

while True:
    # Receive a packet
    packet, addr = sock.recvfrom(1024)

    # Check if the packet is an empty UDP packet
    if packet[16:20] == b"\x00\x00\x00\x00" and addr[1] == 5640:
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=", "BlockEmptyUDP", "protocol=", "udp", "dir=", "in", "action=", "block", "remoteip=" + addr[0]])
        print("Empty UDP packet detected from", addr[0])
        


