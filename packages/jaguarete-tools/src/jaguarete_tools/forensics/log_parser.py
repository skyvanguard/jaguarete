"""Log parsing tool for security forensics."""
import re

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

# Common log patterns
LOG_PATTERNS = {
    "syslog": re.compile(
        r"(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
        r"(?P<hostname>\S+)\s+(?P<process>\S+?)(?:\[(?P<pid>\d+)\])?"
        r":\s+(?P<message>.*)"
    ),
    "apache_access": re.compile(
        r"(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+"
        r'"(?P<method>\w+)\s+(?P<path>\S+)\s+\S+"\s+'
        r"(?P<status>\d+)\s+(?P<size>\S+)"
    ),
    "nginx_access": re.compile(
        r"(?P<ip>\S+)\s+-\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+"
        r'"(?P<method>\w+)\s+(?P<path>\S+)\s+\S+"\s+'
        r"(?P<status>\d+)\s+(?P<size>\d+)"
    ),
    "auth_log": re.compile(
        r"(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
        r"(?P<hostname>\S+)\s+(?P<service>\S+?)(?:\[(?P<pid>\d+)\])?:\s+"
        r"(?P<message>.*(?:(?:Failed|Accepted)\s+password"
        r"|session\s+(?:opened|closed)).*)"
    ),
}


@tool(
    description="Parse log entries and extract structured security-relevant information"
)
def log_parser(
    log_text: Annotated[str, Doc("Raw log text to parse (one or more lines)")],
    log_format: Annotated[
        str,
        Doc(
            "Log format: syslog, apache_access, nginx_access, auth_log, or auto"
        ),
    ] = "auto",
) -> str:
    """Parse log entries into structured format for security analysis.

    Supports syslog, Apache/Nginx access logs, and auth logs.
    Auto-detects format if not specified.
    """
    lines = log_text.strip().split("\n")
    results = []
    results.append(f"Log Analysis ({len(lines)} lines)")
    results.append("=" * 50)

    parsed_count = 0
    suspicious = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        formats_to_try = (
            [log_format] if log_format != "auto" else LOG_PATTERNS.keys()
        )

        for fmt in formats_to_try:
            pattern = LOG_PATTERNS.get(fmt)
            if not pattern:
                continue
            match = pattern.match(line)
            if match:
                data = match.groupdict()
                parsed_count += 1

                # Check for suspicious patterns
                message = data.get("message", "") + data.get("path", "")
                status = data.get("status", "")

                if "Failed password" in message:
                    suspicious.append(
                        f"  Line {i+1}: Failed auth from "
                        f"{data.get('ip', data.get('hostname', '?'))}"
                    )
                if any(
                    p in message
                    for p in ["../", "etc/passwd", "UNION SELECT", "<script"]
                ):
                    suspicious.append(
                        f"  Line {i+1}: Possible attack pattern in: "
                        f"{message[:100]}"
                    )
                if status in ("401", "403", "500"):
                    suspicious.append(
                        f"  Line {i+1}: HTTP {status} from "
                        f"{data.get('ip', '?')} -> {data.get('path', '?')}"
                    )
                break

    results.append(f"Parsed: {parsed_count}/{len(lines)} lines")

    if suspicious:
        results.append(f"\nSuspicious entries ({len(suspicious)}):")
        results.extend(suspicious)
    else:
        results.append("\nNo suspicious patterns detected")

    return "\n".join(results)
