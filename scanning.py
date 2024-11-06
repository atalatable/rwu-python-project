import socket
import threading
import options
from concurrent.futures import ThreadPoolExecutor


def scan_ports(
        ip_addr: str,
        ports: list[int],
        max_threads: int = 100,
        ) -> list[int]:
    """Returns the list of open ports among all given ports"""

    open_ports = []
    # Using a lock to safely append to the list
    lock = threading.Lock()

    def scan_port(port):
        """Scan a single port."""
        if is_port_open(ip_addr, port):
            # Use a lock to append to the list safely from different threads
            with lock:
                open_ports.append(port)

    # Using ThreadPoolExecutor to limit the number of threads allowed
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in ports:
            executor.submit(scan_port, port)

    return open_ports


def is_port_open(
        ip_addr,
        port,
        ) -> bool:
    """Returns True if a port is open"""

    socket_type = socket.SOCK_STREAM
    sock = socket.socket(socket.AF_INET, socket_type)
    sock.settimeout(0.5)  # Set a timeout for faster response
    result = sock.connect_ex((ip_addr, port))
    sock.close()

    if options.verbose:
        print(f"[+] {port} : {'opened' if result == 0 else 'closed'}")

    return result == 0
