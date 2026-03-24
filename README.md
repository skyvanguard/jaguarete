<h1 align="center">Jaguarete</h1>

<p align="center">
  <strong>AI-Powered Purple Team Platform</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#agents">Agents</a> &bull;
  <a href="#tools">Tools</a> &bull;
  <a href="#knowledge-bases">Knowledge</a> &bull;
  <a href="docs/jaguarete/getting-started.md">Docs</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/tests-88%20passing-brightgreen" alt="Tests" />
  <img src="https://img.shields.io/badge/version-0.1.0-orange" alt="v0.1.0" />
</p>

---

**Jaguarete** (Jaguar in Guarani) is a cybersecurity platform that uses AI agents to automate Purple Team operations. It combines offensive testing (Red Team), defensive analysis (Blue Team), and coordinated reporting (Purple Team) into a single platform with RAG-powered knowledge bases.

## Quick Start

```bash
git clone https://github.com/skyvanguard/jaguarete.git
cd jaguarete

uv sync                    # Install dependencies
cp .env.example .env       # Configure API keys

# Backend
uv run uvicorn jaguarete_app.main:app --reload

# Frontend (separate terminal)
cd web && npm install && npm run dev
```

Or with Docker:

```bash
docker compose up
```

Open http://localhost:3000 &mdash; default login: `admin` / `admin`

## Agents

Eight specialized security agents organized by team:

| Team | Agent | Role |
|------|-------|------|
| **Red** | `ReconAgent` | Passive & active reconnaissance |
| **Red** | `VulnScannerAgent` | Vulnerability assessment & CVE mapping |
| **Red** | `ExploitAnalystAgent` | Exploit analysis & impact evaluation |
| **Blue** | `LogAnalystAgent` | Log analysis & anomaly detection |
| **Blue** | `IncidentResponderAgent` | Incident response coordination (NIST) |
| **Blue** | `ThreatHunterAgent` | Proactive threat hunting & IOC analysis |
| **Purple** | `AttackSurfaceAgent` | Attack surface mapping & risk scoring |
| **Purple** | `ReportGeneratorAgent` | Executive & technical report generation |

## Tools

Ten security tools available to agents via the `@tool` decorator:

| Category | Tool | Description |
|----------|------|-------------|
| Recon | `dns_enum` | DNS record enumeration |
| Recon | `port_scan` | TCP port scanning (21 common ports) |
| Recon | `whois_lookup` | WHOIS domain information |
| Intel | `cve_lookup` | NVD API vulnerability search |
| Intel | `mitre_attack_map` | MITRE ATT&CK technique mapping |
| Forensics | `log_parser` | Multi-format log analysis |
| Forensics | `ioc_extractor` | IOC extraction (IPs, hashes, domains, CVEs) |
| Analysis | `secrets_scan` | Credential & secret detection |
| Reporting | `report_builder` | Markdown report generation |
| Reporting | `risk_scorer` | CVSS v3.1-based risk scoring |

## Knowledge Bases

RAG-integrated security knowledge sources:

| Source | Content | Records |
|--------|---------|---------|
| **MITRE ATT&CK** | Adversary tactics, techniques & mitigations | 15+ techniques |
| **NVD CVE** | Known vulnerabilities with CVSS scores | NVD API integration |
| **OWASP Top 10** | Web application security risks (2021) | 10 categories |

## Architecture

```
jaguarete/
├── packages/
│   ├── jaguarete-core/       # Agent engine, RAG pipeline, LLM adapters
│   ├── jaguarete-agents/     # 8 security agents (red/blue/purple)
│   ├── jaguarete-tools/      # 10 security tools
│   ├── jaguarete-knowledge/  # MITRE, NVD, OWASP knowledge sources
│   └── jaguarete-app/        # FastAPI server + JWT auth
├── web/                      # Next.js security dashboard
├── docker/                   # Dockerfiles
└── docs/                     # Documentation
```

## API

All endpoints require JWT authentication. Roles: `admin`, `analyst`, `viewer`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Authenticate & get tokens |
| `POST` | `/api/auth/refresh` | Refresh access token |
| `GET` | `/api/agents` | List available agents (filtered by scope) |
| `POST` | `/api/chat` | Chat with agent (SSE streaming) |
| `GET` | `/api/knowledge` | List knowledge bases |
| `POST` | `/api/knowledge/query` | RAG query |
| `GET` | `/api/health` | Health check |

## LLM Providers

| Provider | Type | Use Case |
|----------|------|----------|
| **OpenAI** | Cloud | GPT-4o for complex analysis |
| **Claude** | Cloud | Advanced reasoning & reports |
| **Ollama** | Local | Privacy-first, offline operation |

## Development

```bash
make setup    # Install dependencies
make test     # Run tests (88 passing)
make fmt      # Format code (ruff)
make lint     # Check code style
make clean    # Clean build artifacts
```

## License

[MIT](LICENSE)

---

<p align="center">
  Built by <a href="https://github.com/skyvanguard">@skyvanguard</a> &mdash; Cybersecurity & AI Researcher, Paraguay
</p>
