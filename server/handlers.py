import socket
import struct
from constants import (
    MAGIC_COOKIE,
    REQUEST_TYPE,
    PAYLOAD_TYPE,
    PAYLOAD_SIZE,
    DATA_PAYLOAD_SIZE,
)


def handle_tcp_client(client_socket: socket.socket):
    file_size = int(client_socket.recv(1024).decode().strip())
    print(f"[TCP] Client requested {file_size} bytes")
    client_socket.send(b"X" * file_size)
    client_socket.close()


def handle_udp_client(udp_socket: socket.socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)
        magic_cookie, message_type, file_size = struct.unpack("!I B Q", data[:13])

        if magic_cookie == MAGIC_COOKIE and message_type == REQUEST_TYPE:
            print(f"[UDP] Received request from {addr}")
            print(f"[UDP] Client requested {file_size} bytes")

            total_segments = (file_size + DATA_PAYLOAD_SIZE - 1) // DATA_PAYLOAD_SIZE

            print(total_segments)
            for segment in range(total_segments):
                # Construct payload packet
                data_payload = b"X" * min(
                    DATA_PAYLOAD_SIZE, file_size - (segment * DATA_PAYLOAD_SIZE)
                )
                payload_packet = (
                    struct.pack(
                        "!I B Q Q", MAGIC_COOKIE, PAYLOAD_TYPE, total_segments, segment
                    )
                    + data_payload
                )

                # Send the packet to the client
                udp_socket.sendto(payload_packet, addr)
                print(f"[UDP] Sent segment {segment + 1}/{total_segments} to {addr}")

            print(f"[UDP] Completed transfer to {addr}")
        else:
            continue
