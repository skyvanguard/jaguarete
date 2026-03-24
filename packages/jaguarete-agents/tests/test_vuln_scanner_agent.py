"""Tests for VulnScannerAgent."""


def test_vuln_scanner_agent_has_correct_profile():
    """VulnScannerAgent has the correct role and goal."""
    from jaguarete_agents.red.vuln_scanner_agent import VulnScannerAgent

    profile = VulnScannerAgent.model_fields["profile"].default
    assert profile is not None
    assert "VulnScannerAgent" in profile.name.default


def test_vuln_scanner_agent_extends_conversable():
    """VulnScannerAgent inherits from ConversableAgent."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete_agents.red.vuln_scanner_agent import VulnScannerAgent

    assert issubclass(VulnScannerAgent, ConversableAgent)


def test_vuln_scanner_agent_has_constraints():
    """VulnScannerAgent has security constraints defined."""
    from jaguarete_agents.red.vuln_scanner_agent import VulnScannerAgent

    profile = VulnScannerAgent.model_fields["profile"].default
    constraints = profile.constraints
    assert constraints is not None
