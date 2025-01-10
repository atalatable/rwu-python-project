from ipaddress import IPv4Address

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self._name = name
        self._ip_addr = ip_addr
        self._port = port

    # Connect method to be implemented for each service
    def connect(self, username: str, password=None):
        raise NotImplementedError("connect method should be implemented for each service individually")

    # Try login method to be implemented for each service
    # Should try default credentials, anonymous login, ...
    def try_login(self):
        raise NotImplementedError("try_login method should be implemented for each service individually")

    # Bruteforce method to be implemented for each service
    def bruteforce(self):
        raise NotImplementedError("bruteforce method should be implemented for each service individually")

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
