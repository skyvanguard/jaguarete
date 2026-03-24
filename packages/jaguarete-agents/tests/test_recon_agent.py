"""Tests for ReconAgent."""


def test_recon_agent_has_correct_profile():
    """ReconAgent has the correct role and goal."""
    from jaguarete_agents.red.recon_agent import ReconAgent

    profile = ReconAgent.model_fields["profile"].default
    assert profile is not None
    assert "ReconAgent" in profile.name.default


def test_recon_agent_extends_conversable():
    """ReconAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.red.recon_agent import ReconAgent

    assert issubclass(ReconAgent, ConversableAgent)


def test_recon_agent_has_constraints():
    """ReconAgent has security constraints defined."""
    from jaguarete_agents.red.recon_agent import ReconAgent

    profile = ReconAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
