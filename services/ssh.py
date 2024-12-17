from ipaddress import IPv4Address
from services.service import Service

class SshService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("SSH", ip_addr, port)
