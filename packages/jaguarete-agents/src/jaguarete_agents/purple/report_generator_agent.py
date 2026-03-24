"""ReportGeneratorAgent - Security report generation specialist."""

from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class ReportGeneratorAgent(ConversableAgent):
    """Generate comprehensive executive and technical security reports.

    Includes risk scores, remediation priorities, and compliance mapping
    to frameworks such as NIST, ISO 27001, and SOC 2.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "ReportGeneratorAgent",
            category="agent",
            key="jaguarete_report_generator_agent_name",
        ),
        role=DynConfig(
            "Security Report Generator",
            category="agent",
            key="jaguarete_report_generator_agent_role",
        ),
        goal=DynConfig(
            "Generate comprehensive executive and technical security reports "
            "from agent findings. Include risk scores, remediation priorities, "
            "and compliance mapping.",
            category="agent",
            key="jaguarete_report_generator_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Two report modes: executive summary and technical detail",
                "Include remediation recommendations with priority rankings",
                "Map findings to compliance frameworks (NIST, ISO 27001, SOC 2)",
                "Use clear visualizable data structures for charts",
                "Never include raw exploit code in executive reports",
            ],
            category="agent",
            key="jaguarete_report_generator_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize ReportGeneratorAgent."""
        super().__init__(**kwargs)
