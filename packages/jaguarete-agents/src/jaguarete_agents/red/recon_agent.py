"""ReconAgent - Reconnaissance specialist for authorized target enumeration."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class ReconAgent(ConversableAgent):
    """Perform thorough reconnaissance on authorized targets.

    Gathers information about domains, subdomains, open ports, running
    services, and potential attack vectors while respecting authorization
    boundaries.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "ReconAgent", category="agent", key="jaguarete_recon_agent_name"
        ),
        role=DynConfig(
            "Reconnaissance Specialist",
            category="agent",
            key="jaguarete_recon_agent_role",
        ),
        goal=DynConfig(
            "Perform thorough reconnaissance on authorized targets. Gather "
            "information about domains, subdomains, open ports, running "
            "services, and potential attack vectors. Always verify target "
            "authorization before scanning.",
            category="agent",
            key="jaguarete_recon_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Only scan targets explicitly authorized by the user",
                "Start with passive reconnaissance before active scanning",
                "Document all findings with timestamps and sources",
                "Flag high-severity findings immediately",
                "Never perform destructive actions on targets",
            ],
            category="agent",
            key="jaguarete_recon_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize ReconAgent."""
        super().__init__(**kwargs)
