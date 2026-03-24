# Jaguarete Tools Reference

Jaguarete provides 10 specialized security tools organized into 5 categories. All tools use the `@tool` decorator pattern and are automatically available to agents through the RAG pipeline.

## Tool System Overview

### @tool Decorator

All Jaguarete tools are defined using the `@tool` decorator:

```python
from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Tool description for LLM")
def my_tool(
    param1: Annotated[str, Doc("Parameter documentation")],
    param2: Annotated[int, Doc("Another parameter")] = 10,
) -> str:
    """Tool implementation with full documentation."""
    # Implementation
    return result
```

### Tool Integration with Agents

Tools are automatically available to all agents:

```python
from jaguarete_agents.red import ReconAgent

agent = ReconAgent(llm_provider="openai")

# Agent can call tools in its response
response = await agent.chat(
    "Use dns_enum to enumerate example.com DNS records"
)
```

### Tool Parameters

- **description:** Brief description for LLM (50-100 chars)
- **Annotated types:** Use `Annotated[Type, Doc("...")]` for parameter documentation
- **Return type:** Always specify return type (str, dict, list)
- **Default values:** Optional parameters with sensible defaults

---

## Reconnaissance Tools

Tools for gathering information about targets.

### dns_enum - DNS Record Enumeration

**Category:** Recon

**Purpose:** Enumerate DNS records for a target domain.

**Parameters:**
- `domain` (str, required): Target domain to enumerate
- `record_types` (str, optional): Comma-separated DNS record types
  - Default: "A,AAAA,MX,NS,TXT,CNAME"
  - Supported: A, AAAA, MX, NS, TXT, CNAME, SOA, SRV

**Returns:** Formatted DNS information including IP addresses and record types

**Example:**

```python
response = dns_enum(
    domain="example.com",
    record_types="A,AAAA,MX,NS"
)
# Output:
# DNS Enumeration for: example.com
# ==================================================
# A: 93.184.216.34
# AAAA: 2606:2800:220:1:248:1893:25c8:1946
# MX: mail.example.com -> 93.184.216.36
# NS: ns1.example.com -> 93.184.216.35
```

**Use Cases:**
- Domain reconnaissance
- Subdomain discovery
- Email server identification
- Infrastructure mapping

**Time to Execute:** < 1 second (local)

---

### port_scan - Network Port Scanning

**Category:** Recon

**Purpose:** Scan a host or network for open ports and services.

**Parameters:**
- `target` (str, required): IP address, hostname, or CIDR range
- `ports` (str, optional): Port range or list (e.g., "1-65535", "80,443,22")
  - Default: "1-1024" (well-known ports)
- `timeout` (int, optional): Timeout per port in seconds
  - Default: 2

**Returns:** List of open ports with service information

**Example:**

```python
response = port_scan(
    target="192.168.1.100",
    ports="1-1000"
)
# Output:
# Port Scan Results for: 192.168.1.100
# ========================================
# 22 (ssh) - OPEN
# 80 (http) - OPEN
# 443 (https) - OPEN
# 3306 (mysql) - OPEN
# 5432 (postgresql) - OPEN
```

**Use Cases:**
- Service discovery
- Infrastructure reconnaissance
- Network baseline establishment
- Attack surface mapping

**Time to Execute:** 30-300 seconds (depends on port range)

**Note:** Requires proper authorization before scanning

---

### whois_lookup - WHOIS Domain Information

**Category:** Recon

**Purpose:** Retrieve WHOIS information for a domain.

**Parameters:**
- `domain` (str, required): Domain name to look up

**Returns:** Domain registration details (registrar, registrant, dates)

**Example:**

```python
response = whois_lookup(domain="example.com")
# Output:
# WHOIS Information for: example.com
# ====================================
# Registrar: VeriSign Global Registry Services
# Registrant: ICANN
# Created: 1995-08-14
# Expires: 2025-08-13
# Status: ok
```

**Use Cases:**
- Domain owner identification
- Registration timeline analysis
- Registrar research
- Passive reconnaissance

**Time to Execute:** < 2 seconds

---

## Intelligence Tools

Tools for analyzing threats and vulnerabilities.

### cve_lookup - CVE Database Search

**Category:** Intel

**Purpose:** Look up Common Vulnerabilities and Exposures from NVD.

**Parameters:**
- `cve_id` (str, required): CVE identifier (e.g., "CVE-2024-1234")
- `include_details` (bool, optional): Include full vulnerability details
  - Default: True

**Returns:** CVE information including CVSS score, description, and affected products

**Example:**

```python
response = cve_lookup(cve_id="CVE-2024-1234", include_details=True)
# Output:
# CVE-2024-1234: Remote Code Execution in OpenSSL
# ================================================
# CVSS v3.1: 9.8 (CRITICAL)
# Description: An attacker can execute arbitrary code...
# Affected: OpenSSL 1.0.0 - 1.1.1
# Published: 2024-03-15
# References: [NIST, MITRE, Vendor]
```

**Use Cases:**
- Vulnerability assessment
- Risk scoring
- Patch priority determination
- Compliance verification

