"""MITRE ATT&CK knowledge source for RAG pipeline."""
import json
from dataclasses import dataclass, field
from typing import Optional

from jaguarete.core.interface.knowledge import Chunk, Document


MITRE_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Embedded subset of MITRE ATT&CK techniques for offline use
MITRE_ATTACK_TECHNIQUES = [
    {
        "id": "T1595",
        "name": "Active Scanning",
        "tactic": "Reconnaissance",
        "description": "Adversaries may execute active reconnaissance scans to gather information that can be used during targeting. Active scans are those where the adversary probes victim infrastructure via network traffic.",
        "mitigations": ["M1056 - Pre-compromise", "Filter network traffic to prevent scanning"],
        "detection": "Monitor for suspicious network traffic that may indicate scanning activity.",
    },
    {
        "id": "T1592",
        "name": "Gather Victim Host Information",
        "tactic": "Reconnaissance",
        "description": "Adversaries may gather information about the victim's hosts that can be used during targeting. Information about hosts may include administrative data as well as specifics regarding its configuration.",
        "mitigations": ["M1056 - Pre-compromise"],
        "detection": "Monitor for suspicious queries about host configurations.",
    },
    {
        "id": "T1190",
        "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access",
        "description": "Adversaries may attempt to exploit a weakness in an Internet-facing host or system to initially access a network. The weakness may be a software bug, a temporary glitch, or a misconfiguration.",
        "mitigations": ["M1048 - Application Isolation", "M1050 - Exploit Protection", "M1051 - Update Software", "M1030 - Network Segmentation"],
        "detection": "Monitor application logs for abnormal behavior, failed authentication, SQL errors.",
    },
    {
        "id": "T1566",
        "name": "Phishing",
        "tactic": "Initial Access",
        "description": "Adversaries may send phishing messages to gain access to victim systems. All forms of phishing are electronically delivered social engineering.",
        "mitigations": ["M1049 - Antivirus/Antimalware", "M1031 - Network Intrusion Prevention", "M1054 - Software Configuration", "M1017 - User Training"],
        "detection": "Monitor emails for suspicious attachments and links. Network intrusion detection signatures.",
    },
    {
        "id": "T1059",
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "description": "Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries.",
        "mitigations": ["M1049 - Antivirus/Antimalware", "M1038 - Execution Prevention", "M1040 - Behavior Prevention"],
        "detection": "Monitor command-line arguments and script execution. Process monitoring.",
    },
    {
        "id": "T1078",
        "name": "Valid Accounts",
        "tactic": "Persistence",
        "description": "Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion.",
        "mitigations": ["M1013 - Application Developer Guidance", "M1027 - Password Policies", "M1026 - Privileged Account Management"],
        "detection": "Monitor authentication logs for unusual account activity.",
    },
    {
        "id": "T1068",
        "name": "Exploitation for Privilege Escalation",
        "tactic": "Privilege Escalation",
        "description": "Adversaries may exploit software vulnerabilities in an attempt to elevate privileges.",
        "mitigations": ["M1048 - Application Isolation", "M1050 - Exploit Protection", "M1051 - Update Software"],
        "detection": "Monitor for unusual process behavior and privilege changes.",
    },
    {
        "id": "T1055",
        "name": "Process Injection",
        "tactic": "Defense Evasion",
        "description": "Adversaries may inject code into processes in order to evade process-based defenses as well as possibly elevate privileges.",
        "mitigations": ["M1040 - Behavior Prevention on Endpoint", "M1026 - Privileged Account Management"],
        "detection": "Monitor for process injection indicators: unexpected DLL loads, memory modifications.",
    },
    {
        "id": "T1110",
        "name": "Brute Force",
        "tactic": "Credential Access",
        "description": "Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.",
        "mitigations": ["M1036 - Account Use Policies", "M1032 - Multi-factor Authentication", "M1027 - Password Policies"],
        "detection": "Monitor authentication logs for repeated failed attempts.",
    },
    {
        "id": "T1046",
        "name": "Network Service Discovery",
        "tactic": "Discovery",
        "description": "Adversaries may attempt to get a listing of services running on remote hosts and local network infrastructure devices.",
        "mitigations": ["M1031 - Network Intrusion Prevention", "M1030 - Network Segmentation"],
        "detection": "Monitor for port scanning activity and network enumeration.",
    },
    {
        "id": "T1021",
        "name": "Remote Services",
        "tactic": "Lateral Movement",
        "description": "Adversaries may use Valid Accounts to log into a service that accepts remote connections, such as SSH, RDP, VNC, or similar.",
        "mitigations": ["M1032 - Multi-factor Authentication", "M1018 - User Account Management"],
        "detection": "Monitor for lateral movement via remote service connections.",
    },
    {
        "id": "T1041",
        "name": "Exfiltration Over C2 Channel",
        "tactic": "Exfiltration",
        "description": "Adversaries may steal data by exfiltrating it over an existing command and control channel.",
        "mitigations": ["M1031 - Network Intrusion Prevention", "M1057 - Data Loss Prevention"],
        "detection": "Monitor for unusual data transfers over C2 channels.",
    },
    {
        "id": "T1486",
        "name": "Data Encrypted for Impact",
        "tactic": "Impact",
        "description": "Adversaries may encrypt data on target systems or on large numbers of systems to interrupt availability (ransomware).",
        "mitigations": ["M1053 - Data Backup", "M1040 - Behavior Prevention on Endpoint"],
        "detection": "Monitor for mass file encryption operations and ransom notes.",
    },
    {
        "id": "T1003",
        "name": "OS Credential Dumping",
        "tactic": "Credential Access",
        "description": "Adversaries may attempt to dump credentials to obtain account login and credential material.",
        "mitigations": ["M1040 - Behavior Prevention", "M1043 - Credential Access Protection", "M1027 - Password Policies"],
        "detection": "Monitor for access to credential stores (SAM, LSASS, /etc/shadow).",
    },
    {
        "id": "T1070",
        "name": "Indicator Removal",
        "tactic": "Defense Evasion",
        "description": "Adversaries may delete or modify artifacts generated within systems to remove evidence of their presence or hinder defenses.",
        "mitigations": ["M1029 - Remote Data Storage", "M1041 - Encrypt Sensitive Information"],
        "detection": "Monitor for file deletion of logs and audit trails.",
    },
]


