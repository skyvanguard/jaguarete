# Jaguarete Agents Guide

Jaguarete provides 8 specialized AI agents organized into three teams: Red Team (offensive), Blue Team (defensive), and Purple Team (coordination). All agents inherit from `ConversableAgent` and use the `ProfileConfig` system for dynamic configuration.

## Agent Architecture

### Base Agent: ConversableAgent

All Jaguarete agents extend `ConversableAgent`, providing:

- **Profile Configuration**: Dynamic role, goal, and constraints via `ProfileConfig`
- **Tool Integration**: Access to security scanning and analysis tools
- **Memory Management**: Short-term and long-term conversation memory
- **RAG Pipeline**: Integration with knowledge bases (MITRE, CVE, OWASP)
- **LLM Flexibility**: Works with OpenAI, Anthropic, Ollama

### ProfileConfig Structure

```python
from jaguarete.agent.core.profile import ProfileConfig, DynConfig

agent.profile = ProfileConfig(
    name=DynConfig("AgentName", category="agent", key="config_key"),
    role=DynConfig("Security Specialist", category="agent", key="role_key"),
    goal=DynConfig("Achieve security objective", category="agent", key="goal_key"),
    constraints=DynConfig([
        "Constraint 1",
        "Constraint 2",
    ], category="agent", key="constraints_key"),
)
```

## Red Team Agents

Red Team agents perform offensive security operations to identify weaknesses.

### ReconAgent - Reconnaissance Specialist

**Purpose:** Gather intelligence on authorized targets through passive and active reconnaissance.

**Capabilities:**
- Domain enumeration and WHOIS lookups
- DNS record enumeration (A, AAAA, MX, NS, TXT, CNAME)
- Port scanning and service detection
- Subdomain discovery
- Attack surface identification

**Authorization Model:**
- Requires explicit target authorization before scanning
- Starts with passive reconnaissance
- Documents all findings with timestamps
- Flags high-severity findings immediately

**Example Usage:**

```python
from jaguarete_agents.red import ReconAgent

agent = ReconAgent(llm_provider="openai")

# Request reconnaissance
response = await agent.chat(
    "Enumerate all DNS records for example.com and identify open ports on 192.168.1.0/24"
)
```

**RBAC Access:** `analyst`, `admin`

---

### VulnScannerAgent - Vulnerability Detection Specialist

**Purpose:** Identify and catalog security vulnerabilities in systems and applications.

**Capabilities:**
- Vulnerability scanning using OpenVAS/Nessus integration
- CVE lookup and severity assessment
- Configuration review against security benchmarks
- Dependency analysis for known vulnerabilities
- CVSS scoring and prioritization

**Analysis Focus:**
- Application vulnerabilities (SQL injection, XSS, RCE)
- System weaknesses (misconfiguration, weak credentials)
- Dependency risks (outdated libraries)
- Service-specific vulnerabilities

**Example Usage:**

```python
from jaguarete_agents.red import VulnScannerAgent

agent = VulnScannerAgent(llm_provider="openai")

response = await agent.chat(
    "Scan the web application at http://target.local:8080 for OWASP Top 10 vulnerabilities"
)
```

**RBAC Access:** `analyst`, `admin`

---

### ExploitAnalystAgent - Exploitation Specialist

**Purpose:** Analyze exploit chains, proof-of-concept code, and post-exploitation scenarios.

**Capabilities:**
- Exploit chain analysis (initial access → persistence → exfiltration)
- PoC code review and safety assessment
- Attack path visualization
- Payload analysis and behavior prediction
- Post-exploitation scenario planning

**Safety Features:**
- Never executes actual exploits (analysis only)
- Flags dangerous PoC code patterns
- Provides mitigation recommendations
- Documents findings for incident response

**Example Usage:**

```python
from jaguarete_agents.red import ExploitAnalystAgent

agent = ExploitAnalystAgent(llm_provider="anthropic")

response = await agent.chat(
    "Analyze the exploitation path for CVE-2024-1234: initial access → lateral movement → data exfiltration"
)
```

**RBAC Access:** `analyst`, `admin`

---

## Blue Team Agents

Blue Team agents perform defensive security operations to detect, investigate, and respond to threats.

### LogAnalystAgent - Log Analysis Specialist

**Purpose:** Analyze system and application logs to detect anomalies and indicators of compromise.

**Capabilities:**
- Real-time log parsing and correlation
- Sigma rule-based threat detection
- Event timeline reconstruction
- Anomaly detection (statistical and behavioral)
- IoC (Indicator of Compromise) extraction

