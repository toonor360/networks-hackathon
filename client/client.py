import threading

from handlers import perform_tcp_transfer, perform_udp_transfer
from listen import listen_for_offers


def start_client():
    file_size = int(input("[Client] Enter file size (in bytes): "))
    tcp_connections = int(input("[Client] Enter number of TCP connections: "))
    udp_connections = int(input("[Client] Enter number of UDP connections: "))

    server_ip, udp_port, tcp_port = listen_for_offers()

    tcp_threads = []
    for i in range(tcp_connections):
        t = threading.Thread(
            target=perform_tcp_transfer, args=(server_ip, tcp_port, file_size)
        )
        tcp_threads.append(t)
        t.start()

    udp_threads = []
    for i in range(udp_connections):
        t = threading.Thread(
            target=perform_udp_transfer, args=(server_ip, udp_port, file_size)
        )
        udp_threads.append(t)
        t.start()

    for t in tcp_threads + udp_threads:
        t.join()

    print("[Client] All transfers complete!")
