import scanning


if __name__ == "__main__":

    ip_target = "127.0.0.1"

    print(scanning.scan_ports(ip_target, range(0, 9999)))
