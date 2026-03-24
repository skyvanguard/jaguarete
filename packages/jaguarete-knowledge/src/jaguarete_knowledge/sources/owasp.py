"""OWASP Top 10 knowledge source for RAG pipeline."""
from dataclasses import dataclass, field

from jaguarete.core.interface.knowledge import Chunk, Document


OWASP_TOP_10_2021 = [
    {
        "id": "A01",
        "name": "Broken Access Control",
        "description": "Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits.",
        "examples": [
            "Violation of the principle of least privilege",
            "Bypassing access control checks by modifying the URL",
            "Permitting viewing or editing someone else's account",
            "Accessing API with missing access controls for POST, PUT and DELETE",
            "Elevation of privilege (acting as a user without being logged in)",
        ],
        "prevention": [
            "Deny by default except for public resources",
            "Implement access control mechanisms once and re-use them throughout the application",
            "Model access controls should enforce record ownership",
            "Disable web server directory listing",
            "Log access control failures and alert admins",
            "Rate limit API and controller access",
        ],
    },
    {
        "id": "A02",
        "name": "Cryptographic Failures",
        "description": "Failures related to cryptography which often lead to sensitive data exposure. This includes the use of weak or outdated cryptographic algorithms, insufficient key management, and transmission of data in clear text.",
        "examples": ["Data transmitted in clear text (HTTP, SMTP, FTP)", "Old or weak cryptographic algorithms", "Default or weak crypto keys", "Missing proper certificate validation"],
        "prevention": ["Classify data and apply controls", "Encrypt all data in transit with TLS", "Disable caching for sensitive data", "Use strong adaptive hashing for passwords"],
    },
    {
        "id": "A03",
        "name": "Injection",
        "description": "Injection flaws such as SQL, NoSQL, OS, and LDAP injection occur when untrusted data is sent to an interpreter as part of a command or query. The attacker's hostile data can trick the interpreter into executing unintended commands.",
        "examples": ["SQL injection", "NoSQL injection", "OS command injection", "LDAP injection", "Cross-site Scripting (XSS)", "Server-Side Template Injection (SSTI)"],
        "prevention": ["Use parameterized queries / prepared statements", "Use positive server-side input validation", "Escape special characters", "Use LIMIT and other SQL controls to prevent mass disclosure"],
    },
    {
        "id": "A04",
        "name": "Insecure Design",
        "description": "Insecure design is a broad category representing different weaknesses expressed as missing or ineffective control design. Insecure design is not the source for all other Top 10 risk categories.",
        "examples": ["Missing rate limiting on sensitive operations", "No fraud protection in business logic", "Missing threat modeling during design", "Lack of security requirements"],
        "prevention": ["Establish secure development lifecycle", "Use threat modeling for critical flows", "Integrate security in user stories", "Use secure design patterns"],
    },
    {
        "id": "A05",
        "name": "Security Misconfiguration",
        "description": "Security misconfiguration is the most commonly seen issue. This is commonly a result of insecure default configurations, incomplete or ad hoc configurations, open cloud storage, misconfigured HTTP headers, and verbose error messages.",
        "examples": ["Unnecessary features enabled", "Default accounts with unchanged passwords", "Overly informative error messages", "Missing security headers", "Outdated software"],
        "prevention": ["Repeatable hardening process", "Minimal platform with no unnecessary features", "Review and update configurations", "Segmented architecture", "Automated configuration verification"],
    },
    {
        "id": "A06",
        "name": "Vulnerable and Outdated Components",
        "description": "Components such as libraries, frameworks, and software modules run with the same privileges as the application. If a vulnerable component is exploited, such an attack can facilitate serious data loss or server takeover.",
        "examples": ["Running components with known vulnerabilities", "Not knowing versions of all components", "Software that is unsupported or out of date", "Not scanning for vulnerabilities regularly"],
        "prevention": ["Remove unused dependencies", "Continuously inventory component versions", "Monitor CVE databases", "Only obtain components from official sources", "Monitor for unmaintained components"],
    },
    {
        "id": "A07",
        "name": "Identification and Authentication Failures",
        "description": "Confirmation of the user's identity, authentication, and session management is critical to protect against authentication-related attacks.",
        "examples": ["Permits brute force attacks", "Permits weak passwords", "Uses plain text or weakly hashed passwords", "Missing or ineffective multi-factor authentication", "Session IDs in URLs"],
        "prevention": ["Implement multi-factor authentication", "Do not deploy with default credentials", "Implement weak password checks", "Harden account recovery paths", "Limit failed login attempts"],
    },
    {
        "id": "A08",
        "name": "Software and Data Integrity Failures",
        "description": "Software and data integrity failures relate to code and infrastructure that does not protect against integrity violations. This includes insecure CI/CD pipelines and auto-update mechanisms.",
        "examples": ["Using untrusted CDNs or repositories", "Insecure CI/CD pipeline", "Auto-update without integrity verification", "Insecure deserialization"],
        "prevention": ["Use digital signatures to verify software", "Ensure CI/CD pipeline has proper access control", "Review code and configuration changes", "Verify data integrity with checksums"],
    },
    {
        "id": "A09",
        "name": "Security Logging and Monitoring Failures",
        "description": "This category helps detect, escalate, and respond to active breaches. Without logging and monitoring, breaches cannot be detected.",
        "examples": ["Auditable events not logged", "Warnings and errors generate no log messages", "Logs not monitored for suspicious activity", "No alerting thresholds or escalation"],
        "prevention": ["Log all login, access control, and server-side input validation failures", "Ensure logs are in a format easily consumed by log management solutions", "Establish effective monitoring and alerting", "Establish incident response and recovery plan"],
    },
    {
        "id": "A10",
        "name": "Server-Side Request Forgery (SSRF)",
        "description": "SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL. It allows an attacker to coerce the application to send a crafted request to an unexpected destination.",
        "examples": ["Fetching remote URLs without validation", "Accessing cloud metadata services", "Internal port scanning via the application", "Accessing internal services behind firewalls"],
        "prevention": ["Sanitize and validate all client-supplied input data", "Enforce URL schema, port, and destination with allowlist", "Disable HTTP redirections", "Do not send raw responses to clients"],
    },
]


