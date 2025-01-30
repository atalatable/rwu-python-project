from ipaddress import IPv4Address
from colorama import Fore, Style
import os
import sys

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self._name = name
        self._ip_addr = ip_addr
        self._port = port

    # Connect method to be implemented for each service
    def connect(self, username: str, password=None) -> bool:
        raise NotImplementedError("connect method should be implemented for each service individually")

    # Try login method to be implemented for each service
    # Should try default credentials, anonymous login, ...
    def try_login(self):
        raise NotImplementedError("try_login method should be implemented for each service individually")

    def bruteforce(self) -> bool:
        username = "baptiste"  # TODO: Hardcoded for now, ask the user?
        wordlist_path = os.path.join(os.path.dirname(__file__), "wordlists", "ftp-wordlist.txt")

        attempt_count = 0

        try:
            with open(wordlist_path, "r") as wordlist:
                passwords = wordlist.readlines()
                total_attempts = len(passwords)

                for password in passwords:
                    password = password.strip()
                    attempt_count += 1

                    sys.stdout.write(f"\r\t[*] Bruteforce Attempts: {attempt_count}/{total_attempts}")
                    sys.stdout.flush()

                    if self.connect(username, password):
                        sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite with spaces
                        sys.stdout.flush()
                        print(Fore.GREEN + f"\t[+] Brute-force success: {username}/{password}" + Style.RESET_ALL)
                        return True

            sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite with spaces
            sys.stdout.flush()
            print("\t[-] Brute-force attempt finished, no valid credentials found.")
        except FileNotFoundError:
            print("\t[ERROR] Wordlist file not found at", wordlist_path)
        
        return False

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
