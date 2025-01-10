import socket
import struct

from constants import BROADCAST_PORT, OFFER_TYPE, MAGIC_COOKIE


def listen_for_offers():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind(("", BROADCAST_PORT))
    udp_socket.settimeout(1)
    print("[Client] Listening for server offers...")

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            magic_cookie, message_type, udp_port, tcp_port = struct.unpack(
                "!I B H H", data[:9]
            )
            if magic_cookie == MAGIC_COOKIE and message_type == OFFER_TYPE:
                print(
                    f"[Client] Offer received from {addr[0]}: UDP Port {udp_port}, TCP Port {tcp_port}"
                )
                return addr[0], udp_port, tcp_port
        except socket.timeout:
            continue
