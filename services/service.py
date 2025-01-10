from ipaddress import IPv4Address

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self._name = name
        self._ip_addr = ip_addr
        self._port = port

    # Connect method to be implemented for each service
    def connect(self):
        raise NotImplementedError("Connect method should be implemented for each service individually")

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def port(self):
        return self._port

    @property
    def ip_addr(self):
        return self._ip_addr

    def __str__(self) -> str:
        return f"{self.ip_addr}:{self.port} -> {self.name}"
