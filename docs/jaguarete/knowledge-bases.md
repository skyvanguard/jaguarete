# Jaguarete Knowledge Bases

Jaguarete integrates 3 external knowledge bases into its RAG (Retrieval-Augmented Generation) pipeline. These knowledge sources provide security agents with real-time threat intelligence, vulnerability data, and best practices.

## RAG Pipeline Overview

The RAG pipeline enhances agent decision-making by:

1. **Document Loading:** Knowledge sources are converted to documents
2. **Chunking:** Large documents split for efficient retrieval
3. **Embedding:** Text converted to vector representations
4. **Indexing:** Vectors stored in vector database
5. **Retrieval:** Relevant chunks retrieved based on user query
6. **Augmentation:** Retrieved context injected into LLM prompt
7. **Generation:** LLM generates response using knowledge context

### Enabling RAG for an Agent

```python
from jaguarete_agents.blue import ThreatHunterAgent
from jaguarete_knowledge.sources import MitreAttackSource

# Create agent with knowledge source
agent = ThreatHunterAgent(llm_provider="openai")
agent.add_knowledge_source(MitreAttackSource())

# Agent now has access to MITRE ATT&CK techniques
response = await agent.chat("What are T1595 detection strategies?")
```

---

## MITRE ATT&CK Knowledge Source

**Source Name:** `mitre_attack`
**Coverage:** 15+ techniques (Reconnaissance to Impact)
**Format:** JSON with technique IDs, tactics, descriptions, mitigations
**Update Frequency:** Bi-weekly (fetches from MITRE GitHub)

### What It Contains

The MITRE ATT&CK source contains:

- **Technique ID:** Unique identifier (e.g., T1595)
- **Technique Name:** Human-readable name (e.g., "Active Scanning")
- **Tactic:** Kill chain phase (Reconnaissance, Execution, etc.)
- **Description:** Detailed explanation of the technique
- **Mitigations:** Security controls to prevent the technique
- **Detection:** Methods to identify the technique in use

### Embedded Techniques

Currently includes 15 core Enterprise techniques:

| ID | Name | Tactic | Use Case |
|----|----|-------|----------|
| T1595 | Active Scanning | Reconnaissance | Network enumeration |
| T1592 | Gather Victim Host Information | Reconnaissance | System profiling |
| T1190 | Exploit Public-Facing Application | Initial Access | Web vulnerability exploitation |
| T1566 | Phishing | Initial Access | Social engineering |
| T1059 | Command and Scripting Interpreter | Execution | Command execution |
| T1078 | Valid Accounts | Persistence | Account abuse |
| T1068 | Exploitation for Privilege Escalation | Privilege Escalation | Privilege elevation |
| T1055 | Process Injection | Defense Evasion | Evasion technique |
| T1110 | Brute Force | Credential Access | Password attacks |
| T1046 | Network Service Discovery | Discovery | Service enumeration |
| T1021 | Remote Services | Lateral Movement | SSH/RDP abuse |
| T1041 | Exfiltration Over C2 Channel | Exfiltration | Data theft |
| T1486 | Data Encrypted for Impact | Impact | Ransomware |
| T1003 | OS Credential Dumping | Credential Access | Credential theft |
| T1070 | Indicator Removal | Defense Evasion | Log deletion |

### Searching MITRE ATT&CK

```python
from jaguarete_knowledge.sources import MitreAttackSource

mitre = MitreAttackSource()

# Search by keyword
results = mitre.search("phishing")
# Returns: [T1566 - Phishing technique]

# Get techniques by tactic
execution_techniques = mitre.get_by_tactic("Execution")
# Returns: [T1059, ...]

# Load all techniques for RAG
documents = mitre.load_documents()
chunks = mitre.load_chunks()
```

### Using MITRE in Threat Hunting

