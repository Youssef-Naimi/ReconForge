import socket
import ssl
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    80,    # HTTP
    110,   # POP3
    143,   # IMAP
    443,   # HTTPS
    445,   # SMB
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    6379,  # Redis
    8080,  # HTTP Proxy / Alternate HTTP
    8443,  # Alternate HTTPS
]


def grab_banner(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)

            banner = sock.recv(4096)

            if banner:
                return banner.decode("utf-8", errors="replace").strip()

            return None

    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def probe_https(host, port, timeout=2):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                secure_sock.settimeout(timeout)

                request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                )

                secure_sock.sendall(request.encode())

                response = secure_sock.recv(1024)

                if response:
                    return response.decode("utf-8", errors="replace").strip()

                return None

    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def probe_http(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)

            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )

            sock.sendall(request.encode())

            response = sock.recv(1024)

            if response:
                return response.decode("utf-8", errors="replace").strip()

            return None

    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def get_expected_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"


def validate_port(port):
    return isinstance(port, int) and 1 <= port <= 65535


def scan_port(host, port, timeout=1):
    if not validate_port(port):
        raise ValueError("port must be in [1,65535]")

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "OPEN"
    except socket.timeout:
        return "FILTERED"
    except (ConnectionRefusedError, OSError):
        return "CLOSED"


def probe_port(host, port, timeout=2):
    state = scan_port(host, port, timeout)

    if state != "OPEN":
        return {
            "port": port,
            "state": state
        }

    banner = grab_banner(host, port, timeout)

    if banner is not None:
        return {
            "port": port,
            "state": state,
            "response": banner
        }

    response = probe_http(host, port, timeout)

    if response is not None:
        return {
            "port": port,
            "state": state,
            "response": response
        }

    response = probe_https(host, port, timeout)

    return {
        "port": port,
        "state": state,
        "response": response
    }


def scan_ports(host, ports=None, timeout=2):
    if ports is None:
        ports = COMMON_PORTS

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(probe_port, host, port, timeout): port
            for port in ports
        }

        for future in futures:
            port = futures[future]

            try:
                result = future.result()

            except Exception as error:
                result = {
                    "port": port,
                    "state": "ERROR",
                    "error": str(error)
                }

            if result["state"] == "OPEN":
                results.append(result)

    return results