**Data Sources:**
- Syslog (Linux/Unix)
- Windows Event Log
- Web server logs (Apache, Nginx)
- Application logs (JSON, plaintext)
- IDS/IPS alerts

**Example Usage:**

```python
from jaguarete_agents.blue import LogAnalystAgent

agent = LogAnalystAgent(llm_provider="openai")

response = await agent.chat(
    "Analyze /var/log/auth.log for failed SSH attempts and potential brute force attacks"
)
```

**RBAC Access:** `analyst`, `admin`

---

### IncidentResponderAgent - Incident Response Coordinator

**Purpose:** Orchestrate incident response activities and guide response teams through procedures.

**Capabilities:**
- Incident assessment and triage
- NIST Incident Response Framework integration
- Playbook execution and adaptation
- Escalation procedure management
- Evidence collection coordination

**Response Phases:**
1. **Preparation:** System hardening, detection setup
2. **Detection:** Alert analysis and confirmation
3. **Containment:** Isolate affected systems
4. **Eradication:** Remove attack artifacts
5. **Recovery:** Restore and verify systems
6. **Post-Incident:** Analysis and lessons learned

**Example Usage:**

```python
from jaguarete_agents.blue import IncidentResponderAgent

agent = IncidentResponderAgent(llm_provider="anthropic")

response = await agent.chat(
    "We detected ransomware on Server-DC1. Guide containment and recovery steps"
)
```

**RBAC Access:** `analyst`, `admin`

---

### ThreatHunterAgent - Threat Hunting Specialist

**Purpose:** Proactively hunt for signs of compromise and advanced threats.

**Capabilities:**
- Behavioral threat hunting (hypothesis-driven)
- IOC correlation across systems
- MITRE ATT&CK technique mapping
- TTP (Tactics, Techniques, Procedures) analysis
- Threat intelligence integration

**Hunting Methodologies:**
- Chain analysis (finding related indicators)
- Timeline analysis (event sequencing)
- Baseline comparison (detecting deviations)
- Hypothesis testing (confirming attack patterns)

**Example Usage:**

```python
from jaguarete_agents.blue import ThreatHunterAgent

agent = ThreatHunterAgent(llm_provider="openai")

response = await agent.chat(
    "Hunt for signs of APT28 activity (T1595, T1046, T1021) in our network logs"
)
```

**RBAC Access:** `analyst`, `admin`

---

## Purple Team Agents

Purple Team agents coordinate offensive and defensive operations for comprehensive security assessments.

### AttackSurfaceAgent - Attack Surface Mapper

**Purpose:** Map the complete attack surface and identify high-risk areas.

**Capabilities:**
- External-facing asset inventory
- Attack surface visualization
- Risk scoring by attack path
- Interdependency analysis
- Defensive gap identification

**Analysis Output:**
- Asset inventory (domains, IPs, services)
- Attack paths (how attackers might enter)
- Defensive gaps (missing controls)
- Remediation priorities (ROI-based)

**Example Usage:**

```python
from jaguarete_agents.purple import AttackSurfaceAgent

agent = AttackSurfaceAgent(llm_provider="openai")

response = await agent.chat(
    "Map the attack surface for acme-corp.com including all subdomains, VPNs, and third-party integrations"
)
```

**RBAC Access:** `analyst`, `admin`

---

### ReportGeneratorAgent - Report Generation Specialist

**Purpose:** Create comprehensive security assessment reports for stakeholders.

**Capabilities:**
- Multi-format report generation (PDF, HTML, Markdown)
- Executive summary creation
- Technical finding documentation
- Risk rating and prioritization
- Remediation roadmap planning

**Report Types:**
- **Pentest Reports:** Vulnerabilities, exploitation paths, remediation
- **Threat Assessment:** Threat landscape, APT targeting, mitigation
- **Compliance Reports:** Control assessment against frameworks
- **Risk Analysis:** CVSS scoring, business impact, ROI analysis

**Example Usage:**

```python
from jaguarete_agents.purple import ReportGeneratorAgent

agent = ReportGeneratorAgent(llm_provider="anthropic")

response = await agent.chat(
    "Create an executive summary report from our red team assessment findings"
)
```

**RBAC Access:** `admin` (report generation), `analyst` (viewing)

---

## Agent Access Control (RBAC)

