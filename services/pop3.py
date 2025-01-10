from ipaddress import IPv4Address
from services.service import Service

class Pop3Service(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("POP3", ip_addr, port)
