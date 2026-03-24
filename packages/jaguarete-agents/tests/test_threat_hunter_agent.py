"""Tests for ThreatHunterAgent."""


def test_threat_hunter_agent_has_correct_profile():
    """ThreatHunterAgent has the correct role and goal."""
    from jaguarete_agents.blue.threat_hunter_agent import ThreatHunterAgent

    profile = ThreatHunterAgent.model_fields["profile"].default
    assert profile is not None
    assert "ThreatHunterAgent" in profile.name.default


def test_threat_hunter_agent_extends_conversable():
    """ThreatHunterAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.blue.threat_hunter_agent import ThreatHunterAgent

    assert issubclass(ThreatHunterAgent, ConversableAgent)


def test_threat_hunter_agent_has_constraints():
    """ThreatHunterAgent has security constraints defined."""
    from jaguarete_agents.blue.threat_hunter_agent import ThreatHunterAgent

    profile = ThreatHunterAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