| Agent | Viewer | Analyst | Admin |
|-------|--------|---------|-------|
| ReconAgent | ✗ | ✓ | ✓ |
| VulnScannerAgent | ✗ | ✓ | ✓ |
| ExploitAnalystAgent | ✗ | ✓ | ✓ |
| LogAnalystAgent | ✗ | ✓ | ✓ |
| IncidentResponderAgent | ✗ | ✓ | ✓ |
| ThreatHunterAgent | ✗ | ✓ | ✓ |
| AttackSurfaceAgent | ✓ | ✓ | ✓ |
| ReportGeneratorAgent | ✓* | ✓ | ✓ |

*Viewers can see reports but not initiate generation

## Creating Custom Agents

### Step 1: Extend ConversableAgent

```python
from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class CustomSecurityAgent(ConversableAgent):
    """Your custom security agent."""

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig("CustomAgent", category="agent", key="custom_agent_name"),
        role=DynConfig("Custom Specialist", category="agent", key="custom_agent_role"),
        goal=DynConfig("Achieve custom objective", category="agent", key="custom_agent_goal"),
        constraints=DynConfig(
            ["Constraint 1", "Constraint 2"],
            category="agent",
            key="custom_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize custom agent."""
        super().__init__(**kwargs)
```

### Step 2: Register in API

```python
# packages/jaguarete-app/src/jaguarete_app/api/agents.py
from jaguarete_agents.custom import CustomSecurityAgent

@router.post("/custom")
async def run_custom_agent(request: AgentRequest):
    agent = CustomSecurityAgent(llm_provider=request.llm_provider)
    response = await agent.chat(request.prompt)
    return {"response": response}
```

### Step 3: Use in Dashboard

```javascript
// web/app/api/agents.ts
export const agents = [
  // ... existing agents
  {
    id: "custom",
    name: "Custom Agent",
    team: "custom",
    description: "Your custom security agent",
  },
];
```

## Agent Configuration

### Environment Variables

```bash
# LLM Configuration
JAGUARETE_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Agent Behavior
JAGUARETE_AGENT_TIMEOUT=300  # seconds
JAGUARETE_AGENT_MEMORY_SIZE=10  # conversations to remember
```

### Runtime Configuration

```python
from jaguarete_agents.red import ReconAgent

agent = ReconAgent(
    llm_provider="openai",
    model="gpt-4o",  # specific model
    temperature=0.5,  # reasoning vs creativity
    max_tokens=4000,
)
```

## Agent Communication Patterns

### Agent-to-Agent Collaboration

```python
from jaguarete_agents.red import ReconAgent
from jaguarete_agents.blue import LogAnalystAgent

# Red team reconnaissance findings
recon = ReconAgent()
recon_findings = await recon.chat("Scan target.com")

# Blue team log analysis with findings context
log_analyst = LogAnalystAgent()
response = await log_analyst.chat(
    f"Given these attack paths: {recon_findings}, analyze our logs for matching indicators"
)
```

### Team Coordination

```python
from jaguarete_agents.purple import AttackSurfaceAgent, ReportGeneratorAgent

# Map attack surface
mapper = AttackSurfaceAgent()
attack_surface = await mapper.chat("Map attack surface for acme.com")

# Generate report
reporter = ReportGeneratorAgent()
report = await reporter.chat(
    f"Create security report based on: {attack_surface}"
)
```

## Troubleshooting Agents

### Agent Not Responding

```python
# Check agent initialization
agent = ReconAgent(llm_provider="openai")
print(agent.profile.name)
print(agent.profile.role)

# Test with simple prompt
response = await agent.chat("Hello, what can you do?")
```

### LLM Integration Issues

```python
# Verify LLM availability
from jaguarete.core.llm import get_llm_instance

llm = get_llm_instance("openai")
test = await llm.agenerate("Test prompt")
```

### Memory and Context

```python
# View agent memory
memory = agent.memory
print(memory.conversation_history)
print(memory.token_usage)
```

## Best Practices

1. **Clear Instructions:** Provide specific, detailed prompts for better results
2. **Context:** Include relevant background information (scope, targets, past findings)
3. **Constraints:** Always specify authorization boundaries
4. **Verification:** Double-check agent findings, especially for critical decisions
5. **Escalation:** Hand off complex decisions to human analysts
6. **Documentation:** Record all agent operations for audit trails

## References

- **MITRE ATT&CK:** Accessed via ThreatHunterAgent and knowledge base
- **OWASP Top 10:** Referenced by VulnScannerAgent
- **NIST Framework:** Used by IncidentResponderAgent
- **CVE/NVD:** Integrated in all vulnerability agents
