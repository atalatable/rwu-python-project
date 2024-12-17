#!/usr/bin/env python

from ipaddress import IPv4Address
import scanning
from cli import initialize
import options
from services.ssh import SshService

if __name__ == "__main__":
    initialize()

    results = scanning.scan_network(
        options.TARGET_NETWORK,
        list(range(options.START_PORT, options.END_PORT))
    )

    for address in results:
        if address["open_ports"]:
            print(f"--------------------\n-- {address["ip"]}")
            for port in address["open_ports"]:
                print(f"{port} - {scanning.detect_service(address["ip"], port)}")
