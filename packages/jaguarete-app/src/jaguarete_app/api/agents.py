"""Agent management routes."""

from fastapi import APIRouter, Depends

from jaguarete_app.auth.dependencies import get_current_user
from jaguarete_app.auth.models import TokenData

router = APIRouter()

# Available agent catalog
AGENT_CATALOG = [
    {
        "id": "recon",
        "name": "ReconAgent",
        "team": "red",
        "description": "Performs thorough reconnaissance on authorized targets",
        "scope_required": "red_team",
    },
    {
        "id": "vuln_scanner",
        "name": "VulnScannerAgent",
        "team": "red",
        "description": "Identifies and assesses security vulnerabilities",
        "scope_required": "red_team",
    },
    {
        "id": "exploit_analyst",
        "name": "ExploitAnalystAgent",
        "team": "red",
        "description": "Analyzes exploits and assesses impact",
        "scope_required": "red_team",
    },
    {
        "id": "log_analyst",
        "name": "LogAnalystAgent",
        "team": "blue",
        "description": "Analyzes security logs for anomalies and threats",
        "scope_required": "blue_team",
    },
    {
        "id": "incident_responder",
        "name": "IncidentResponderAgent",
        "team": "blue",
        "description": "Coordinates incident response procedures",
        "scope_required": "blue_team",
    },
    {
        "id": "threat_hunter",
        "name": "ThreatHunterAgent",
        "team": "blue",
        "description": "Proactively hunts for threats and IOCs",
        "scope_required": "blue_team",
    },
    {
        "id": "attack_surface",
        "name": "AttackSurfaceAgent",
        "team": "purple",
        "description": "Maps and analyzes the attack surface",
        "scope_required": "red_team",
    },
    {
        "id": "report_generator",
        "name": "ReportGeneratorAgent",
        "team": "purple",
        "description": "Generates comprehensive security reports",
        "scope_required": "reports",
    },
]


@router.get("")
async def list_agents(user: TokenData = Depends(get_current_user)):
    """List available security agents filtered by user scopes."""
    user_scopes = set(user.scopes)
    if user.role.value == "admin":
        return {"agents": AGENT_CATALOG}
    return {
        "agents": [
            a for a in AGENT_CATALOG if a["scope_required"] in user_scopes
        ]
    }
