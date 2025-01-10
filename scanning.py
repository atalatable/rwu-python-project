import socket
import threading
import options
import ipaddress
from concurrent.futures import ThreadPoolExecutor

from services.http import HttpService
from services.ssh import SshService


def scan_network(ip_netw: ipaddress.IPv4Network, ports: list[int]) -> list[dict]:
    out = []
    for ip_addr in ip_netw.hosts():
        if options.VERBOSE:
            print(f"[+] {ip_addr}")
        out.append({
            "ip": ip_addr,
            "open_ports": scan_ports(ip_addr, ports)
        })

    return out

def scan_ports(ip_addr: ipaddress.IPv4Address, ports: list[int]) -> list[dict]:
    """Returns a list of dictionaries with port and service information."""
    results = []
    # Using a lock to safely append to the list while on multiple threads
    lock = threading.Lock()

    def scan_port(port): 
        """Scan a single port and detect its service."""
        if is_port_open(ip_addr, port):
            # TODO Move detect services to another function
            # service = detect_service(ip_addr, port)
            with lock:
                results.append(port)

    # Using ThreadPoolExecutor to limit the number of threads allowed 
    with ThreadPoolExecutor(max_workers=options.MAX_THREADS) as executor:
        for port in ports:
            executor.submit(scan_port, port)

    return results

def is_port_open(
        ip_addr: ipaddress.IPv4Address,
        port: int,
        ) -> bool:
    """Returns True if a port is open"""

    socket_type = socket.SOCK_STREAM
    sock = socket.socket(socket.AF_INET, socket_type)
    sock.settimeout(0.5)  # Set a timeout for faster response
    result = sock.connect_ex((str(ip_addr), port))
    sock.close()

    if options.VERBOSE:
        print(f"[+] {port} : {'opened' if result == 0 else 'closed'}")

    return result == 0

def detect_service(ip_addr: ipaddress.IPv4Address, port: int):
    """Attempt to detect the service running on any given port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((str(ip_addr), port))

            # Attempt to read initial banner
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if banner:
                    if "SSH" in banner.upper():
                        return SshService(ip_addr, port)
                    if "FTP" in banner.upper():
                        return "FTP"
                    if "SMTP" in banner.upper():
                        return "SMTP"
                    if "MySQL" in banner.upper():
                        return "MySQL"
                    if "HTTP" in banner or "<HTML>" in banner.upper():
                        return HttpService(ip_addr, port)
                    return f"Banner Detected: {banner}"
            except socket.timeout:
                pass  
            
            # Fallback: Send an HTTP-like request and analyze response
            sock.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = sock.recv(1024).decode(errors="ignore")
            if "HTTP" in response:
                return HttpService(ip_addr, port)
            if "Not Implemented" in response:
                return HttpService(ip_addr, port)
            if "SMTP" in response:
                return "SMTP"
            if "POP3" in response:
                return "POP3"

            return "Unknown Service"
    except socket.timeout:
        return "No Response (Timeout)"
    except ConnectionRefusedError:
        return "Connection Refused"
    except Exception as e:
        return f"Error: {str(e)}"
