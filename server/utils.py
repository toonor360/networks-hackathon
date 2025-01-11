MAGIC_COOKIE = 0xABCDDCBA
OFFER_TYPE = 0x2
REQUEST_TYPE = 0x3
PAYLOAD_TYPE = 0x4
TCP_PORT = 12346
UDP_PORT = 12345
BROADCAST_PORT = 12347
PAYLOAD_SIZE = 1024
DATA_PAYLOAD_SIZE = PAYLOAD_SIZE - 21


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(color: bcolors, message):
    print(f"{color}{message}{bcolors.ENDC}")
