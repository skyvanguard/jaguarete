"""Security report generation tool."""
from datetime import datetime

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Generate a structured security report in markdown format")
def report_builder(
    title: Annotated[str, Doc("Report title")],
    findings: Annotated[
        str, Doc("Findings as newline-separated items (severity:description format)")
    ],
    report_type: Annotated[
        str, Doc("Report type: executive or technical")
    ] = "technical",
    target: Annotated[
        str, Doc("Target system or scope of assessment")
    ] = "N/A",
) -> str:
    """Generate a structured markdown security report.

    Accepts findings in 'severity:description' format and produces either
    an executive summary or detailed technical report.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    lines.append("# Security Assessment Report")
    lines.append(f"\n**Title:** {title}")
    lines.append(f"**Date:** {now}")
    lines.append(f"**Target:** {target}")
    lines.append(f"**Type:** {report_type.title()}")
    lines.append("\n---\n")

    # Parse findings
    finding_list = []
    severity_count = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0,
    }

    for line in findings.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            severity, desc = line.split(":", 1)
            severity = severity.strip().lower()
            if severity not in severity_count:
                severity = "info"
            severity_count[severity] += 1
            finding_list.append(
                {"severity": severity, "description": desc.strip()}
            )
        else:
            severity_count["info"] += 1
            finding_list.append({"severity": "info", "description": line})

    # Executive summary
    lines.append("## Executive Summary\n")
    total = len(finding_list)
    lines.append(f"This assessment identified **{total} findings**:\n")
    for sev in ["critical", "high", "medium", "low", "info"]:
        if severity_count[sev] > 0:
            marker = {
                "critical": "!!",
                "high": "!",
                "medium": "-",
                "low": "~",
                "info": "i",
            }[sev]
            lines.append(f"- [{marker}] **{sev.upper()}**: {severity_count[sev]}")

    if report_type == "executive":
        lines.append("\n## Key Risks\n")
        for f in finding_list:
            if f["severity"] in ("critical", "high"):
                lines.append(
                    f"- **[{f['severity'].upper()}]** {f['description']}"
                )
        lines.append("\n## Recommendations\n")
        lines.append("- Address all CRITICAL findings within 24 hours")
        lines.append("- Address HIGH findings within 1 week")
        lines.append("- Schedule MEDIUM findings for next sprint")
    else:
        lines.append("\n## Detailed Findings\n")
        for i, f in enumerate(finding_list, 1):
            lines.append(f"### Finding {i}: [{f['severity'].upper()}]\n")
            lines.append(f"**Description:** {f['description']}\n")

    return "\n".join(lines)
