#!/usr/bin/env python

import scanning
from cli import initialize
import options
from services import service

if __name__ == "__main__":
    initialize()

    results = scanning.scan_network(
        options.TARGET_NETWORK,
        list(range(options.START_PORT, options.END_PORT))
    )

    for address in results:
        if address["open_ports"]:
            print(f"========== OPEN PORTS ==========\n-- {address['ip']} :")
            for port in address["open_ports"]:
                detected_service = scanning.detect_service(address["ip"], port)

                if isinstance(detected_service, service.Service):
                    print(f"{detected_service.port} - {detected_service.name}")
                else:
                    print(f"{port} - {detected_service}")
            
            print("\n========== LOGIN ATTEMPTS ==========")
            for port in address["open_ports"]:
                detected_service = scanning.detect_service(address["ip"], port)
                if isinstance(detected_service, service.Service):
                    login_success = detected_service.try_login()
                    if login_success:
                        print(f"[+] Successful login on {detected_service.name} ({detected_service.ip_addr}:{detected_service.port})")
                    else:
                        print(f"[-] Failed login on {detected_service.name} ({detected_service.ip_addr}:{detected_service.port})")
            
            print("\n========== BRUTE FORCE ATTEMPTS ==========")
            for port in address["open_ports"]:
                detected_service = scanning.detect_service(address["ip"], port)
                if isinstance(detected_service, service.Service):
                    brute_force_success = detected_service.bruteforce()
                    if brute_force_success:
                        print(f"[+] Brute-force success on {detected_service.name} ({detected_service.ip_addr}:{detected_service.port})")
                    else:
                        print(f"[-] Brute-force failed on {detected_service.name} ({detected_service.ip_addr}:{detected_service.port})")


                    