**Time to Execute:** < 1 second (local database)

---

### mitre_attack_map - MITRE ATT&CK Mapping

**Category:** Intel

**Purpose:** Map indicators of compromise to MITRE ATT&CK techniques.

**Parameters:**
- `indicators` (str, required): Comma-separated indicators (processes, files, IPs)
- `tactic_filter` (str, optional): Filter by tactic (e.g., "Execution", "Persistence")
  - Default: None (all tactics)

**Returns:** Matched techniques with tactic, description, and mitigations

**Example:**

```python
response = mitre_attack_map(
    indicators="cmd.exe,powershell.exe,schtasks.exe",
    tactic_filter="Execution"
)
# Output:
# MITRE ATT&CK Mapping Results
# ============================
# T1059 - Command and Scripting Interpreter (Execution)
#   Description: Adversaries may abuse command interpreters...
#   Mitigations: M1049 - Antivirus/Antimalware
# T1053 - Scheduled Task/Job (Persistence)
#   Description: Adversaries may use scheduled tasks...
```

**Use Cases:**
- Threat intelligence analysis
- Attack technique identification
- TTP (Tactics, Techniques, Procedures) mapping
- Detection rule development

**Time to Execute:** < 500ms

---

## Forensics Tools

Tools for log analysis and evidence collection.

### log_parser - Structured Log Analysis

**Category:** Forensics

**Purpose:** Parse and extract structured data from various log formats.

**Parameters:**
- `log_source` (str, required): Log file path or log type
- `format` (str, optional): Log format (syslog, json, windows_event, apache, nginx)
  - Auto-detect if not specified
- `filter_pattern` (str, optional): Regex pattern to filter entries

**Returns:** Parsed log entries with extracted fields

**Example:**

```python
response = log_parser(
    log_source="/var/log/auth.log",
    format="syslog",
    filter_pattern="Failed password"
)
# Output:
# Parsed 45 entries from /var/log/auth.log
# ============================================
# Failed Password Attempts:
# 2024-03-23 14:32:10 - user: admin, source: 192.168.1.50
# 2024-03-23 14:32:45 - user: root, source: 203.0.113.45
# 2024-03-23 14:33:12 - user: admin, source: 192.168.1.50
```

**Use Cases:**
- Incident investigation
- Forensic analysis
- Log correlation
- Timeline reconstruction

**Time to Execute:** < 5 seconds (depends on file size)

---

### ioc_extractor - Indicator of Compromise Extraction

**Category:** Forensics

**Purpose:** Extract indicators of compromise (hashes, IPs, domains, etc.) from text.

**Parameters:**
- `text` (str, required): Text containing potential IOCs
- `ioc_types` (str, optional): Comma-separated types to extract
  - Default: "ip,hash,domain,email,url,file"
  - Supported: ip, hash, domain, email, url, file, registry, process

**Returns:** Extracted and deduplicated indicators with confidence scores

**Example:**

```python
response = ioc_extractor(
    text="Attack from 192.168.1.50. Malware hash: e5d8f1a9b2c3d4e5. Domain: evil.com",
    ioc_types="ip,hash,domain"
)
# Output:
# Extracted Indicators of Compromise
# ==================================
# IPs: 192.168.1.50 (confidence: 1.0)
# Hashes: e5d8f1a9b2c3d4e5 (type: MD5, confidence: 0.9)
# Domains: evil.com (confidence: 1.0)
```

**Use Cases:**
- Threat intelligence gathering
- Incident triage
- Malware analysis
- Detection rule creation

**Time to Execute:** < 500ms

---

## Analysis Tools

Tools for code and content analysis.

### secrets_scan - Credential and Secret Detection

**Category:** Analysis

**Purpose:** Scan code, configs, and logs for exposed secrets (API keys, passwords, tokens).

**Parameters:**
- `target` (str, required): File path, directory, or code snippet
- `patterns` (str, optional): Custom regex patterns for secret detection
  - Default: Uses built-in patterns for common secret types
- `entropy_threshold` (float, optional): Minimum entropy score (0-1)
  - Default: 0.7

**Returns:** Detected secrets with location and severity

**Example:**

```python
response = secrets_scan(
    target="/path/to/code",
    entropy_threshold=0.7
)
# Output:
# Secrets Scan Results
# ===================
# Found 3 secrets:
# 1. API Key (high confidence)
#    File: config.py, Line 42
#    Pattern: sk-[A-Za-z0-9]{48}
#    Risk: CRITICAL
#
# 2. AWS Access Key (high confidence)
#    File: .env, Line 15
#    Pattern: AKIA[0-9A-Z]{16}
#    Risk: CRITICAL
```

**Use Cases:**
- Code security scanning
- Configuration hardening
- Secret rotation auditing
- Compliance verification

**Time to Execute:** < 10 seconds (depends on target size)

---

## Reporting Tools

Tools for generating reports and scoring.

### report_builder - Report Generation

**Category:** Reporting

**Purpose:** Build formatted security reports from findings.

