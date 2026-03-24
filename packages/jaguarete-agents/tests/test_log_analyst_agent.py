"""Tests for LogAnalystAgent."""


def test_log_analyst_agent_has_correct_profile():
    """LogAnalystAgent has the correct role and goal."""
    from jaguarete_agents.blue.log_analyst_agent import LogAnalystAgent

    profile = LogAnalystAgent.model_fields["profile"].default
    assert profile is not None
    assert "LogAnalystAgent" in profile.name.default


def test_log_analyst_agent_extends_conversable():
    """LogAnalystAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.blue.log_analyst_agent import LogAnalystAgent

    assert issubclass(LogAnalystAgent, ConversableAgent)


def test_log_analyst_agent_has_constraints():
    """LogAnalystAgent has security constraints defined."""
    from jaguarete_agents.blue.log_analyst_agent import LogAnalystAgent

    profile = LogAnalystAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
