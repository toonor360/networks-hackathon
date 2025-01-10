import socket
import threading

from broadcast import start_broadcast_udp_offers
from constants import TCP_PORT, UDP_PORT
from handlers import handle_tcp_client, handle_udp_client


def start_server():
    threading.Thread(target=start_broadcast_udp_offers, daemon=True).start()

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", TCP_PORT))
    tcp_socket.settimeout(1)
    tcp_socket.listen()
    print(f"[TCP] Server listening on port {TCP_PORT}")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("", UDP_PORT))
    threading.Thread(target=handle_udp_client, args=(udp_socket,), daemon=True).start()

    while True:
        try:
            client_socket, addr = tcp_socket.accept()
            print(f"[TCP] Connection from {addr}")
            threading.Thread(
                target=handle_tcp_client, args=(client_socket,), daemon=True
            ).start()
        except socket.timeout:
            continue
