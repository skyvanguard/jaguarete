"""Jaguarete Security Agents - Red, Blue, and Purple team AI agents."""

from jaguarete_agents.blue import IncidentResponderAgent, LogAnalystAgent, ThreatHunterAgent
from jaguarete_agents.purple import AttackSurfaceAgent, ReportGeneratorAgent
from jaguarete_agents.red import ExploitAnalystAgent, ReconAgent, VulnScannerAgent

__all__ = [
    "ReconAgent",
    "VulnScannerAgent",
    "ExploitAnalystAgent",
    "LogAnalystAgent",
    "IncidentResponderAgent",
    "ThreatHunterAgent",
    "AttackSurfaceAgent",
    "ReportGeneratorAgent",
]

__version__ = "0.1.0"
