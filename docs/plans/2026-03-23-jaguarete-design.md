# Jaguarete - AI-Powered Purple Team Platform

**Date:** 2026-03-23
**Author:** skyvanguard
**Status:** Approved

## Overview

Jaguarete (Jaguar in Guarani) is a minimalist fork of DB-GPT v0.8.0, rebuilt as an
AI-powered cybersecurity platform for Purple Teams. It extracts the core agent framework
and RAG pipeline from DB-GPT, discards everything else, and builds a security-focused
platform on top.

**Audience:** Pentesters, SOC analysts, and security researchers (Purple Team).
**Approach:** Gutting & Rebuilding - extract the engine, discard the rest, new identity.

## Architecture

### Monorepo Structure

```
jaguarete/
├── pyproject.toml                 # uv workspace root
├── packages/
│   ├── jaguarete-core/            # Engine: agents, RAG, LLM adapters
│   │   └── src/jaguarete/
│   │       ├── agent/             # Agent framework (fork of dbgpt.agent)
│   │       │   ├── core/          # base_agent, agent_manage, middleware
│   │       │   ├── resource/      # tool system, resource manager
│   │       │   └── memory/        # agent memory
│   │       ├── rag/               # RAG pipeline (fork of dbgpt.rag)
│   │       ├── model/             # LLM adapters (OpenAI, Ollama, Claude only)
│   │       ├── storage/           # Vector stores, graph stores
│   │       └── core/              # AWEL operators base, interfaces, schema
│   │
│   ├── jaguarete-agents/          # Security agents
│   │   └── src/jaguarete_agents/
│   │       ├── red/               # Offensive agents
│   │       │   ├── recon_agent.py
│   │       │   ├── vuln_scanner_agent.py
│   │       │   └── exploit_analyst_agent.py
│   │       ├── blue/              # Defensive agents
│   │       │   ├── log_analyst_agent.py
│   │       │   ├── incident_responder_agent.py
│   │       │   └── threat_hunter_agent.py
│   │       └── purple/            # Coordinator agents
│   │           ├── attack_surface_agent.py
│   │           └── report_generator_agent.py
│   │
│   ├── jaguarete-tools/           # Security tools
│   │   └── src/jaguarete_tools/
│   │       ├── recon/             # nmap, whois, dns, subdomain enum
│   │       ├── analysis/          # SAST, dependency audit, secrets scan
│   │       ├── intel/             # CVE lookup, MITRE mapping, threat feeds
│   │       ├── forensics/         # log parsing, IOC extraction
│   │       └── reporting/         # PDF/markdown report generation
│   │
│   ├── jaguarete-knowledge/       # Security knowledge bases
│   │   └── src/jaguarete_knowledge/
│   │       ├── sources/           # Loaders for CVE, NVD, MITRE ATT&CK
│   │       ├── embeddings/        # Security-specific chunking strategies
│   │       └── feeds/             # Auto-update threat intelligence
│   │
│   └── jaguarete-app/             # Simplified FastAPI server
│       └── src/jaguarete_app/
│           ├── api/               # REST endpoints
│           ├── auth/              # JWT auth + RBAC
│           └── config.py
│
├── web/                           # Frontend (Next.js, dark theme, security UI)
├── docker/                        # Docker setup
├── docs/                          # Documentation (en/es)
└── tests/                         # Tests
```

### What is extracted from DB-GPT

**Kept (forked + renamed):**
- `dbgpt.agent.core` -> `jaguarete.agent.core` (agent framework, middleware system)
- `dbgpt.agent.resource` -> `jaguarete.agent.resource` (tool system, resource manager)
- `dbgpt.rag` -> `jaguarete.rag` (RAG pipeline, chunking, retrieval)
- `dbgpt.model.proxy.llms.chatgpt` -> OpenAI adapter
- `dbgpt.model.proxy.llms.claude` -> Claude adapter
- `dbgpt.model.proxy.llms.ollama` -> Ollama adapter
- `dbgpt.storage.vector_store` -> Vector store base + Chroma
- `dbgpt.core` -> AWEL operators base, interfaces

