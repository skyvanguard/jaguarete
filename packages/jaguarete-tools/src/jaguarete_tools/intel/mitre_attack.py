"""MITRE ATT&CK mapping tool."""
from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

# Common MITRE ATT&CK techniques mapping
MITRE_TECHNIQUES = {
    "T1595": {
        "name": "Active Scanning",
        "tactic": "Reconnaissance",
        "url": "https://attack.mitre.org/techniques/T1595/",
    },
    "T1592": {
        "name": "Gather Victim Host Information",
        "tactic": "Reconnaissance",
        "url": "https://attack.mitre.org/techniques/T1592/",
    },
    "T1590": {
        "name": "Gather Victim Network Information",
        "tactic": "Reconnaissance",
        "url": "https://attack.mitre.org/techniques/T1590/",
    },
    "T1589": {
        "name": "Gather Victim Identity Information",
        "tactic": "Reconnaissance",
        "url": "https://attack.mitre.org/techniques/T1589/",
    },
    "T1190": {
        "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access",
        "url": "https://attack.mitre.org/techniques/T1190/",
    },
    "T1133": {
        "name": "External Remote Services",
        "tactic": "Initial Access",
        "url": "https://attack.mitre.org/techniques/T1133/",
    },
    "T1566": {
        "name": "Phishing",
        "tactic": "Initial Access",
        "url": "https://attack.mitre.org/techniques/T1566/",
    },
    "T1059": {
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "url": "https://attack.mitre.org/techniques/T1059/",
    },
    "T1053": {
        "name": "Scheduled Task/Job",
        "tactic": "Execution",
        "url": "https://attack.mitre.org/techniques/T1053/",
    },
    "T1078": {
        "name": "Valid Accounts",
        "tactic": "Persistence",
        "url": "https://attack.mitre.org/techniques/T1078/",
    },
    "T1098": {
        "name": "Account Manipulation",
        "tactic": "Persistence",
        "url": "https://attack.mitre.org/techniques/T1098/",
    },
    "T1068": {
        "name": "Exploitation for Privilege Escalation",
        "tactic": "Privilege Escalation",
        "url": "https://attack.mitre.org/techniques/T1068/",
    },
    "T1055": {
        "name": "Process Injection",
        "tactic": "Defense Evasion",
        "url": "https://attack.mitre.org/techniques/T1055/",
    },
    "T1070": {
        "name": "Indicator Removal",
        "tactic": "Defense Evasion",
        "url": "https://attack.mitre.org/techniques/T1070/",
    },
    "T1110": {
        "name": "Brute Force",
        "tactic": "Credential Access",
        "url": "https://attack.mitre.org/techniques/T1110/",
    },
    "T1003": {
        "name": "OS Credential Dumping",
        "tactic": "Credential Access",
        "url": "https://attack.mitre.org/techniques/T1003/",
    },
    "T1046": {
        "name": "Network Service Discovery",
        "tactic": "Discovery",
        "url": "https://attack.mitre.org/techniques/T1046/",
    },
    "T1021": {
        "name": "Remote Services",
        "tactic": "Lateral Movement",
        "url": "https://attack.mitre.org/techniques/T1021/",
    },
    "T1041": {
        "name": "Exfiltration Over C2 Channel",
        "tactic": "Exfiltration",
        "url": "https://attack.mitre.org/techniques/T1041/",
    },
    "T1486": {
        "name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "url": "https://attack.mitre.org/techniques/T1486/",
    },
}


@tool(description="Map a finding or technique to the MITRE ATT&CK framework")
def mitre_attack_map(
    technique_id: Annotated[
        str, Doc("MITRE ATT&CK technique ID (e.g., T1190) or keyword to search")
    ] = "",
    keyword: Annotated[
        str, Doc("Keyword to search across technique names and tactics")
    ] = "",
) -> str:
    """Map security findings to MITRE ATT&CK techniques.

    Search by technique ID or keyword to find relevant ATT&CK mappings.
    """
    results = []
    results.append("MITRE ATT&CK Mapping")
    results.append("=" * 50)

    if technique_id:
        tech_id = technique_id.upper()
        if tech_id in MITRE_TECHNIQUES:
            tech = MITRE_TECHNIQUES[tech_id]
            results.append(f"\n{tech_id}: {tech['name']}")
            results.append(f"  Tactic: {tech['tactic']}")
            results.append(f"  Reference: {tech['url']}")
        else:
            results.append(f"Technique {tech_id} not found in local database")
            results.append(f"Check: https://attack.mitre.org/techniques/{tech_id}/")

    if keyword:
        keyword_lower = keyword.lower()
        matches = []
        for tid, tech in MITRE_TECHNIQUES.items():
            if (
                keyword_lower in tech["name"].lower()
                or keyword_lower in tech["tactic"].lower()
            ):
                matches.append((tid, tech))

        if matches:
            results.append(f"\nMatches for '{keyword}':")
            for tid, tech in matches:
                results.append(f"  {tid}: {tech['name']} ({tech['tactic']})")
        else:
            results.append(f"No matches for '{keyword}'")

    if not technique_id and not keyword:
        results.append("\nAvailable tactics:")
        tactics = sorted(set(t["tactic"] for t in MITRE_TECHNIQUES.values()))
        for tactic in tactics:
            count = sum(
                1 for t in MITRE_TECHNIQUES.values() if t["tactic"] == tactic
            )
            results.append(f"  - {tactic} ({count} techniques)")

    return "\n".join(results)
