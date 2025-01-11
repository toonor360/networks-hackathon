import socket
import struct
from utils import (
    MAGIC_COOKIE,
    REQUEST_TYPE,
    PAYLOAD_TYPE,
    DATA_PAYLOAD_SIZE,
    print_colored,
    bcolors,
)


def handle_tcp_client(client_socket: socket.socket):
    # decoded and converted requested form client to an integer
    file_size = int(client_socket.recv(1024).decode().strip())

    print_colored(bcolors.OKCYAN, f"[TCP] Client requested {file_size} bytes")

    # Send the requested number of bytes back to the client
    client_socket.send(b"X" * file_size)
    client_socket.close()


def handle_udp_client(udp_socket: socket.socket):
    #  listen for incoming UDP requests
    while True:
        # receive data from the client
        data, addr = udp_socket.recvfrom(1024)

        # Unpack the first 13 bytes of the received data
        # '!I B Q' specifies the format: integer (magic_cookie), byte (message_type), and unsigned long long (file_size)
        magic_cookie, message_type, file_size = struct.unpack("!I B Q", data[:13])

        if magic_cookie == MAGIC_COOKIE and message_type == REQUEST_TYPE:
            print_colored(bcolors.OKBLUE, f"[UDP] Received request from {addr}")
            print_colored(bcolors.OKBLUE, f"[UDP] Client requested {file_size} bytes")

            # Calculate the total number of segments needed for the request
            total_segments = (file_size + DATA_PAYLOAD_SIZE - 1) // DATA_PAYLOAD_SIZE

            # Send the data to the client in segments
            for segment in range(total_segments):
                # Calculate the size of the current data payload
                data_payload = b"X" * min(
                    DATA_PAYLOAD_SIZE, file_size - (segment * DATA_PAYLOAD_SIZE)
                )

                # Create the payload packet
                # The packet consists of a header (magic_cookie, payload type, total segments, current segment index)
                payload_packet = (
                    struct.pack(
                        "!I B Q Q", MAGIC_COOKIE, PAYLOAD_TYPE, total_segments, segment
                    )
                    + data_payload
                )

                # Send the packet to the client
                udp_socket.sendto(payload_packet, addr)

                print_colored(
                    bcolors.OKBLUE,
                    f"[UDP] Sent segment {segment + 1}/{total_segments} to {addr}",
                )

            print_colored(bcolors.OKBLUE, f"[UDP] Completed transfer to {addr}")
        else:
            # Ignore packets that do not match the expected format
            continue