**Parameters:**
- `title` (str, required): Report title
- `findings` (str, required): Findings in JSON or structured format
- `format` (str, optional): Output format (html, pdf, markdown, json)
  - Default: "markdown"
- `include_executive_summary` (bool, optional): Add executive summary
  - Default: True

**Returns:** Formatted report as string (or file path if PDF)

**Example:**

```python
findings = """
{
  "vulnerabilities": [
    {"id": "CVE-2024-1234", "severity": "CRITICAL", "affected": "OpenSSL"}
  ],
  "misconfigurations": 12,
  "weak_credentials": 5
}
"""

response = report_builder(
    title="Security Assessment Report",
    findings=findings,
    format="markdown"
)
# Output: Full markdown report with formatting
```

**Use Cases:**
- Assessment report generation
- Executive reporting
- Compliance documentation
- Stakeholder communication

**Time to Execute:** < 2 seconds

---

### risk_scorer - Risk Scoring and Prioritization

**Category:** Reporting

**Purpose:** Score and prioritize findings based on risk metrics.

**Parameters:**
- `vulnerability` (str, required): Vulnerability description
- `cvss_score` (float, optional): CVSS v3.1 base score (0-10)
- `business_impact` (str, optional): Impact level (critical, high, medium, low)
- `exploitability` (str, optional): Exploitability (confirmed, probable, unproven)

**Returns:** Risk score (0-100) with prioritization recommendation

**Example:**

```python
response = risk_scorer(
    vulnerability="SQL Injection in login form",
    cvss_score=9.8,
    business_impact="critical",
    exploitability="confirmed"
)
# Output:
# Risk Score: 98/100 (CRITICAL)
# =============================
# Prioritization: IMMEDIATE (0-1 day)
# Rationale: High CVSS, confirmed exploitability, critical business impact
# Recommended Action: Emergency patching, WAF rules, monitoring
```

**Use Cases:**
- Vulnerability prioritization
- Resource allocation planning
- SLA determination
- Board reporting

**Time to Execute:** < 100ms

---

## Tools Summary Table

| Tool | Category | Input | Output | Exec Time |
|------|----------|-------|--------|-----------|
| dns_enum | Recon | Domain | DNS records | < 1s |
| port_scan | Recon | IP/CIDR | Open ports | 30-300s |
| whois_lookup | Recon | Domain | Registration info | < 2s |
| cve_lookup | Intel | CVE ID | Vulnerability details | < 1s |
| mitre_attack_map | Intel | Indicators | Techniques + tactics | < 500ms |
| log_parser | Forensics | Log file | Parsed entries | < 5s |
| ioc_extractor | Forensics | Text | IOCs + confidence | < 500ms |
| secrets_scan | Analysis | Code/files | Found secrets | < 10s |
| report_builder | Reporting | Findings | Formatted report | < 2s |
| risk_scorer | Reporting | Vulnerability | Risk score + action | < 100ms |

---

## Creating Custom Tools

### Step 1: Define Tool Function

```python
from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Analyze SSL certificate for security issues")
def ssl_analyzer(
    hostname: Annotated[str, Doc("Hostname or IP address to check")],
    port: Annotated[int, Doc("HTTPS port number")] = 443,
) -> str:
    """Analyze SSL certificate security."""
    import ssl

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return format_ssl_info(cert)
    except Exception as e:
        return f"Error analyzing SSL: {e}"
```

### Step 2: Place in Tools Package

```
packages/jaguarete-tools/src/jaguarete_tools/
├── recon/
├── intel/
├── forensics/
├── analysis/
└── reporting/
```

### Step 3: Register in Package

```python
# packages/jaguarete-tools/src/jaguarete_tools/__init__.py
from jaguarete_tools.analysis.ssl_analyzer import ssl_analyzer

__all__ = ["ssl_analyzer"]
```

### Step 4: Test Tool

```python
result = ssl_analyzer(hostname="example.com", port=443)
print(result)
```

---

## Tool Best Practices

1. **Clear Documentation:** Use Annotated types with Doc strings
2. **Error Handling:** Always catch and return meaningful errors
3. **Timeout Protection:** Set reasonable timeouts for network operations
4. **Input Validation:** Validate and sanitize all inputs
5. **Consistent Format:** Return structured, readable output
6. **Performance:** Optimize for typical use cases (seconds, not minutes)
7. **Security:** Never store credentials in code, use environment variables

---

## Troubleshooting Tools

### Tool Not Available to Agent

```python
# Verify tool registration
from jaguarete_tools import dns_enum, port_scan

# Test directly
result = dns_enum(domain="example.com")
print(result)
```

### Timeout Issues

```python
# Increase timeout in tool call
port_scan(target="192.168.1.0/24", timeout=5)  # 5 seconds per port
```

### Network Connectivity

```python
# Test basic connectivity
import socket
socket.getaddrinfo("example.com", 443)  # Should not raise exception
```

---

## References

- **MITRE ATT&CK:** Used by mitre_attack_map tool
- **CVSS Scoring:** Used by risk_scorer tool
- **NVD API:** Used by cve_lookup tool
- **Common Log Formats:** Supported by log_parser tool
