"""AttackSurfaceAgent - Attack surface mapping coordinator."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class AttackSurfaceAgent(ConversableAgent):
    """Coordinate red team agents to build complete attack surface maps.

    Aggregates findings from reconnaissance and vulnerability scanning into
    a unified risk-scored view with executive and technical perspectives.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "AttackSurfaceAgent",
            category="agent",
            key="jaguarete_attack_surface_agent_name",
        ),
        role=DynConfig(
            "Attack Surface Mapping Coordinator",
            category="agent",
            key="jaguarete_attack_surface_agent_role",
        ),
        goal=DynConfig(
            "Coordinate red team agents to build complete attack surface maps. "
            "Aggregate findings from reconnaissance and vulnerability scanning "
            "into a unified risk-scored view.",
            category="agent",
            key="jaguarete_attack_surface_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Aggregate and deduplicate findings from all agents",
                "Score each attack vector by likelihood and impact",
                "Identify the most critical attack paths",
                "Maintain a living map updated with new findings",
                "Provide executive and technical views of the attack surface",
            ],
            category="agent",
            key="jaguarete_attack_surface_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize AttackSurfaceAgent."""
        super().__init__(**kwargs)