**Discarded:**
- 15+ Chinese LLM providers (tongyi, wenxin, zhipu, baichuan, etc.)
- `dbgpt-serve` (replaced by simplified jaguarete-app)
- `dbgpt-client` (rebuilt as simple SDK)
- `dbgpt-sandbox` (evaluate later)
- `dbgpt-accelerator` (not needed)
- All generic agents in `dbgpt.agent.expand/`
- AWEL visual editor
- Model evaluation/playground
- Documentation in Chinese
- Multi-language i18n (keep only en/es)

## Security Agents

### Red Team Agents

| Agent | Function | Tools |
|-------|----------|-------|
| `ReconAgent` | Passive/active reconnaissance | nmap, whois, dns_enum, subfinder, shodan_lookup |
| `VulnScannerAgent` | Known vulnerability detection | cve_lookup, dependency_audit, port_scan, banner_grab |
| `ExploitAnalystAgent` | Exploit analysis and attack vectors | exploit_db_search, mitre_attack_map, payload_analyzer |

### Blue Team Agents

| Agent | Function | Tools |
|-------|----------|-------|
| `LogAnalystAgent` | Log anomaly detection and IOC extraction | log_parser, ioc_extractor, sigma_rule_matcher |
| `IncidentResponderAgent` | Step-by-step incident response guidance | containment_advisor, timeline_builder, evidence_collector |
| `ThreatHunterAgent` | Proactive threat hunting | yara_scanner, osint_search, threat_feed_query |

### Purple Team Agents

| Agent | Function | Tools |
|-------|----------|-------|
| `AttackSurfaceAgent` | Complete attack surface mapping | Coordinates ReconAgent + VulnScanner |
| `ReportGeneratorAgent` | Executive and technical report generation | report_builder, risk_scorer, remediation_advisor |

### Agent Design Patterns

- All agents extend `ConversableAgent` with middleware for:
  - **Audit logging**: Every agent action is recorded
  - **Scope control**: Red team agents only operate on authorized targets
  - **Chain of custody**: Digitally signed evidence

## RAG Security Knowledge

Knowledge bases fed from:
- **MITRE ATT&CK**: Tactics, techniques and procedures
- **NVD/CVE**: Known vulnerabilities (weekly auto-update)
- **OWASP**: Top 10, checklists, guides
- **CWE**: Weakness classification
- **Sigma Rules**: Detection rules

Agents query these bases via RAG before making decisions.

## Platform Security

### Auth & RBAC

- JWT authentication with bcrypt password hashing
- Refresh token rotation
- Roles: `admin`, `analyst`, `viewer`
- Scopes: `red_team`, `blue_team`, `knowledge`, `reports`
- API keys for external integrations
- Full audit log of all actions
- Rate limiting per user

### Frontend

- Dark theme native (security aesthetic)
- Dashboard: Security metrics, active agents, alerts
- Chat: Conversation interface with agents
- Knowledge: Security knowledge base management
- Reports: Report visualization and export
- Languages: English + Spanish only

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.10+, FastAPI, uv workspaces |
| Agents | jaguarete-core (fork of dbgpt agent framework) |
| RAG | jaguarete-core (fork of dbgpt rag) |
| LLM | OpenAI, Claude, Ollama |
| Vector Store | ChromaDB (default), pgvector (production) |
| Auth | JWT + bcrypt |
| Frontend | Next.js 14, Ant Design, dark theme |
| Database | SQLite (dev), PostgreSQL (prod) |
| Container | Docker + docker-compose |

## Development Phases

| Phase | Description |
|-------|-------------|
| **F0: Rebrand & Strip** | Rename all references, remove unnecessary packages, clean imports, new README, new pyproject.toml |
| **F1: Core Engine** | Ensure agent engine and RAG pipeline work standalone with 3 LLM providers |
| **F2: Security Agents** | Implement 8 agents with their tools |
| **F3: Knowledge Base** | MITRE, CVE, OWASP loaders + auto-update pipeline |
| **F4: Auth & Hardening** | JWT, RBAC, audit logging, input validation |
| **F5: Frontend** | Security dashboard with dark theme |
| **F6: Docker & Docs** | Docker-compose ready, documentation in en/es |