```python
from jaguarete_agents.blue import ThreatHunterAgent
from jaguarete_knowledge.sources import MitreAttackSource

agent = ThreatHunterAgent(llm_provider="openai")
agent.add_knowledge_source(MitreAttackSource())

# Agent uses MITRE for technique lookup
response = await agent.chat(
    "We found scheduled tasks being created. What MITRE technique is this and how do we detect it?"
)
# Response references T1053 with detection methods
```

### Updating MITRE ATT&CK Data

```python
import asyncio
from jaguarete_knowledge.sources import MitreAttackSource

async def update_mitre():
    mitre = MitreAttackSource()
    # Fetches latest from https://github.com/mitre/cti
    success = await mitre.fetch_latest()
    if success:
        print("Updated MITRE ATT&CK data")
    else:
        print("Update failed, using embedded techniques")

asyncio.run(update_mitre())
```

### Use Cases

- **Threat Intelligence:** Map observed indicators to techniques
- **Detection Rule Creation:** Reference detection methods
- **Attack Simulation:** Plan red team exercises
- **Defense Assessment:** Evaluate coverage for techniques
- **Incident Response:** Understand attacker TTP (Tactics, Techniques, Procedures)

---

## NVD CVE Knowledge Source

**Source Name:** `nvd_cve`
**Coverage:** 250,000+ CVE entries
**API:** NVD API 2.0 integration
**Update Frequency:** Real-time (via NVD API)
**Format:** CVSS scores, affected products, published dates, references

### What It Contains

The NVD CVE source provides:

- **CVE ID:** Unique vulnerability identifier (CVE-YYYY-NNNNN)
- **CVSS v3.1 Score:** Severity rating (0-10)
- **Description:** Technical vulnerability description
- **CWE:** Weakness type (SQL Injection, XSS, etc.)
- **Affected Products:** Software and versions impacted
- **Published Date:** Public disclosure date
- **References:** Links to vendor advisories and patches
- **CPE:** Common Platform Enumeration (product identifiers)

### Sample CVE Records

```python
from jaguarete_knowledge.sources import NvdCveSource

nvd = NvdCveSource()

# Look up specific CVE
cve_2024_1234 = nvd.lookup("CVE-2024-1234")
# Returns:
# {
#   "cve_id": "CVE-2024-1234",
#   "cvss_score": 9.8,
#   "cvss_severity": "CRITICAL",
#   "description": "Remote code execution in OpenSSL...",
#   "affected_products": ["OpenSSL 1.0.0 - 1.1.1"],
#   "published": "2024-03-15",
#   "cwe_types": ["CWE-119 - Buffer Overflow"]
# }
```

### Searching NVD CVE

```python
from jaguarete_knowledge.sources import NvdCveSource

nvd = NvdCveSource()

# Search by keyword
openssl_cves = nvd.search("OpenSSL")

# Filter by severity
critical_cves = nvd.filter_by_severity("CRITICAL")

# Filter by date range
recent_cves = nvd.filter_by_date_range("2024-01-01", "2024-03-31")

# Filter by CWE
injection_cves = nvd.filter_by_cwe("CWE-89")  # SQL Injection
```

### NVD API Configuration

```bash
# Set NVD API key in environment
export NVD_API_KEY=your-api-key

# Optional: Set cache directory
export NVD_CACHE_DIR=/tmp/nvd-cache
```

```python
from jaguarete_knowledge.sources import NvdCveSource

nvd = NvdCveSource(
    api_key="your-api-key",
    cache_enabled=True,
    cache_ttl=86400,  # 24 hours
)
```

### Using CVE Data in Vulnerability Assessment

```python
from jaguarete_agents.red import VulnScannerAgent
from jaguarete_knowledge.sources import NvdCveSource

agent = VulnScannerAgent(llm_provider="openai")
agent.add_knowledge_source(NvdCveSource())

# Agent can look up CVE details during analysis
response = await agent.chat(
    "Analyze the vulnerabilities found in our OpenSSL version: "
    "List all known CVEs with CVSS scores"
)
# Response includes details from NVD for relevant CVEs
```

### Use Cases