@dataclass
class OwaspSource:
    """OWASP Top 10 knowledge source for RAG pipeline.

    Provides OWASP Top 10 (2021) vulnerability categories with descriptions,
    examples, and prevention strategies as documents for vector embedding.
    """

    name: str = "owasp_top10"
    description: str = "OWASP Top 10 Web Application Security Risks (2021)"
    _entries: list = field(default_factory=lambda: OWASP_TOP_10_2021)

    def load_documents(self) -> list[Document]:
        """Load OWASP Top 10 entries as documents for RAG indexing."""
        documents = []
        for entry in self._entries:
            content = self._format_entry(entry)
            doc = Document(
                content=content,
                metadata={
                    "source": "owasp_top10",
                    "owasp_id": entry["id"],
                    "category_name": entry["name"],
                },
            )
            documents.append(doc)
        return documents

    def load_chunks(self) -> list[Chunk]:
        """Load OWASP entries as pre-chunked items."""
        chunks = []
        for entry in self._entries:
            content = self._format_entry(entry)
            chunk = Chunk(
                content=content,
                metadata={
                    "source": "owasp_top10",
                    "owasp_id": entry["id"],
                    "category_name": entry["name"],
                },
            )
            chunks.append(chunk)
        return chunks

    def search(self, query: str) -> list[dict]:
        """Search OWASP entries by keyword."""
        query_lower = query.lower()
        results = []
        for entry in self._entries:
            text = f"{entry['name']} {entry['description']} {' '.join(entry.get('examples', []))}"
            if query_lower in text.lower():
                results.append(entry)
        return results

    def get_by_id(self, owasp_id: str) -> dict | None:
        """Get a specific OWASP category by ID (e.g., 'A01')."""
        for entry in self._entries:
            if entry["id"] == owasp_id.upper():
                return entry
        return None

    def _format_entry(self, entry: dict) -> str:
        """Format an OWASP entry as readable text."""
        lines = [
            f"OWASP Top 10 - {entry['id']}: {entry['name']}",
            f"\nDescription:\n{entry['description']}",
            "\nExamples:",
        ]
        for ex in entry.get("examples", []):
            lines.append(f"  - {ex}")
        lines.append("\nPrevention:")
        for p in entry.get("prevention", []):
            lines.append(f"  - {p}")
        return "\n".join(lines)
