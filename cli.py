import argparse
import re


def execute_cli() -> str:
    parser = argparse.ArgumentParser(description="Bakebolu")

    # Target ip address or network to scan
    parser.add_argument("target_ip", 
                        type=ip_addr_or_network_validator,
                        help="Ip address or network to scan")

    args = parser.parse_args()

    return args.target_ip

def ip_addr_or_network_validator(address, pat=re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(\/(\d|[12]\d|3[0-2]))?$")):
    """Regex to validate the given ip address"""
    # Regex taken from here https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp?page=1&tab=scoredesc#tab-top
    # And added optional / at the end (from 0 going to 32, based on CIDR)
    if not pat.match(address):
        raise argparse.ArgumentTypeError("invalid ip address or network")
    return address