from ipaddress import IPv4Address
from services.service import Service
from colorama import Fore, Style
import ftplib

class FtpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("FTP", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        try:
            ftp = ftplib.FTP()
            ftp.connect(str(self.ip_addr), self.port, timeout=5)
            ftp.login(username, password)
            ftp.quit()
            return True
        except ftplib.error_perm:
            return False  # Invalid login credentials
        except Exception as e:
            print(f"[FTP ERROR] {e}")
            return False

    def try_login(self) -> bool:
        # TODO faire anonymous login pas des creds par defaults pour le try_login
        
        default_credentials = [("admin", "admin"), ("root", "root"), ("ftp", "ftp"), ("anonymous", "anonymous"), ("bipbip", "superpassword")]
        for username, password in default_credentials:
            if self.connect(username, password):
                print(Fore.GREEN + f"\t[+] Default credentials found: {username}/{password}" + Style.RESET_ALL)
                return True
        return False
