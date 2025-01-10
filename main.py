#!/usr/bin/env python

import scanning
from cli import initialize
import options

if __name__ == "__main__":
    initialize()

    results = scanning.scan_network(
        options.TARGET_NETWORK,
        list(range(options.START_PORT, options.END_PORT))
    )

    for address in results:
        if address["open_ports"]:
            print(f"--------------------\n-- {address["ip"]} :")
            for port in address["open_ports"]:
                detected_service = scanning.detect_service(address["ip"], port)

                print(f"{detected_service.port} - {detected_service.name}")
