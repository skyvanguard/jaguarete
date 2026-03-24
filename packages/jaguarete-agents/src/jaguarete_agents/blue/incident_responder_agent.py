"""IncidentResponderAgent - Incident response coordinator following NIST framework."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class IncidentResponderAgent(ConversableAgent):
    """Guide step-by-step incident response following NIST SP 800-61.

    Coordinates containment, eradication, and recovery procedures while
    preserving evidence chain of custody throughout the process.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "IncidentResponderAgent",
            category="agent",
            key="jaguarete_incident_responder_agent_name",
        ),
        role=DynConfig(
            "Incident Response Coordinator",
            category="agent",
            key="jaguarete_incident_responder_agent_role",
        ),
        goal=DynConfig(
            "Guide step-by-step incident response following NIST SP 800-61 "
            "framework. Coordinate containment, eradication, and recovery "
            "procedures while preserving evidence.",
            category="agent",
            key="jaguarete_incident_responder_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Follow NIST SP 800-61 incident response lifecycle",
                "Preserve evidence chain of custody at all times",
                "Prioritize containment to prevent lateral movement",
                "Document all response actions with timestamps",
                "Coordinate with relevant stakeholders before major actions",
            ],
            category="agent",
            key="jaguarete_incident_responder_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize IncidentResponderAgent."""
        super().__init__(**kwargs)
