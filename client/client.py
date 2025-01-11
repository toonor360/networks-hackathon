import threading

from utils import print_colored, bcolors, validate_input
from handlers import perform_tcp_transfer, perform_udp_transfer
from listen import listen_for_offers


"""
Starts the client to perform file transfers using TCP and UDP connections.
Prompts the user to input the file size and the number of TCP and UDP connections.
Listens for server offers to get the server IP, UDP port, and TCP port.
Creates and starts threads for TCP and UDP transfers based on user input.
Waits for all threads to complete before printing a completion message.
Raises:
    ValueError: If the user inputs invalid data for file size or number of connections.
"""


def start_client():
    file_size = validate_input("[Client] Enter file size (in bytes): ", min_value=1)
    tcp_connections = validate_input(
        "[Client] Enter number of TCP connections: ", min_value=0
    )
    udp_connections = validate_input(
        "[Client] Enter number of UDP connections: ", min_value=0
    )

    server_ip, udp_port, tcp_port = listen_for_offers()

    tcp_threads = [
        threading.Thread(
            target=perform_tcp_transfer, args=(server_ip, tcp_port, file_size)
        )
        for _ in range(tcp_connections)
    ]

    for t in tcp_threads:
        t.start()

    udp_threads = [
        threading.Thread(
            target=perform_udp_transfer, args=(server_ip, udp_port, file_size)
        )
        for _ in range(udp_connections)
    ]
    for t in udp_threads:
        t.start()

    for t in tcp_threads + udp_threads:
        t.join()

    print_colored(bcolors.OKGREEN, "[Client] All transfers complete!")