- **Vulnerability Assessment:** Identify and score vulnerabilities
- **Patch Management:** Prioritize patches by CVSS and exploitability
- **Risk Scoring:** Calculate business impact
- **Compliance:** Verify remediation of known CVEs
- **Threat Intelligence:** Monitor emerging vulnerabilities
- **Asset Management:** Track vulnerable software versions

### Performance Optimization

```python
from jaguarete_knowledge.sources import NvdCveSource

# Use caching for frequent lookups
nvd = NvdCveSource(cache_enabled=True)

# Batch operations for efficiency
cves = ["CVE-2024-1234", "CVE-2024-5678", "CVE-2024-9012"]
details = nvd.batch_lookup(cves)

# Enable offline mode with cached data
nvd.set_offline_mode(True)
```

---

## OWASP Top 10 Knowledge Source

**Source Name:** `owasp`
**Version:** OWASP Top 10 2021
**Coverage:** All 10 risks with detailed descriptions
**Format:** Risk categories, examples, prevention methods
**Update Frequency:** On-demand (updated with new releases)

### OWASP Top 10 2021

The OWASP source covers all 10 critical web application security risks:

| Rank | Risk | Description |
|------|------|-------------|
| A01 | Broken Access Control | Users can act outside intended permissions |
| A02 | Cryptographic Failures | Data exposure due to weak/missing encryption |
| A03 | Injection | Untrusted data misinterpreted as commands |
| A04 | Insecure Design | Lack of security controls in design |
| A05 | Security Misconfiguration | Insecure defaults and incomplete configs |
| A06 | Vulnerable Components | Using components with known vulnerabilities |
| A07 | Authentication Failures | Weak authentication and session management |
| A08 | Software Data Integrity | Insecure CI/CD and dependency chain |
| A09 | Logging Monitoring Failures | Insufficient logging and detection |
| A10 | SSRF | Requests to unintended URLs |

### Detailed Risk Information

Each OWASP risk includes:

- **Description:** What the risk is and why it matters
- **Examples:** Real-world code examples (vulnerable and secure)
- **Impact:** Business and technical consequences
- **Detection Methods:** How to identify the risk
- **Prevention:** Security controls and best practices
- **References:** CWE mappings and further resources

### Searching OWASP

```python
from jaguarete_knowledge.sources import OwaspSource

owasp = OwaspSource()

# Get specific risk
a03_injection = owasp.get_risk("A03")

# Search by keyword
auth_risks = owasp.search("authentication")

# Get all risks
all_risks = owasp.load_documents()
```

### Using OWASP in Security Assessment

```python
from jaguarete_agents.red import VulnScannerAgent
from jaguarete_knowledge.sources import OwaspSource

agent = VulnScannerAgent(llm_provider="openai")
agent.add_knowledge_source(OwaspSource())

# Agent uses OWASP context during analysis
response = await agent.chat(
    "Review this web application against OWASP Top 10. "
    "List any vulnerabilities and remediation steps"
)
```

### A03:2021 - Injection Example

```markdown
# A03:2021 - Injection

## Description
Injection flaws occur when untrusted data is sent to an interpreter.
The attacker's hostile data can trick the interpreter into executing
unintended commands or accessing data without proper authorization.

## Example (Vulnerable Code)
```python
user_input = request.get("username")
query = f"SELECT * FROM users WHERE name = '{user_input}'"
db.execute(query)
```

## Example (Secure Code)
```python
user_input = request.get("username")
query = "SELECT * FROM users WHERE name = ?"
db.execute(query, [user_input])  # Parameterized query
```

## Prevention
1. Use parameterized queries/prepared statements
2. Input validation and sanitization
3. Whitelist allowed input
4. Escape special characters
5. Principle of least privilege for DB accounts
```

### Use Cases

- **Code Review:** Identify OWASP vulnerabilities
- **Penetration Testing:** Test for Top 10 risks
- **Secure Development:** Train developers on risks
- **Compliance:** Verify OWASP risk coverage
- **Risk Assessment:** Prioritize remediation efforts

