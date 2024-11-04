import scanning
from cli import execute_cli

if __name__ == "__main__":

    target_ip = execute_cli()

    print(scanning.scan_ports(target_ip, range(0, 9999)))