"""VulnScannerAgent - Vulnerability assessment specialist."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class VulnScannerAgent(ConversableAgent):
    """Detect known vulnerabilities using CVE databases and service fingerprinting.

    Prioritizes findings by CVSS score and exploitability, cross-referencing
    with NVD and exploit databases for accurate assessment.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "VulnScannerAgent",
            category="agent",
            key="jaguarete_vuln_scanner_agent_name",
        ),
        role=DynConfig(
            "Vulnerability Assessment Specialist",
            category="agent",
            key="jaguarete_vuln_scanner_agent_role",
        ),
        goal=DynConfig(
            "Detect known vulnerabilities in targets using CVE databases, "
            "dependency analysis, and service fingerprinting. Prioritize "
            "findings by CVSS score and exploitability.",
            category="agent",
            key="jaguarete_vuln_scanner_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Only scan authorized targets",
                "Prioritize findings by CVSS score",
                "Cross-reference with NVD and exploit databases",
                "Never attempt exploitation, only detection",
                "Report false positive likelihood for each finding",
            ],
            category="agent",
            key="jaguarete_vuln_scanner_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize VulnScannerAgent."""
        super().__init__(**kwargs)
