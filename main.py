#!/usr/bin/env python

import scanning
from cli import initialize
import options

if __name__ == "__main__":
    initialize()

    results = scanning.scan_ports(
        options.TARGET_IP,
        list(range(options.START_PORT, options.END_PORT))
    )

    print("\nScan Results:")
    for result in results:
        print(f"Port: {result['port']}, Service: {result['service']}")

