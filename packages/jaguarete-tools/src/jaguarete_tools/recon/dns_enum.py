"""DNS enumeration tool for reconnaissance."""
import socket
from typing import Optional

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Enumerate DNS records for a target domain")
def dns_enum(
    domain: Annotated[str, Doc("Target domain to enumerate")],
    record_types: Annotated[
        str, Doc("Comma-separated DNS record types to query")
    ] = "A,AAAA,MX,NS,TXT,CNAME",
) -> str:
    """Enumerate DNS records for a target domain using socket resolution.

    Returns formatted DNS information including IP addresses and record types.
    """
    results = []
    results.append(f"DNS Enumeration for: {domain}")
    results.append("=" * 50)

    # A record lookup
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET)
        seen: set[str] = set()
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                seen.add(ip)
                results.append(f"A: {ip}")
    except socket.gaierror as e:
        results.append(f"A: lookup failed - {e}")

    # AAAA record lookup
    if "AAAA" in record_types:
        try:
            ips = socket.getaddrinfo(domain, None, socket.AF_INET6)
            seen_v6: set[str] = set()
            for info in ips:
                ip = info[4][0]
                if ip not in seen_v6:
                    seen_v6.add(ip)
                    results.append(f"AAAA: {ip}")
        except socket.gaierror:
            results.append("AAAA: no records found")

    # MX lookup via socket
    if "MX" in record_types:
        try:
            mx_info = socket.getaddrinfo(f"mail.{domain}", None)
            if mx_info:
                results.append(f"MX: mail.{domain} -> {mx_info[0][4][0]}")
        except socket.gaierror:
            results.append("MX: no records found (basic lookup)")

    return "\n".join(results)
