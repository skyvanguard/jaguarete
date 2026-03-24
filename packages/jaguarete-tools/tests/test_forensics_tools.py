"""Tests for forensics tools."""


def test_ioc_extractor_finds_ips():
    from jaguarete_tools.forensics.ioc_extractor import ioc_extractor

    text = "Connection from 192.168.1.100 to 10.0.0.5 on port 443"
    result = ioc_extractor(text)
    assert "192.168.1.100" in result
    assert "10.0.0.5" in result


def test_ioc_extractor_finds_hashes():
    from jaguarete_tools.forensics.ioc_extractor import ioc_extractor

    text = "File hash: d41d8cd98f00b204e9800998ecf8427e"
    result = ioc_extractor(text, ioc_types="md5")
    assert "d41d8cd98f00b204e9800998ecf8427e" in result


def test_ioc_extractor_finds_cves():
    from jaguarete_tools.forensics.ioc_extractor import ioc_extractor

    text = "Patched CVE-2024-1234 and CVE-2023-5678"
    result = ioc_extractor(text, ioc_types="cve")
    assert "CVE-2024-1234" in result
    assert "CVE-2023-5678" in result


def test_ioc_extractor_filters_benign():
    from jaguarete_tools.forensics.ioc_extractor import ioc_extractor

    text = "Localhost 127.0.0.1 and 192.168.1.1"
    result = ioc_extractor(text, ioc_types="ipv4")
    assert "127.0.0.1" not in result
    assert "192.168.1.1" in result


def test_log_parser_detects_suspicious():
    from jaguarete_tools.forensics.log_parser import log_parser

    log = (
        "Jan  5 12:00:00 server sshd[1234]: "
        "Failed password for root from 10.0.0.1 port 22 ssh2"
    )
    result = log_parser(log)
    assert "Suspicious" in result or "Failed auth" in result


def test_log_parser_handles_empty():
    from jaguarete_tools.forensics.log_parser import log_parser

    result = log_parser("")
    assert "Log Analysis" in result
