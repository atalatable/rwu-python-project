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

    print(results)
