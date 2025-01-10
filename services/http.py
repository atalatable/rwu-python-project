from ipaddress import IPv4Address
from services.service import Service

class HttpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("HTTP", ip_addr, port)
