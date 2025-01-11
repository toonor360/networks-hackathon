MAGIC_COOKIE = 0xABCDDCBA
OFFER_TYPE = 0x2
REQUEST_TYPE = 0x3
PAYLOAD_TYPE = 0x4
BROADCAST_PORT = 12347
VERY_SMALL_VALUE = 1e-9


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


def validate_input(prompt, input_type=int, min_value=None, max_value=None):
    while True:
        try:
            value = input_type(input(prompt))
            if (min_value is not None and value < min_value) or (
                max_value is not None and value > max_value
            ):
                raise ValueError
            return value
        except ValueError:
            print_colored(
                bcolors.FAIL,
                f"[Client] Invalid input. Please enter a valid {input_type.__name__}.",
            )
