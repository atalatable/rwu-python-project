import socket


def scan_ports(ip_addr: str, ports: [int]) -> [int]:
    """Returns the list of open ports among all given ports"""
    open_ports = []

    for port in ports:
        if is_port_open(ip_addr, port):
            open_ports.append(port)

    return open_ports


def is_port_open(ip_addr, port):
    """Returns True if a port is oppened"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip_addr, port))
    sock.close()

    return result == 0
