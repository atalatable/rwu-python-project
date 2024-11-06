import scanning
from cli import initialize
import options

if __name__ == "__main__":

    initialize()

    print(
            scanning.scan_ports(
                options.target_ip,
                range(options.start_port, options.end_port)
                )
            )
