import scanning


if __name__ == "__main__":
    print(scanning.scan_ports("127.0.0.1", range(0, 9999)))
