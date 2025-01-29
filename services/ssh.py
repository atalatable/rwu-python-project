from ipaddress import IPv4Address
from services.service import Service
import paramiko

class SshService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("SSH", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(str(self.ip_addr), port=self.port, username=username, password=password, timeout=5)
            client.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except paramiko.SSHException as e:
            print(f"[SSH ERROR] {e}")
            return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def try_login(self) -> bool:
        
        default_credentials = [("admin", "admin"), ("root", "root"), ("user", "password")]
        for username, password in default_credentials:
            if self.connect(username, password):
                print(f"[+] Default credentials found: {username}/{password}")
                return True
        return False

    def bruteforce(self, username: str, wordlist_path: str) -> bool:
        
        try:
            with open(wordlist_path, "r") as wordlist:
                for password in wordlist:
                    password = password.strip()
                    if self.connect(username, password):
                        print(f"[+] Brute-force success: {username}/{password}")
                        return True
        except FileNotFoundError:
            print("[ERROR] Wordlist file not found.")
        return False