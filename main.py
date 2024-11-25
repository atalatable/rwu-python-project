#!/usr/bin/env python

import scanning
from cli import initialize
import options

if __name__ == "__main__":
    initialize()

    results = scanning.scan_ports(
        options.target_ip,
        range(options.start_port, options.end_port)
    )

    print("\nScan Results:")
    for result in results:
        print(f"Port: {result['port']}, Service: {result['service']}")

