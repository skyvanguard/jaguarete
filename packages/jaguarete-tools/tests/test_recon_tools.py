"""Tests for reconnaissance tools."""


def test_dns_enum_returns_results():
    from jaguarete_tools.recon.dns_enum import dns_enum

    result = dns_enum("example.com")
    assert "DNS Enumeration for: example.com" in result
    assert "A:" in result


def test_port_scan_callable():
    from jaguarete_tools.recon.port_scan import port_scan

    assert callable(port_scan)


def test_whois_lookup_callable():
    from jaguarete_tools.recon.whois_lookup import whois_lookup

    assert callable(whois_lookup)


def test_port_scan_common_ports_defined():
    from jaguarete_tools.recon.port_scan import COMMON_PORTS

    assert 80 in COMMON_PORTS
    assert 443 in COMMON_PORTS
    assert 22 in COMMON_PORTS