@dataclass
class MitreAttackSource:
    """MITRE ATT&CK knowledge source for RAG pipeline.

    Provides technique descriptions, mitigations, and detection strategies
    from the MITRE ATT&CK framework as documents for vector embedding.
    """

    name: str = "mitre_attack"
    description: str = "MITRE ATT&CK Enterprise techniques, mitigations, and detection strategies"
    _techniques: list = field(default_factory=lambda: MITRE_ATTACK_TECHNIQUES)

    def load_documents(self) -> list[Document]:
        """Load MITRE ATT&CK techniques as documents for RAG indexing."""
        documents = []
        for tech in self._techniques:
            content = self._format_technique(tech)
            doc = Document(
                content=content,
                metadata={
                    "source": "mitre_attack",
                    "technique_id": tech["id"],
                    "technique_name": tech["name"],
                    "tactic": tech["tactic"],
                },
            )
            documents.append(doc)
        return documents

    def load_chunks(self) -> list[Chunk]:
        """Load MITRE ATT&CK techniques as pre-chunked items."""
        chunks = []
        for tech in self._techniques:
            content = self._format_technique(tech)
            chunk = Chunk(
                content=content,
                metadata={
                    "source": "mitre_attack",
                    "technique_id": tech["id"],
                    "technique_name": tech["name"],
                    "tactic": tech["tactic"],
                },
            )
            chunks.append(chunk)
        return chunks

    def search(self, query: str) -> list[dict]:
        """Search techniques by keyword."""
        query_lower = query.lower()
        results = []
        for tech in self._techniques:
            text = f"{tech['name']} {tech['description']} {tech['tactic']}"
            if query_lower in text.lower():
                results.append(tech)
        return results

    def get_by_tactic(self, tactic: str) -> list[dict]:
        """Get all techniques for a given tactic."""
        return [t for t in self._techniques if t["tactic"].lower() == tactic.lower()]

    def _format_technique(self, tech: dict) -> str:
        """Format a technique as readable text."""
        lines = [
            f"MITRE ATT&CK Technique: {tech['id']} - {tech['name']}",
            f"Tactic: {tech['tactic']}",
            f"\nDescription:\n{tech['description']}",
            "\nMitigations:",
        ]
        for m in tech.get("mitigations", []):
            lines.append(f"  - {m}")
        lines.append(f"\nDetection:\n{tech.get('detection', 'N/A')}")
        return "\n".join(lines)

    async def fetch_latest(self) -> bool:
        """Fetch latest MITRE ATT&CK data from GitHub (STIX format).

        Returns True if successfully updated, False otherwise.
        """
        import httpx

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(MITRE_ATTACK_URL)
                response.raise_for_status()
                data = response.json()

            techniques = []
            objects = data.get("objects", [])
            for obj in objects:
                if obj.get("type") == "attack-pattern" and not obj.get("revoked"):
                    tech_id = ""
                    for ref in obj.get("external_references", []):
                        if ref.get("source_name") == "mitre-attack":
                            tech_id = ref.get("external_id", "")
                            break

                    if tech_id:
                        tactic = ""
                        kill_chain = obj.get("kill_chain_phases", [])
                        if kill_chain:
                            tactic = kill_chain[0].get("phase_name", "").replace("-", " ").title()

                        techniques.append({
                            "id": tech_id,
                            "name": obj.get("name", ""),
                            "tactic": tactic,
                            "description": obj.get("description", ""),
                            "mitigations": [],
                            "detection": "",
                        })

            if techniques:
                self._techniques = techniques
                return True
        except Exception:
            pass
        return False
