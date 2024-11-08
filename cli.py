import argparse
import re
import options


def initialize():
    parser = argparse.ArgumentParser(description="Bakebolu")

    # Target ip address or network to scan
    parser.add_argument("target_ip",
                        type=ip_addr_or_network_validator,
                        help="Ip address or network to scan")

    # Port range to scan 0-9999 default
    parser.add_argument("-p", "--port-range",
                        type=port_range_validator,
                        default=(0, 9999),
                        help="Port range to scan, e.g. 0-9999")

    # Verbose flag
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()

    options.verbose = args.verbose
    options.target_ip = args.target_ip
    options.start_port, options.end_port = args.port_range


def ip_addr_or_network_validator(
        address,
        pat=re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(\/(\d|[12]\d|3[0-2]))?$")):
    """Regex to validate the given ip address"""
    # Regex taken from here https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp?page=1&tab=scoredesc#tab-top
    # And added optional / at the end (from 0 going to 32, based on CIDR)
    if not pat.match(address):
        raise argparse.ArgumentTypeError("invalid ip address or network")
    return address


def port_range_validator(port_range, pat=re.compile(r"^(\d+)-(\d+)$")):
    """Regex to validate the given port range"""
    match = pat.match(port_range)

    if not match:
        raise argparse.ArgumentTypeError("invalid port range")

    # Extract the port from the regex
    start_port, end_port = int(match.group(1)), int(match.group(2))

    # Check that given range is valid
    if not (0 <= start_port <= 65535 and
            0 <= end_port <= 65535 and
            start_port <= end_port):
        raise argparse.ArgumentTypeError(
                "Ports must be between 0 and 65535, and start must be <= end")

    return (start_port, end_port)
