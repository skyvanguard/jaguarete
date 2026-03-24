"""CVSS-based risk scoring tool."""
from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

SEVERITY_RANGES = {
    "none": (0.0, 0.0),
    "low": (0.1, 3.9),
    "medium": (4.0, 6.9),
    "high": (7.0, 8.9),
    "critical": (9.0, 10.0),
}


@tool(description="Calculate risk score based on CVSS-like parameters")
def risk_scorer(
    attack_vector: Annotated[
        str, Doc("Attack vector: network, adjacent, local, physical")
    ] = "network",
    attack_complexity: Annotated[
        str, Doc("Attack complexity: low, high")
    ] = "low",
    privileges_required: Annotated[
        str, Doc("Privileges required: none, low, high")
    ] = "none",
    user_interaction: Annotated[
        str, Doc("User interaction: none, required")
    ] = "none",
    impact_confidentiality: Annotated[
        str, Doc("Confidentiality impact: none, low, high")
    ] = "high",
    impact_integrity: Annotated[
        str, Doc("Integrity impact: none, low, high")
    ] = "high",
    impact_availability: Annotated[
        str, Doc("Availability impact: none, low, high")
    ] = "high",
) -> str:
    """Calculate a CVSS-like risk score from vulnerability parameters.

    Returns a score from 0.0 to 10.0 with severity classification.
    """
    # Simplified CVSS v3.1-like scoring
    av_scores = {
        "network": 0.85,
        "adjacent": 0.62,
        "local": 0.55,
        "physical": 0.20,
    }
    ac_scores = {"low": 0.77, "high": 0.44}
    pr_scores = {"none": 0.85, "low": 0.62, "high": 0.27}
    ui_scores = {"none": 0.85, "required": 0.62}
    impact_scores = {"none": 0.0, "low": 0.22, "high": 0.56}

    exploitability = (
        8.22
        * av_scores.get(attack_vector, 0.85)
        * ac_scores.get(attack_complexity, 0.77)
        * pr_scores.get(privileges_required, 0.85)
        * ui_scores.get(user_interaction, 0.85)
    )

    isc_base = 1 - (
        (1 - impact_scores.get(impact_confidentiality, 0.56))
        * (1 - impact_scores.get(impact_integrity, 0.56))
        * (1 - impact_scores.get(impact_availability, 0.56))
    )

    if isc_base <= 0:
        score = 0.0
    else:
        impact = 6.42 * isc_base
        score = min(10.0, round(1.08 * (impact + exploitability), 1))

    # Classify severity
    severity = "none"
    for sev, (low, high) in SEVERITY_RANGES.items():
        if low <= score <= high:
            severity = sev
            break

    results = []
    results.append("Risk Score Assessment")
    results.append("=" * 50)
    results.append(f"\nScore: {score}/10.0")
    results.append(f"Severity: {severity.upper()}")
    results.append(f"\nParameters:")
    results.append(f"  Attack Vector: {attack_vector}")
    results.append(f"  Attack Complexity: {attack_complexity}")
    results.append(f"  Privileges Required: {privileges_required}")
    results.append(f"  User Interaction: {user_interaction}")
    results.append(f"  Confidentiality Impact: {impact_confidentiality}")
    results.append(f"  Integrity Impact: {impact_integrity}")
    results.append(f"  Availability Impact: {impact_availability}")

    return "\n".join(results)
