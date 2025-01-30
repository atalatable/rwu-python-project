#!/usr/bin/env python

import scanning
from cli import initialize
import options
from services import service
import logging

if __name__ == "__main__":
    initialize()

    logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

    results = scanning.scan_network(
        options.TARGET_NETWORK,
        list(range(options.START_PORT, options.END_PORT))
    )

    for address in results:
        if address["open_ports"]:
            for open_ports in address["open_ports"]:
                open_ports["service"] = scanning.detect_service(address["ip"], open_ports["port"])

    print("========== OPEN PORTS ===========")

    for address in results:
        if address["open_ports"]:
            print(f"[+] {address['ip']}")
            for open_port in address["open_ports"]:
                detected_service = open_port["service"]

                if isinstance(detected_service, service.Service):
                    print(f"\t{detected_service.port} - {detected_service.name}")
                else:
                    print(f"\t{open_port} - {detected_service}")

    print("\n========== DEFAULT LOGIN ==========")

    for address in results:
        if address["open_ports"]:
            print(f"[+] {address['ip']}")
            for open_port in address["open_ports"]:
                detected_service = open_port["service"]
                if isinstance(detected_service, service.Service):
                    try:
                        login_success = detected_service.try_login()
                        if not login_success:
                            print(f"\t({detected_service.port} - {detected_service.name}) Default login method doesn't work")
                        # else:
                        #     print(f"\t[+] Successful login on {detected_service.name} ({detected_service.ip_addr}:{detected_service.port})")
                    except:
                        print(f"\tUnsupported service for default login ({detected_service})")
                else:
                    print(f"\tUnsupported service for default login ({detected_service})")

    if options.USERNAME:
        print("\n======== BRUTE FORCE ===========")

        for address in results:
            if address["open_ports"]:
                print(f"[+] {address['ip']}")
                for open_port in address["open_ports"]:
                    detected_service = open_port["service"]
                    if isinstance(detected_service, service.Service):
                        try:
                            brute_force_success = detected_service.bruteforce()
                            if not brute_force_success:
                                print(f"\t({detected_service.port} - {detected_service.name}) Brute-force failed")
                        except:
                            print(f"\tUnsupported service for bruteforce attempt ({detected_service})")
                    else:
                        print(f"\tUnsupported service for bruteforce attempt ({detected_service})")

