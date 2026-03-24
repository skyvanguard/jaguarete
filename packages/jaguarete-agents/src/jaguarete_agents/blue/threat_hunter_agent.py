"""ThreatHunterAgent - Proactive threat hunting specialist."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class ThreatHunterAgent(ConversableAgent):
    """Proactively search for hidden threats using hypothesis-driven methodology.

    Develops and tests threat hypotheses based on intelligence and behavioral
    analytics, mapping findings to MITRE ATT&CK techniques.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "ThreatHunterAgent",
            category="agent",
            key="jaguarete_threat_hunter_agent_name",
        ),
        role=DynConfig(
            "Proactive Threat Hunter",
            category="agent",
            key="jaguarete_threat_hunter_agent_role",
        ),
        goal=DynConfig(
            "Proactively search for hidden threats using hypothesis-driven "
            "hunting methodology. Develop and test threat hypotheses based on "
            "intelligence and behavioral analytics.",
            category="agent",
            key="jaguarete_threat_hunter_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Document all hypotheses before investigation",
                "Use Sigma rules for detection logic",
                "Map findings to MITRE ATT&CK techniques",
                "Distinguish between confirmed threats and suspicious activity",
                "Provide hunting playbooks for recurring patterns",
            ],
            category="agent",
            key="jaguarete_threat_hunter_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize ThreatHunterAgent."""
        super().__init__(**kwargs)
