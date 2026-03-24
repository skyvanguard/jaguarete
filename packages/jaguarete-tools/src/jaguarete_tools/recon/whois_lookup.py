"""WHOIS lookup tool for domain reconnaissance."""
import socket

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Perform WHOIS lookup on a domain to gather registration information")
def whois_lookup(
    domain: Annotated[str, Doc("Target domain for WHOIS lookup")],
) -> str:
    """Query WHOIS information for a domain.

    Connects to the WHOIS server to retrieve domain registration details.
    """
    results = []
    results.append(f"WHOIS Lookup for: {domain}")
    results.append("=" * 50)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(("whois.iana.org", 43))
        sock.send(f"{domain}\r\n".encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()

        text = response.decode("utf-8", errors="replace")
        results.append(text.strip())
    except (socket.timeout, socket.error) as e:
        results.append(f"WHOIS query failed: {e}")

    return "\n".join(results)
