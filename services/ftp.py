from ipaddress import IPv4Address
from services.service import Service
from colorama import Fore, Style
import ftplib
import sys

class FtpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("FTP", ip_addr, port)
        self.ftp = ftplib.FTP()

    def connect(self, username: str, password: str) -> bool:
        try:
            self.ftp.connect(str(self.ip_addr), self.port, timeout=5)
            self.ftp.login(username, password)
            self.ftp.quit()
            return True
        except ftplib.error_perm:
            return False  # Invalid login credentials
        except Exception as e:
            sys.stdout.write("\r" + " " * 50 + "\r")
            sys.stdout.flush()
            print(f"\t[FTP ERROR] {e}")
            return False

    def try_login(self) -> bool:
        # TODO faire anonymous login pas des creds par defaults pour le try_login
        try:
            self.ftp.connect(str(self.ip_addr), self.port, timeout=5)
            response = self.ftp.login("Anonymous", "")
            print(Fore.GREEN + f"\t[+] Anonymous login successful: {response}" + Style.RESET_ALL)
            self.ftp.quit()
            return True
        except ftplib.error_perm:
            print("\t[-] Anonymous login not allowed" + Style.RESET_ALL)
            return False
        except Exception as e:
            print(f"\t[FTP ERROR] {e}")
            return False
