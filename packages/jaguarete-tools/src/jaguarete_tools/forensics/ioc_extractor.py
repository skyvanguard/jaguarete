"""Indicator of Compromise (IOC) extraction tool."""
import re

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

# IOC patterns
IOC_PATTERNS = {
    "ipv4": re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
    ),
    "ipv6": re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"),
    "domain": re.compile(
        r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"
        r"+[a-zA-Z]{2,}\b"
    ),
    "url": re.compile(r"https?://[^\s<>\"']+"),
    "email": re.compile(
        r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
    ),
    "md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "cve": re.compile(r"\bCVE-\d{4}-\d{4,}\b"),
    "registry_key": re.compile(r"\b(?:HKEY_[A-Z_]+\\[^\s]+)\b"),
    "file_path_windows": re.compile(
        r"[A-Z]:\\(?:[^\s\\/:*?\"<>|]+\\)*[^\s\\/:*?\"<>|]+"
    ),
    "file_path_unix": re.compile(r"(?:/[^\s/]+){2,}"),
}

# Known benign patterns to exclude
BENIGN_DOMAINS = {"example.com", "localhost", "example.org", "test.com"}
BENIGN_IPS = {"127.0.0.1", "0.0.0.0", "255.255.255.255"}


@tool(
    description="Extract indicators of compromise (IOCs) from text"
    " - IPs, domains, hashes, URLs, CVEs"
)
def ioc_extractor(
    text: Annotated[
        str, Doc("Text to extract IOCs from (logs, reports, alerts)")
    ],
    ioc_types: Annotated[
        str, Doc("Comma-separated IOC types to extract, or 'all'")
    ] = "all",
) -> str:
    """Extract IOCs from unstructured text.

    Identifies IPs, domains, URLs, email addresses, file hashes
    (MD5/SHA1/SHA256), CVE identifiers, file paths, and registry keys.
    """
    results = []
    results.append("IOC Extraction Results")
    results.append("=" * 50)

    types_to_check = (
        IOC_PATTERNS.keys()
        if ioc_types == "all"
        else [t.strip() for t in ioc_types.split(",")]
    )

    total_iocs = 0
    for ioc_type in types_to_check:
        pattern = IOC_PATTERNS.get(ioc_type)
        if not pattern:
            continue

        matches = set(pattern.findall(text))

        # Filter benign
        if ioc_type == "ipv4":
            matches -= BENIGN_IPS
        if ioc_type == "domain":
            matches -= BENIGN_DOMAINS
            # Filter common non-IOC domains
            matches = {
                m
                for m in matches
                if not m.endswith((".png", ".jpg", ".css", ".js"))
            }

        if matches:
            results.append(f"\n{ioc_type.upper()} ({len(matches)}):")
            for match in sorted(matches):
                results.append(f"  - {match}")
            total_iocs += len(matches)

    results.append(f"\nTotal unique IOCs found: {total_iocs}")
    return "\n".join(results)
