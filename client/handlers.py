# Perform TCP Transfer
import socket
import struct
import time

from constants import MAGIC_COOKIE, PAYLOAD_TYPE, REQUEST_TYPE


def perform_tcp_transfer(server_ip, tcp_port, file_size):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((server_ip, tcp_port))
    tcp_socket.send(f"{file_size}\n".encode())

    start_time = time.time()
    received_data = tcp_socket.recv(file_size)
    elapsed_time = time.time() - start_time
    speed = len(received_data) / elapsed_time

    print(
        f"[TCP] Transfer finished: {len(received_data)} bytes in {elapsed_time:.2f} seconds, Speed: {speed:.2f} bytes/sec"
    )
    tcp_socket.close()


def perform_udp_transfer(server_ip, udp_port, file_size):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    request_packet = struct.pack("!I B Q", MAGIC_COOKIE, REQUEST_TYPE, file_size)
    udp_socket.sendto(request_packet, (server_ip, udp_port))
    udp_socket.settimeout(1)

    start_time = time.time()
    received_bytes = 0
    packet_count = 0
    segments_received = 0
    total_segments_value = 0

    while True:
        try:
            data, _ = udp_socket.recvfrom(1024)
            magic_cookie, message_type, total_segments, current_segment = struct.unpack(
                "!I B Q Q", data[:21]
            )
            if magic_cookie == MAGIC_COOKIE and message_type == PAYLOAD_TYPE:
                received_bytes += len(data[21:])
                packet_count += 1
                segments_received += 1
                total_segments_value = total_segments

            if current_segment + 1 == total_segments:
                break
        except socket.timeout:
            break

    elapsed_time = time.time() - start_time
    speed = received_bytes / elapsed_time
    packets_percent = (segments_received / total_segments_value) * 100

    print(
        f"[UDP] Transfer finished: {received_bytes} bytes in {elapsed_time:.2f} seconds, Speed: {speed:.2f} bytes/sec, Packets: {packet_count}, Packets received: {packets_percent}%"
    )
    udp_socket.close()
