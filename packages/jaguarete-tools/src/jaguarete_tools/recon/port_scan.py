"""Port scanning tool for reconnaissance."""
import socket

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-ALT",
    8443: "HTTPS-ALT",
    27017: "MongoDB",
}


@tool(description="Scan common ports on a target host to identify open services")
def port_scan(
    host: Annotated[str, Doc("Target hostname or IP address to scan")],
    ports: Annotated[
        str, Doc("Comma-separated port numbers, or 'common' for top 21 ports")
    ] = "common",
    timeout: Annotated[float, Doc("Connection timeout in seconds per port")] = 1.0,
) -> str:
    """Scan ports on a target host to identify open services.

    Uses TCP connect scanning to determine if ports are open.
    """
    if ports == "common":
        port_list = sorted(COMMON_PORTS.keys())
    else:
        port_list = [int(p.strip()) for p in ports.split(",")]

    results = []
    results.append(f"Port Scan Results for: {host}")
    results.append("=" * 50)
    open_count = 0

    for port in port_list:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "unknown")
                results.append(f"  {port}/tcp  OPEN  {service}")
                open_count += 1
            sock.close()
        except (socket.timeout, socket.error):
            pass

    results.append(f"\n{open_count} open port(s) found out of {len(port_list)} scanned")
    return "\n".join(results)