---

## Using Multiple Knowledge Sources

### Combining Sources for Comprehensive Analysis

```python
from jaguarete_agents.red import VulnScannerAgent
from jaguarete_knowledge.sources import (
    MitreAttackSource,
    NvdCveSource,
    OwaspSource,
)

agent = VulnScannerAgent(llm_provider="openai")

# Add multiple knowledge sources
agent.add_knowledge_source(MitreAttackSource())
agent.add_knowledge_source(NvdCveSource())
agent.add_knowledge_source(OwaspSource())

# Agent now has comprehensive security knowledge
response = await agent.chat(
    "Analyze target.com for security vulnerabilities. "
    "Map findings to MITRE techniques, OWASP risks, and NVD CVEs"
)
```

### Knowledge Source Priority and Relevance

```python
# Configure source priorities (0-1, higher = more relevant)
agent.add_knowledge_source(
    MitreAttackSource(),
    priority=0.8,  # High priority for threat hunting
)
agent.add_knowledge_source(
    OwaspSource(),
    priority=0.7,  # Medium priority for web apps
)
```

---

## Creating Custom Knowledge Sources

### Step 1: Implement Knowledge Source Interface

```python
from dataclasses import dataclass
from jaguarete.core.interface.knowledge import Chunk, Document


@dataclass
class CustomSecuritySource:
    """Custom security knowledge source."""

    name: str = "custom_security"
    description: str = "Custom security framework"

    def load_documents(self) -> list[Document]:
        """Load documents for RAG indexing."""
        documents = []
        # Your implementation
        doc = Document(
            content="Document content",
            metadata={
                "source": "custom_security",
                "category": "category_name",
            },
        )
        documents.append(doc)
        return documents

    def load_chunks(self) -> list[Chunk]:
        """Load pre-chunked items."""
        chunks = []
        # Your implementation
        return chunks

    def search(self, query: str) -> list[dict]:
        """Search knowledge base by keyword."""
        # Your search implementation
        return results
```

### Step 2: Place in Knowledge Package

```
packages/jaguarete-knowledge/src/jaguarete_knowledge/sources/
├── mitre_attack.py
├── nvd_cve.py
├── owasp.py
└── custom_security.py  # Your custom source
```

### Step 3: Register in Package

```python
# packages/jaguarete-knowledge/src/jaguarete_knowledge/__init__.py
from jaguarete_knowledge.sources.custom_security import CustomSecuritySource

__all__ = ["CustomSecuritySource"]
```

---

## Knowledge Base Best Practices

1. **Keep Data Updated:** Regularly fetch latest threat intelligence
2. **Monitor Performance:** Profile RAG retrieval speed
3. **Relevance Tuning:** Adjust search parameters and priorities
4. **Data Quality:** Validate knowledge source accuracy
5. **Privacy:** Don't include sensitive data in knowledge bases
6. **Versioning:** Track knowledge source versions for audit trails

---

## Troubleshooting Knowledge Sources

### Source Not Available to Agent

```python
# Verify source registration
from jaguarete_knowledge.sources import MitreAttackSource

mitre = MitreAttackSource()
docs = mitre.load_documents()
print(f"Loaded {len(docs)} documents")
```

### Search Not Returning Results

```python
# Test search directly
results = mitre.search("phishing")
print(f"Found {len(results)} results")

# Adjust search parameters
results = mitre.search("phishing", case_sensitive=False)
```

### API Rate Limits (NVD)

```python
# Use caching to reduce API calls
nvd = NvdCveSource(cache_enabled=True, cache_ttl=86400)

# Or batch requests
cves = nvd.batch_lookup(cve_list)
```

---

## References

- **MITRE ATT&CK:** https://attack.mitre.org/
- **NVD:** https://nvd.nist.gov/
- **OWASP:** https://owasp.org/Top10/
- **Knowledge Bases Implementation:** `/packages/jaguarete-knowledge/src/`
