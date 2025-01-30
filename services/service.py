from ipaddress import IPv4Address
from colorama import Fore, Style
import os
import sys
import queue
import threading

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self._name = name
        self._ip_addr = ip_addr
        self._port = port
        self.queue = queue.Queue()
        self.found = False  # Stop flag when credentials are found
        self.lock = threading.Lock()  # Lock for synchronized printing

    # Connect method to be implemented for each service
    def connect(self, username: str, password=None) -> bool:
        raise NotImplementedError("connect method should be implemented for each service individually")

    # Try login method to be implemented for each service
    # Should try default credentials, anonymous login, ...
    def try_login(self):
        raise NotImplementedError("try_login method should be implemented for each service individually")

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

    def worker(self, username: str, total_attempts: int):
        """ Worker thread function to test passwords from the queue """
        while not self.queue.empty() and not self.found:
            password = self.queue.get()
            attempt_count = total_attempts - self.queue.qsize()

            # Print progress safely
            with self.lock:
                sys.stdout.write(f"\r\t[*] Bruteforce Attempts: {attempt_count}/{total_attempts}")
                sys.stdout.flush()

            if self.connect(username, password):
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
                print(Fore.GREEN + f"\t[+] Brute-force success: {username}/{password}" + Style.RESET_ALL)
                self.found = True
                self.queue.queue.clear()  # Clear remaining tasks to stop other threads
                break  

            self.queue.task_done()

    def bruteforce(self):
        """ Multi-threaded brute-force attack """

        username = "baptiste"  # TODO: Hardcoded for now, ask the user?
        wordlist_path = os.path.join(os.path.dirname(__file__), "../test_lab", "wordlist.txt")

        try:
            with open(wordlist_path, "r") as wordlist:
                passwords = [line.strip() for line in wordlist if line.strip()]
                total_attempts = len(passwords)

                if total_attempts == 0:
                    print(Fore.RED + "\t[ERROR] Wordlist is empty!" + Style.RESET_ALL)
                    return False

                for password in passwords:
                    self.queue.put(password)

        except FileNotFoundError:
            print(Fore.RED + f"\t[ERROR] Wordlist file not found at {wordlist_path}" + Style.RESET_ALL)
            return False

        # Create and start worker threads
        threads = []
        for _ in range(min(5, self.queue.qsize())):
            thread = threading.Thread(target=self.worker, args=(username, total_attempts))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

        if not self.found:
            print("\t[-] Brute-force attempt finished, no valid credentials found.")

        return self.found
