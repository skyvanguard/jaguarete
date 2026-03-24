"""Secrets scanning tool for code analysis."""
import re

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS Secret Key": re.compile(
        r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?"
        r"([A-Za-z0-9/+=]{40})['\"]?"
    ),
    "GitHub Token": re.compile(r"gh[ps]_[A-Za-z0-9_]{36,}"),
    "Generic API Key": re.compile(
        r"(?i)(?:api[_-]?key|apikey)\s*[=:]\s*['\"]?"
        r"([A-Za-z0-9]{20,})['\"]?"
    ),
    "Generic Secret": re.compile(
        r"(?i)(?:secret|password|passwd|pwd)\s*[=:]\s*['\"]?"
        r"([^\s'\"]{8,})['\"]?"
    ),
    "Private Key": re.compile(
        r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"
    ),
    "JWT Token": re.compile(
        r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    ),
    "Slack Token": re.compile(
        r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,34}"
    ),
}


@tool(
    description="Scan text or code for hardcoded secrets, API keys, and credentials"
)
def secrets_scan(
    text: Annotated[str, Doc("Text or code to scan for secrets")],
) -> str:
    """Scan text for hardcoded secrets and credentials.

    Detects AWS keys, GitHub tokens, API keys, passwords, private keys,
    JWTs, and Slack tokens.
    """
    results = []
    results.append("Secrets Scan Results")
    results.append("=" * 50)

    total_findings = 0
    lines = text.split("\n")

    for pattern_name, pattern in SECRET_PATTERNS.items():
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                total_findings += 1
                # Mask the actual secret
                masked = line.strip()[:80] + (
                    "..." if len(line.strip()) > 80 else ""
                )
                results.append(f"\n[!!] {pattern_name} found on line {i}")
                results.append(f"     Context: {masked}")

    if total_findings == 0:
        results.append("\nNo secrets detected")
    else:
        results.append(f"\n{total_findings} potential secret(s) found!")
        results.append(
            "ACTION: Remove secrets and rotate affected credentials"
        )

    return "\n".join(results)
