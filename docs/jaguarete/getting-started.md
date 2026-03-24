# Getting Started with Jaguarete

Welcome to Jaguarete, the AI-Powered Purple Team Platform! This guide will walk you through installation and running your first operations.

## Prerequisites

Before starting, ensure you have:
- **Python 3.10+** (3.11 recommended)
- **Node.js 20+** (for the web dashboard)
- **Git**
- **uv** (Python package manager) - [install uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/skyvanguard/jaguarete.git
cd jaguarete
```

### 2. Install Dependencies

```bash
# Install Python packages via uv
uv sync

# Install Node.js dependencies for the web dashboard
cd web
npm install
cd ..
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your configuration. Key variables:

```bash
# LLM Provider (openai, anthropic, ollama)
JAGUARETE_LLM_PROVIDER=openai

# API Keys (choose based on provider)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# For Ollama (local models)
OLLAMA_BASE_URL=http://localhost:11434

# Security
JAGUARETE_SECRET_KEY=your-secure-random-key

# CORS (for local dev)
JAGUARETE_CORS_ORIGINS=http://localhost:3000

# Database
DATABASE_URL=sqlite:///jaguarete.db
```

## Running the Application

### Option 1: Standard Setup (Separate Terminals)

**Terminal 1 - Backend API Server:**

```bash
uv run uvicorn jaguarete_app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API docs: `http://localhost:8000/docs`

**Terminal 2 - Frontend Dashboard:**

```bash
cd web
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Option 2: Docker Compose (Recommended)

```bash
docker compose up -d
```

This starts:
- FastAPI backend on port 8000
- Next.js frontend on port 3000
- SQLite database (persisted)

### Option 3: Make Command

```bash
# Start backend
make run-backend

# Start frontend (in another terminal)
make run-frontend

# Stop everything
make stop
```

## First Login

### Default Credentials

**Username:** `admin`
**Password:** `admin`

**WARNING:** Change these credentials immediately in production!

### Access the Dashboard

1. Open `http://localhost:3000` in your browser
2. Log in with default credentials
3. Navigate to "Agents" to see available Red/Blue/Purple team agents
4. Start your first security operation

## LLM Provider Setup

### OpenAI (GPT-4o)

```bash
JAGUARETE_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

Ideal for: Complex vulnerability analysis, detailed reporting

### Anthropic (Claude)

```bash
JAGUARETE_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

Ideal for: Reasoning-heavy tasks, long-form reports

### Ollama (Local/Offline)

```bash
JAGUARETE_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

Prerequisites:
1. [Install Ollama](https://ollama.ai)
2. Pull a model: `ollama pull mistral`
3. Run Ollama: `ollama serve`

Ideal for: Privacy-first operations, offline capability, cost control

## Verifying Installation

### Check Backend Health

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "operational",
  "service": "Jaguarete",
  "version": "0.0.1"
}
```

### Check Available Agents

```bash
curl http://localhost:8000/api/agents/list
```

## Next Steps

- **[Agents Guide](./agents.md)** - Learn about Red, Blue, and Purple team agents
- **[Tools Reference](./tools.md)** - Available security tools and their usage
- **[Knowledge Bases](./knowledge-bases.md)** - MITRE ATT&CK, CVE, OWASP integration
- **[Docker Deployment](./docker.md)** - Advanced Docker setup and scaling

## Troubleshooting

### Port Already in Use

If port 8000 or 3000 is in use:

```bash
# Backend on custom port
uv run uvicorn jaguarete_app.main:app --port 8001

# Frontend on custom port
cd web && npm run dev -- -p 3001
```

### Missing Dependencies

```bash
# Reinstall all dependencies
uv sync --upgrade
cd web && npm install
```

### LLM Connection Error

- Verify your API key is set correctly
- For OpenAI/Anthropic: Test `curl https://api.openai.com/v1/models` (with auth header)
- For Ollama: Verify `curl http://localhost:11434/api/tags`

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm jaguarete.db
uv run python -c "from jaguarete_app import db; db.init_db()"
```

## Docker Quick Reference

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild images
docker compose up --build

# Access database shell
docker compose exec db sqlite3 /data/jaguarete.db
```

## Security Notes

- **Never commit `.env` files** - Add to `.gitignore`
- **Change default credentials** before any external access
- **Use strong JWT secret** in production (minimum 32 characters)
- **Enable HTTPS** in production (use reverse proxy like Nginx)
- **Rotate API keys** regularly
- **Limit CORS origins** to known domains

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/skyvanguard/jaguarete/issues)
- **Discussions:** [GitHub Discussions](https://github.com/skyvanguard/jaguarete/discussions)
- **Documentation:** [Full Docs](https://jaguarete.dev/docs)

Happy hunting!
