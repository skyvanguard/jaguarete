"""Tests for ReportGeneratorAgent."""


def test_report_generator_agent_has_correct_profile():
    """ReportGeneratorAgent has the correct role and goal."""
    from jaguarete_agents.purple.report_generator_agent import ReportGeneratorAgent

    profile = ReportGeneratorAgent.model_fields["profile"].default
    assert profile is not None
    assert "ReportGeneratorAgent" in profile.name.default


def test_report_generator_agent_extends_conversable():
    """ReportGeneratorAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.purple.report_generator_agent import ReportGeneratorAgent

    assert issubclass(ReportGeneratorAgent, ConversableAgent)


def test_report_generator_agent_has_constraints():
    """ReportGeneratorAgent has security constraints defined."""
    from jaguarete_agents.purple.report_generator_agent import ReportGeneratorAgent

    profile = ReportGeneratorAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
