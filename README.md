# Jaguarete

> AI-Powered Purple Team Platform

Jaguarete (Jaguar in Guarani) is an AI-powered cybersecurity platform for Purple Teams.
It provides specialized AI agents for offensive security (Red Team), defensive security
(Blue Team), and coordinated operations (Purple Team).

Built on a powerful agent framework with RAG capabilities, Jaguarete helps security
professionals automate reconnaissance, vulnerability analysis, log investigation,
incident response, and threat hunting.

## Features

- **Red Team Agents**: Automated recon, vulnerability scanning, exploit analysis
- **Blue Team Agents**: Log analysis, incident response, threat hunting
- **Purple Team Coordination**: Attack surface mapping, report generation
- **Security Knowledge Base**: RAG over MITRE ATT&CK, CVE/NVD, OWASP, Sigma Rules
- **Multi-LLM Support**: OpenAI, Claude, Ollama (local)
- **JWT Authentication**: Role-based access control (admin, analyst, viewer)

## Quick Start

```bash
# Clone
git clone https://github.com/skyvanguard/jaguarete.git
cd jaguarete

# Install
uv sync

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
uv run jaguarete start
```

## Architecture

```
jaguarete/
├── packages/
│   ├── jaguarete-core/      # Agent engine, RAG, LLM adapters
│   ├── jaguarete-agents/    # Security agents (red/blue/purple)
│   ├── jaguarete-tools/     # Security tools
│   ├── jaguarete-knowledge/ # CVE, MITRE, OWASP knowledge bases
│   └── jaguarete-app/       # FastAPI server
└── web/                     # Security dashboard (Next.js)
```

## LLM Providers

| Provider | Type | Use Case |
|----------|------|----------|
| OpenAI | Cloud | GPT-4o for complex analysis |
| Claude | Cloud | Premium reasoning and reports |
| Ollama | Local | Privacy-first, offline operation |

## License

MIT

## Author

[@skyvanguard](https://github.com/skyvanguard) - Cybersecurity & AI Researcher, Paraguay
