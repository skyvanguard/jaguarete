"""LogAnalystAgent - Log analysis and anomaly detection specialist."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class LogAnalystAgent(ConversableAgent):
    """Analyze system and application logs to detect anomalies.

    Extracts indicators of compromise, identifies attack patterns, and
    correlates events across multiple log sources using Sigma rules.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "LogAnalystAgent",
            category="agent",
            key="jaguarete_log_analyst_agent_name",
        ),
        role=DynConfig(
            "Log Analysis and Anomaly Detection Specialist",
            category="agent",
            key="jaguarete_log_analyst_agent_role",
        ),
        goal=DynConfig(
            "Analyze system and application logs to detect anomalies, extract "
            "indicators of compromise, and identify attack patterns. Correlate "
            "events across multiple log sources.",
            category="agent",
            key="jaguarete_log_analyst_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Read-only operations, never modify logs",
                "Correlate events across multiple log sources",
                "Use Sigma rules for standardized detection",
                "Provide timeline reconstruction for incidents",
                "Flag false positives with reasoning",
            ],
            category="agent",
            key="jaguarete_log_analyst_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize LogAnalystAgent."""
        super().__init__(**kwargs)
