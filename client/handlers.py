import socket
import struct
import time

from utils import (
    MAGIC_COOKIE,
    PAYLOAD_TYPE,
    REQUEST_TYPE,
    VERY_SMALL_VALUE,
    print_colored,
    bcolors,
)


def perform_tcp_transfer(server_ip, tcp_port, file_size):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server at the specified IP and port
        tcp_socket.connect((server_ip, tcp_port))

        # Send the file size to the server as a string, encoded as bytes
        # The newline character (\n) might be used as a delimiter for the server to recognize the end of the data
        tcp_socket.send(f"{file_size}\n".encode())

        start_time = time.time()
        received_data = b""

        # Loop until the total data received matches or exceeds the expected file size
        while len(received_data) < file_size:
            # The size of the chunk is the minimum of either the remaining bytes needed or 4096 bytes
            chunk = tcp_socket.recv(min(file_size - len(received_data), 4096))

            # if no data is received (chunk is empty), break the loop. might happen if connection close unexpectedly
            if not chunk:
                break

            received_data += chunk

        elapsed_time = time.time() - start_time

        # Handle the edge case where elapsed_time is 0 (if the transfer is extremely fast)
        if elapsed_time == 0:
            elapsed_time = (
                VERY_SMALL_VALUE  # Set to a very small value to avoid division by zero
            )

        # Calculate the transfer speed in bytes per second
        speed = len(received_data) / elapsed_time

        print_colored(
            bcolors.OKCYAN,
            f"[TCP] Transfer finished: {len(received_data)} bytes in {elapsed_time:.2f} seconds, Speed: {speed:.2f} bytes/sec",
        )

    except (ConnectionRefusedError, ConnectionResetError, socket.timeout):
        # handle exception like server refusing connection, connection reset by peer, or a timeout
        print_colored(bcolors.FAIL, "[TCP] Connection error")

    except Exception as e:
        print_colored(bcolors.FAIL, f"[TCP] Unexpected error: {e}")

    finally:
        # Ensure the socket is closed to release resources,
        tcp_socket.close()


def perform_udp_transfer(server_ip, udp_port, file_size):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Construct a request packet with the required fields
        # "!I B Q" specifies the format for struct.pack (big-endian, integer, byte, and unsigned long long)
        # MAGIC_COOKIE is a predefined constant to identify valid packets
        # REQUEST_TYPE is the type of request (defined elsewhere)
        # file_size is the requested size of the transfer
        request_packet = struct.pack("!I B Q", MAGIC_COOKIE, REQUEST_TYPE, file_size)

        udp_socket.sendto(request_packet, (server_ip, udp_port))
        udp_socket.settimeout(1)  # avoid waiting indefinitely for a response
        start_time = time.time()

        # Initialize variables to track transfer statistics
        received_bytes = 0
        packet_count = 0
        segments_received = 0
        total_segments_value = 0

        # Loop to receive data packets
        while True:
            try:
                # Receive a UDP packet (maximum size of 1024 bytes)
                data, _ = udp_socket.recvfrom(1024)

                # Unpack the first 21 bytes of the received packet to extract metadata
                # "!I B Q Q" unpacks an integer (magic_cookie), a byte (message_type),
                # and two unsigned long long values (total_segments and current_segment)
                magic_cookie, message_type, total_segments, current_segment = (
                    struct.unpack("!I B Q Q", data[:21])
                )

                # validate
                if magic_cookie == MAGIC_COOKIE and message_type == PAYLOAD_TYPE:
                    # Add the size of the payload (data after the first 21 bytes)
                    received_bytes += len(data[21:])
                    packet_count += 1
                    segments_received += 1
                    total_segments_value = total_segments

                # Break if all segments are received
                if current_segment + 1 == total_segments:
                    break

            except socket.timeout:
                # Break the loop if no response is received within the timeout period
                print_colored(
                    bcolors.WARNING, "[UDP] Socket timeout, no more data received."
                )
                break
            except struct.error as e:
                print_colored(bcolors.FAIL, f"[UDP] Error unpacking received data: {e}")
                break
            except Exception as e:
                print_colored(
                    bcolors.FAIL, f"[UDP] Unexpected error during data reception: {e}"
                )
                break

        elapsed_time = time.time() - start_time

        # Handle the edge case where elapsed_time is 0 (if the transfer is very fast)
        if elapsed_time == 0:
            elapsed_time = (
                VERY_SMALL_VALUE  # Set to a very small value to avoid division by zero
            )

        # Calculate the transfer speed in bytes per second
        speed = received_bytes / elapsed_time

        # Calculate the percentage of received packets compared to total segments
        packets_percent = (
            (segments_received / total_segments_value) * 100
            if total_segments_value
            else 0
        )

        # Print a success message with transfer details (bytes, time, speed, packet count, and packet reception percentage)
        print_colored(
            bcolors.OKBLUE,
            f"[UDP] Transfer finished: {received_bytes} bytes in {elapsed_time:.2f} seconds, Speed: {speed:.2f} bytes/sec, Packets: {packet_count}, Packets received: {packets_percent}%",
        )
    except (ConnectionRefusedError, ConnectionResetError, socket.timeout):
        # Handle common connection issues
        print_colored(bcolors.FAIL, "[UDP] Connection error")
    except Exception as e:
        # Handle unexpected errors
        print_colored(bcolors.FAIL, f"[UDP] Unexpected error: {e}")
    finally:
        udp_socket.close()
