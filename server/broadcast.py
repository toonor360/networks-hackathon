import socket
import struct
from time import sleep

from utils import (
    MAGIC_COOKIE,
    OFFER_TYPE,
    TCP_PORT,
    UDP_PORT,
    BROADCAST_PORT,
    print_colored,
    bcolors,
)


def start_broadcast_udp_offers():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.settimeout(0.2)

    offer = struct.pack("!I B H H", MAGIC_COOKIE, OFFER_TYPE, UDP_PORT, TCP_PORT)

    while True:
        udp_socket.sendto(offer, ("<broadcast>", BROADCAST_PORT))
        print_colored(bcolors.OKGREEN, "[Server] UDP offer broadcasted")
        sleep(1)
