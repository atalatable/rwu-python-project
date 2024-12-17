from ipaddress import IPv4Address

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self.name = name
        self.ip_addr = ip_addr
        self.port = port

    # Connect method to be implemented for each service
    def connect(self):
        raise NotImplementedError("Connect method should be implemented for each service individually")

    def __str__(self) -> str:
        return f"{self.ip_addr}:{self.port} -> {self.name}"
