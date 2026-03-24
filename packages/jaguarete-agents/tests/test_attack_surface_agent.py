"""Tests for AttackSurfaceAgent."""


def test_attack_surface_agent_has_correct_profile():
    """AttackSurfaceAgent has the correct role and goal."""
    from jaguarete_agents.purple.attack_surface_agent import AttackSurfaceAgent

    profile = AttackSurfaceAgent.model_fields["profile"].default
    assert profile is not None
    assert "AttackSurfaceAgent" in profile.name.default


def test_attack_surface_agent_extends_conversable():
    """AttackSurfaceAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.purple.attack_surface_agent import AttackSurfaceAgent

    assert issubclass(AttackSurfaceAgent, ConversableAgent)


def test_attack_surface_agent_has_constraints():
    """AttackSurfaceAgent has security constraints defined."""
    from jaguarete_agents.purple.attack_surface_agent import AttackSurfaceAgent

    profile = AttackSurfaceAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
