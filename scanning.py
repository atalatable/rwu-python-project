import socket


def scan_ports(ip_addr: str, ports: [int]) -> [int]:
    """Returns the list of open ports among all given ports"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    open_ports = []

    for port in ports:
        print(port)
        if is_port_open(ip_addr, port, sock):
            open_ports.append(port)

    sock.close()

    return open_ports


def is_port_open(ip_addr, port, sock):
    """Returns True if a port is oppened"""
    result = sock.connect_ex((ip_addr, port))

    return result == 0
