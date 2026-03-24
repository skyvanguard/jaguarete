"""Tests for IncidentResponderAgent."""


def test_incident_responder_agent_has_correct_profile():
    """IncidentResponderAgent has the correct role and goal."""
    from jaguarete_agents.blue.incident_responder_agent import IncidentResponderAgent

    profile = IncidentResponderAgent.model_fields["profile"].default
    assert profile is not None
    assert "IncidentResponderAgent" in profile.name.default


def test_incident_responder_agent_extends_conversable():
    """IncidentResponderAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.blue.incident_responder_agent import IncidentResponderAgent

    assert issubclass(IncidentResponderAgent, ConversableAgent)


def test_incident_responder_agent_has_constraints():
    """IncidentResponderAgent has security constraints defined."""
    from jaguarete_agents.blue.incident_responder_agent import IncidentResponderAgent

    profile = IncidentResponderAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
