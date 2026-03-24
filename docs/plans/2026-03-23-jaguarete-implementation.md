# Jaguarete Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform DB-GPT v0.8.0 into Jaguarete, a minimalist AI-powered Purple Team security platform.

**Architecture:** Extract dbgpt-core's agent framework, RAG pipeline, and 3 LLM adapters (OpenAI, Claude, Ollama). Discard all other packages. Rebuild as jaguarete-* namespace with security-focused agents, tools, and knowledge bases. New simplified FastAPI app with JWT auth and dark-themed frontend.

**Tech Stack:** Python 3.10+, uv workspaces, FastAPI, pytest, Next.js 14, Ant Design, ChromaDB, JWT/bcrypt

---

## Phase F0: Rebrand & Strip

### Task 1: Create new branch and clean git history

**Files:**
- Modify: `.git/config` (via git commands)

**Step 1: Create the jaguarete branch**

```bash
git checkout -b jaguarete
```

**Step 2: Verify clean state**

```bash
git status
```

Expected: `On branch jaguarete, nothing to commit`

**Step 3: Commit checkpoint**

```bash
git commit --allow-empty -m "chore: begin Jaguarete transformation from DB-GPT v0.8.0"
```

---

### Task 2: Delete unnecessary packages

**Files:**
- Delete: `packages/dbgpt-serve/` (entire directory)
- Delete: `packages/dbgpt-client/` (entire directory)
- Delete: `packages/dbgpt-sandbox/` (entire directory)
- Delete: `packages/dbgpt-accelerator/` (entire directory)
- Delete: `packages/dbgpt-app/` (entire directory)
- Delete: `packages/dbgpt-ext/` (entire directory)

**Step 1: Remove the 6 unnecessary packages**

```bash
rm -rf packages/dbgpt-serve packages/dbgpt-client packages/dbgpt-sandbox packages/dbgpt-accelerator packages/dbgpt-app packages/dbgpt-ext
```

**Step 2: Verify only dbgpt-core remains**

```bash
ls packages/
```

Expected: only `dbgpt-core`

**Step 3: Commit**

```bash
git add -A && git commit -m "chore: remove unnecessary packages (serve, client, sandbox, accelerator, app, ext)"
```

---

### Task 3: Delete unnecessary root files and directories

**Files:**
- Delete: `README.hi.md`, `README.ja.md`, `README.ma.md`, `README.ta.md`, `README.zh.md`, `READMR.hi.md`
- Delete: `skills.py`, `skills/`
- Delete: `pilot/`
- Delete: `i18n/`
- Delete: `install_help.py`
- Delete: `MANIFEST.in`
- Delete: `.opencode/`
- Delete: `DB-GPT-Core-Code-Design-Analysis.md`
- Delete: `tests/` (root tests - will recreate for jaguarete)
- Delete: `examples/`
- Delete: `configs/`
- Delete: `scripts/`
- Delete: `assets/`
- Delete: `requirements/`
- Delete: `uv.lock`

**Step 1: Remove all unnecessary root files**

```bash
rm -f README.hi.md README.ja.md README.ma.md README.ta.md README.zh.md READMR.hi.md
rm -f skills.py install_help.py MANIFEST.in DB-GPT-Core-Code-Design-Analysis.md
rm -f uv.lock docker-compose.yml
rm -rf skills/ pilot/ i18n/ .opencode/ tests/ examples/ configs/ scripts/ assets/ requirements/
rm -rf .devcontainer/ .devcontainer.json
rm -rf docker/
rm -rf .github/
```

**Step 2: Verify remaining structure**

```bash
ls -la
```

Expected: `.git`, `.gitignore`, `docs/`, `packages/`, `pyproject.toml`, `web/`, `Makefile`, `README.md`, `LICENSE`, `CODE_OF_CONDUCT`, `CONTRIBUTING.md`, `DISCKAIMER.md`, linting configs

**Step 3: Commit**

```bash
git add -A && git commit -m "chore: remove unnecessary root files, docs, configs, and directories"
```

---

### Task 4: Strip dbgpt-core to essentials

Remove modules from dbgpt-core that are not needed:
- All generic agents in `expand/` (will be replaced by security agents)
- Chinese LLM providers (keep only chatgpt, claude, ollama)
- Visualization module
- Training module
- CLI module (will rebuild)
- Datasource module (not needed for v1)
- Experimental module

**Files:**
- Delete: `packages/dbgpt-core/src/dbgpt/agent/expand/` (all generic agents)
- Delete: `packages/dbgpt-core/src/dbgpt/agent/claude_skill/`
- Delete: `packages/dbgpt-core/src/dbgpt/vis/`
- Delete: `packages/dbgpt-core/src/dbgpt/train/`
- Delete: `packages/dbgpt-core/src/dbgpt/cli/`
- Delete: `packages/dbgpt-core/src/dbgpt/datasource/`
- Delete: `packages/dbgpt-core/src/dbgpt/experimental/`
- Delete: `packages/dbgpt-core/src/dbgpt/configs/`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/tongyi.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/wenxin.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/zhipu.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/deepseek.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/moonshot.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/minimax.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/spark.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/baichuan.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/volcengine.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/yi.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/llms/siliconflow.py`
- Delete: `packages/dbgpt-core/src/dbgpt/model/proxy/data_privacy/` (empty stubs)
- Delete: `packages/dbgpt-core/src/dbgpt/model/cluster/` (distributed model serving - not needed)

**Step 1: Remove unnecessary modules**

```bash
cd packages/dbgpt-core/src/dbgpt

# Remove generic agents and skills
rm -rf agent/expand/ agent/claude_skill/

# Remove unneeded modules
rm -rf vis/ train/ cli/ datasource/ experimental/ configs/

# Remove Chinese LLM providers (keep chatgpt.py, claude.py, ollama.py, proxy_model.py, __init__.py)
cd model/proxy/llms/
rm -f tongyi.py wenxin.py zhipu.py deepseek.py moonshot.py minimax.py spark.py baichuan.py volcengine.py yi.py siliconflow.py
cd ../../..

# Remove empty data privacy stubs and cluster
rm -rf model/proxy/data_privacy/
rm -rf model/cluster/
```

**Step 2: Verify kept LLM providers**

```bash
ls packages/dbgpt-core/src/dbgpt/model/proxy/llms/
```

Expected: `__init__.py`, `chatgpt.py`, `claude.py`, `ollama.py`, `proxy_model.py` (and possibly `gemini.py` - remove if present)

**Step 3: Commit**

```bash
git add -A && git commit -m "chore: strip dbgpt-core to essentials (agents core, RAG, 3 LLM providers)"
```

---

### Task 5: Rename dbgpt-core package to jaguarete-core

This is the most critical task. Rename the Python package namespace from `dbgpt` to `jaguarete`.

**Files:**
- Rename: `packages/dbgpt-core/` -> `packages/jaguarete-core/`
- Rename: `packages/dbgpt-core/src/dbgpt/` -> `packages/jaguarete-core/src/jaguarete/`
- Modify: `packages/jaguarete-core/pyproject.toml`
- Modify: All Python files (find-replace `dbgpt` -> `jaguarete` in imports)

**Step 1: Rename directories**

```bash
mv packages/dbgpt-core packages/jaguarete-core
mv packages/jaguarete-core/src/dbgpt packages/jaguarete-core/src/jaguarete
```

**Step 2: Update pyproject.toml of jaguarete-core**

Replace the content of `packages/jaguarete-core/pyproject.toml`:
- Change `name = "dbgpt"` to `name = "jaguarete-core"`
- Change all `dbgpt` references to `jaguarete`
- Remove extras for deleted providers (tongyi, wenxin, zhipu, etc.)
- Remove extras for deleted modules (cli, datasource, vis, train)
- Keep: `proxy_openai`, `proxy_anthropic`, `proxy_ollama`, `agent`, `rag`, `simple_framework`

**Step 3: Global find-replace imports in all Python files**

```bash
find packages/jaguarete-core -name "*.py" -exec sed -i 's/from dbgpt\./from jaguarete./g' {} +
find packages/jaguarete-core -name "*.py" -exec sed -i 's/import dbgpt\./import jaguarete./g' {} +
find packages/jaguarete-core -name "*.py" -exec sed -i 's/import dbgpt$/import jaguarete/g' {} +
find packages/jaguarete-core -name "*.py" -exec sed -i "s/\"dbgpt\./\"jaguarete./g" {} +
find packages/jaguarete-core -name "*.py" -exec sed -i "s/'dbgpt\./'jaguarete./g" {} +
find packages/jaguarete-core -name "*.py" -exec sed -i 's/dbgpt\.\([a-z]\)/jaguarete.\1/g' {} +
```

**Step 4: Verify no remaining dbgpt references in Python files (except comments/docs)**

```bash
grep -r "from dbgpt" packages/jaguarete-core/src/ --include="*.py" | head -20
grep -r "import dbgpt" packages/jaguarete-core/src/ --include="*.py" | head -20
```

Expected: No results (or only in docstrings/comments which are acceptable)

**Step 5: Commit**

```bash
git add -A && git commit -m "refactor: rename dbgpt namespace to jaguarete"
```

---

### Task 6: Create new root pyproject.toml

**Files:**
- Modify: `pyproject.toml` (root)

**Step 1: Rewrite root pyproject.toml**

```toml
[project]
name = "jaguarete"
version = "0.1.0"
description = "Jaguarete - AI-Powered Purple Team Platform"
authors = [
    { name = "skyvanguard" }
]
dependencies = []
readme = "README.md"
requires-python = ">= 3.10"
license = "MIT"

[tool.uv.workspace]
members = [
    "packages/jaguarete-core",
    "packages/jaguarete-agents",
    "packages/jaguarete-tools",
    "packages/jaguarete-knowledge",
    "packages/jaguarete-app",
]

[tool.uv]
managed = true
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest_asyncio",
    "ruff>=0.9.1",
    "pytest-mock>=3.14.0",
    "pytest-cov>=6.0.0",
    "mypy>=1.15.0",
    "pre-commit>=4.2.0",
]

[tool.pytest.ini_options]
pythonpath = ["packages"]
addopts = ["--import-mode=importlib"]
python_files = ["test_*.py", "*_test.py"]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.format]
docstring-code-format = true
quote-style = "double"
indent-style = "space"
line-ending = "auto"

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.ruff.lint.isort]
known-first-party = ["jaguarete", "jaguarete_agents", "jaguarete_tools", "jaguarete_knowledge", "jaguarete_app"]
```

**Step 2: Commit**

```bash
git add pyproject.toml && git commit -m "refactor: new root pyproject.toml for Jaguarete workspace"
```

---

### Task 7: Create new README.md

**Files:**
- Modify: `README.md`

**Step 1: Write new README**

```markdown
# Jaguarete

> AI-Powered Purple Team Platform

Jaguarete (Jaguar in Guaraní) is an AI-powered cybersecurity platform for Purple Teams.
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
```

**Step 2: Commit**

```bash
git add README.md && git commit -m "docs: new Jaguarete README"
```

---

### Task 8: Clean up linting configs and gitignore

**Files:**
- Modify: `.gitignore`
- Delete: `.flake8` (using ruff instead)
- Delete: `.isort.cfg` (using ruff instead)
- Delete: `.mypy.ini` (move to pyproject.toml)
- Delete: `.pre-commit-config.yaml` (recreate simpler version)
- Modify: `Makefile`

**Step 1: Clean up legacy lint configs**

```bash
rm -f .flake8 .isort.cfg .mypy.ini .pre-commit-config.yaml .python-version
```

**Step 2: Update .gitignore - add jaguarete-specific entries**

Append to existing `.gitignore`:

```
# Jaguarete
.env
*.db
knowledge_data/
reports/
```

**Step 3: Create minimal Makefile**

```makefile
.PHONY: help setup test fmt lint clean

help:
	@echo "Jaguarete - AI-Powered Purple Team Platform"
	@echo ""
	@echo "Commands:"
	@echo "  make setup    - Install dependencies"
	@echo "  make test     - Run tests"
	@echo "  make fmt      - Format code"
	@echo "  make lint     - Check code style"
	@echo "  make clean    - Clean build artifacts"

setup:
	uv sync

test:
	uv run pytest --pyargs jaguarete -v

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
```

**Step 4: Commit**

```bash
git add -A && git commit -m "chore: clean up configs, update gitignore and Makefile for Jaguarete"
```

---

### Task 9: Fix broken imports after stripping

After removing modules, some imports in jaguarete-core will be broken. This task fixes them.

**Files:**
- Modify: `packages/jaguarete-core/src/jaguarete/__init__.py`
- Modify: `packages/jaguarete-core/src/jaguarete/model/__init__.py`
- Modify: `packages/jaguarete-core/src/jaguarete/model/proxy/llms/__init__.py`
- Modify: Various files with imports to deleted modules

**Step 1: Fix root __init__.py**

The root `__init__.py` lazy-loads modules like `vis`, `train`, `cli`, `datasource` that were deleted.
Remove those lazy imports, keep only: `core`, `rag`, `model`, `agent`, `storage`.

**Step 2: Fix model __init__.py**

Remove references to deleted providers and cluster module.

**Step 3: Fix model/proxy/llms/__init__.py**

Remove imports of deleted providers (tongyi, wenxin, etc.).

**Step 4: Run a basic import test**

```bash
cd packages/jaguarete-core && uv run python -c "import jaguarete; print('OK')"
```

Expected: `OK` (no import errors)

**Step 5: Run existing tests that still apply**

```bash
uv run pytest packages/jaguarete-core/src/jaguarete/core/ -v --tb=short 2>&1 | head -50
```

Note: Some tests may fail due to missing fixtures - that's OK for now.

**Step 6: Commit**

```bash
git add -A && git commit -m "fix: repair broken imports after module stripping"
```

---

### Task 10: Verify F0 completion

**Step 1: Check project structure**

```bash
find packages/ -type f -name "*.py" | wc -l
```

Expected: Significantly fewer files than original (~300-400 vs 1172)

**Step 2: Check no dbgpt references in code**

```bash
grep -r "dbgpt" packages/ --include="*.py" -l | head -20
```

Expected: No results (or only in comments/docs)

**Step 3: Check directory structure matches design**

```bash
ls packages/
```

Expected: `jaguarete-core`

**Step 4: Commit tag**

```bash
git tag v0.0.1-f0-rebrand
```

---

## Phase F1: Core Engine Validation

### Task 11: Create jaguarete-core pyproject.toml

**Files:**
- Modify: `packages/jaguarete-core/pyproject.toml`

**Step 1: Write clean pyproject.toml for jaguarete-core**

```toml
[project]
name = "jaguarete-core"
version = "0.1.0"
description = "Jaguarete core engine: agents, RAG, and LLM adapters"
authors = [{ name = "skyvanguard" }]
requires-python = ">= 3.10"
dependencies = [
    "aiohttp>=3.8.0",
    "httpx>=0.24.0",
    "pydantic>=2.0.0",
    "SQLAlchemy>=2.0.25",
    "jinja2>=3.0.0",
    "cachetools",
]

[project.optional-dependencies]
openai = ["openai>=1.59.6", "tiktoken>=0.8.0"]
claude = ["anthropic"]
ollama = ["ollama"]
agent = ["termcolor", "mcp>=1.4.1"]
rag = ["chromadb>=0.4.0"]
all = ["jaguarete-core[openai,claude,ollama,agent,rag]"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/jaguarete"]
```

**Step 2: Commit**

```bash
git add packages/jaguarete-core/pyproject.toml && git commit -m "refactor: clean jaguarete-core pyproject.toml with minimal dependencies"
```

---

### Task 12: Write smoke test for core imports

**Files:**
- Create: `packages/jaguarete-core/tests/__init__.py`
- Create: `packages/jaguarete-core/tests/test_smoke.py`

**Step 1: Create test directory**

```bash
mkdir -p packages/jaguarete-core/tests
touch packages/jaguarete-core/tests/__init__.py
```

**Step 2: Write smoke test**

```python
"""Smoke tests to verify jaguarete-core imports work after rename."""


def test_import_jaguarete():
    """Core package imports without errors."""
    import jaguarete
    assert jaguarete is not None


def test_import_agent_core():
    """Agent framework core classes are importable."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete.agent.core.agent import Agent
    from jaguarete.agent.core.agent_manage import AgentManager
    assert ConversableAgent is not None
    assert Agent is not None
    assert AgentManager is not None


def test_import_agent_middleware():
    """Agent middleware system is importable."""
    from jaguarete.agent.middleware.base import AgentMiddleware
    assert AgentMiddleware is not None


def test_import_agent_resource():
    """Agent resource/tool system is importable."""
    from jaguarete.agent.resource.base import Resource, ResourceType
    from jaguarete.agent.resource.tool.base import tool
    assert Resource is not None
    assert ResourceType is not None
    assert tool is not None


def test_import_core_interfaces():
    """Core interfaces (LLM, embeddings, storage) are importable."""
    from jaguarete.core.interface.llm import LLMClient, ModelRequest, ModelOutput
    from jaguarete.core.interface.embeddings import Embeddings
    from jaguarete.core.interface.storage import StorageInterface
    assert LLMClient is not None
    assert ModelRequest is not None
    assert Embeddings is not None


def test_import_awel():
    """AWEL DAG system is importable."""
    from jaguarete.core.awel.dag.base import DAG
    from jaguarete.core.awel.operators.base import MapOperator
    assert DAG is not None
    assert MapOperator is not None


def test_import_rag():
    """RAG pipeline components are importable."""
    from jaguarete.rag.retriever.base import BaseRetriever
    from jaguarete.rag.text_splitter.text_splitter import (
        RecursiveCharacterTextSplitter,
    )
    assert BaseRetriever is not None
    assert RecursiveCharacterTextSplitter is not None


def test_import_storage():
    """Storage layer is importable."""
    from jaguarete.storage.vector_store.base import VectorStoreBase
    assert VectorStoreBase is not None


def test_import_llm_openai():
    """OpenAI LLM adapter is importable."""
    from jaguarete.model.proxy.llms.chatgpt import OpenAILLMClient
    assert OpenAILLMClient is not None


def test_import_llm_claude():
    """Claude LLM adapter is importable."""
    from jaguarete.model.proxy.llms.claude import ClaudeLLMClient
    assert ClaudeLLMClient is not None


def test_import_llm_ollama():
    """Ollama LLM adapter is importable."""
    from jaguarete.model.proxy.llms.ollama import OllamaLLMClient
    assert OllamaLLMClient is not None
```

**Step 3: Run smoke tests**

```bash
uv run pytest packages/jaguarete-core/tests/test_smoke.py -v
```

Expected: All 11 tests PASS. If any fail, fix the imports before proceeding.

**Step 4: Commit**

```bash
git add packages/jaguarete-core/tests/ && git commit -m "test: add smoke tests for jaguarete-core imports"
```

---

### Task 13: Install dependencies and validate full test suite

**Step 1: Sync workspace**

```bash
uv sync
```

**Step 2: Run full core test suite**

```bash
uv run pytest packages/jaguarete-core/ -v --tb=short 2>&1 | tail -30
```

**Step 3: Fix any failing tests, commit fixes**

```bash
git add -A && git commit -m "fix: resolve test failures after namespace rename"
```

**Step 4: Tag F1 milestone**

```bash
git tag v0.0.2-f1-core-validated
```

---

## Phase F2: Security Agents

### Task 14: Create jaguarete-agents package scaffold

**Files:**
- Create: `packages/jaguarete-agents/pyproject.toml`
- Create: `packages/jaguarete-agents/src/jaguarete_agents/__init__.py`
- Create: `packages/jaguarete-agents/src/jaguarete_agents/red/__init__.py`
- Create: `packages/jaguarete-agents/src/jaguarete_agents/blue/__init__.py`
- Create: `packages/jaguarete-agents/src/jaguarete_agents/purple/__init__.py`
- Create: `packages/jaguarete-agents/tests/__init__.py`

**Step 1: Create directory structure**

```bash
mkdir -p packages/jaguarete-agents/src/jaguarete_agents/{red,blue,purple}
mkdir -p packages/jaguarete-agents/tests
touch packages/jaguarete-agents/src/jaguarete_agents/__init__.py
touch packages/jaguarete-agents/src/jaguarete_agents/red/__init__.py
touch packages/jaguarete-agents/src/jaguarete_agents/blue/__init__.py
touch packages/jaguarete-agents/src/jaguarete_agents/purple/__init__.py
touch packages/jaguarete-agents/tests/__init__.py
```

**Step 2: Write pyproject.toml**

```toml
[project]
name = "jaguarete-agents"
version = "0.1.0"
description = "Jaguarete security agents for red, blue, and purple team operations"
authors = [{ name = "skyvanguard" }]
requires-python = ">= 3.10"
dependencies = [
    "jaguarete-core[agent]",
    "jaguarete-tools",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/jaguarete_agents"]
```

**Step 3: Commit**

```bash
git add packages/jaguarete-agents/ && git commit -m "feat: scaffold jaguarete-agents package"
```

---

### Task 15: Implement ReconAgent (Red Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/red/recon_agent.py`
- Create: `packages/jaguarete-agents/tests/test_recon_agent.py`

**Step 1: Write failing test**

```python
"""Tests for ReconAgent."""
import pytest
from unittest.mock import AsyncMock, MagicMock


def test_recon_agent_has_correct_profile():
    """ReconAgent has the correct role and goal."""
    from jaguarete_agents.red.recon_agent import ReconAgent

    agent = ReconAgent.__new__(ReconAgent)
    assert "Recon" in agent.profile.name
    assert agent.profile is not None


def test_recon_agent_extends_conversable():
    """ReconAgent inherits from ConversableAgent."""
    from jaguarete_agents.red.recon_agent import ReconAgent
    from jaguarete.agent.core.base_agent import ConversableAgent

    assert issubclass(ReconAgent, ConversableAgent)
```

**Step 2: Run test to verify it fails**

```bash
uv run pytest packages/jaguarete-agents/tests/test_recon_agent.py -v
```

Expected: FAIL (module not found)

**Step 3: Implement ReconAgent**

```python
"""ReconAgent - Passive and active reconnaissance for Red Team operations."""
from jaguarete.agent.core.base_agent import ConversableAgent
from jaguarete.agent.core.profile import DynConfig, ProfileConfig


class ReconAgent(ConversableAgent):
    """Agent specialized in reconnaissance operations.

    Performs passive and active recon on authorized targets including
    DNS enumeration, port scanning, service detection, and OSINT gathering.
    """

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig("ReconAgent", category="agent", key="jaguarete_recon_agent_name"),
        role=DynConfig(
            "Reconnaissance Specialist",
            category="agent",
            key="jaguarete_recon_agent_role",
        ),
        goal=DynConfig(
            "Perform thorough reconnaissance on authorized targets. Gather information "
            "about domains, subdomains, open ports, running services, and potential "
            "attack vectors. Always verify target authorization before scanning.",
            category="agent",
            key="jaguarete_recon_agent_goal",
        ),
        constraints=DynConfig(
            [
                "Only scan targets explicitly authorized by the user.",
                "Start with passive reconnaissance before active scanning.",
                "Document all findings with timestamps and sources.",
                "Flag high-severity findings immediately.",
                "Never perform destructive actions on targets.",
            ],
            category="agent",
            key="jaguarete_recon_agent_constraints",
        ),
    )

    def __init__(self, **kwargs):
        """Initialize ReconAgent."""
        super().__init__(**kwargs)
```

**Step 4: Run test to verify it passes**

```bash
uv run pytest packages/jaguarete-agents/tests/test_recon_agent.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add packages/jaguarete-agents/ && git commit -m "feat: implement ReconAgent for red team reconnaissance"
```

---

### Task 16: Implement VulnScannerAgent (Red Team)

Follow the same TDD pattern as Task 15.

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/red/vuln_scanner_agent.py`
- Create: `packages/jaguarete-agents/tests/test_vuln_scanner_agent.py`

Agent profile:
- Name: `VulnScannerAgent`
- Role: `Vulnerability Assessment Specialist`
- Goal: Detect known vulnerabilities in targets using CVE databases, dependency analysis, and service fingerprinting
- Constraints: Only scan authorized targets, prioritize by CVSS score, no exploitation

---

### Task 17: Implement ExploitAnalystAgent (Red Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/red/exploit_analyst_agent.py`
- Create: `packages/jaguarete-agents/tests/test_exploit_analyst_agent.py`

Agent profile:
- Name: `ExploitAnalystAgent`
- Role: `Exploit Analysis Specialist`
- Goal: Analyze known exploits, map to MITRE ATT&CK techniques, assess impact and likelihood
- Constraints: Analysis only (no active exploitation), map all findings to MITRE framework

---

### Task 18: Implement LogAnalystAgent (Blue Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/blue/log_analyst_agent.py`
- Create: `packages/jaguarete-agents/tests/test_log_analyst_agent.py`

Agent profile:
- Name: `LogAnalystAgent`
- Role: `Log Analysis and Anomaly Detection Specialist`
- Goal: Analyze system and application logs to detect anomalies, extract IOCs, and identify attack patterns
- Constraints: Read-only operations, never modify logs, correlate events across sources

---

### Task 19: Implement IncidentResponderAgent (Blue Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/blue/incident_responder_agent.py`
- Create: `packages/jaguarete-agents/tests/test_incident_responder_agent.py`

Agent profile:
- Name: `IncidentResponderAgent`
- Role: `Incident Response Coordinator`
- Goal: Guide step-by-step incident response using NIST SP 800-61 framework
- Constraints: Follow established IR procedures, preserve evidence chain of custody

---

### Task 20: Implement ThreatHunterAgent (Blue Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/blue/threat_hunter_agent.py`
- Create: `packages/jaguarete-agents/tests/test_threat_hunter_agent.py`

Agent profile:
- Name: `ThreatHunterAgent`
- Role: `Proactive Threat Hunter`
- Goal: Proactively search for hidden threats using hypothesis-driven hunting methodology
- Constraints: Document all hypotheses and findings, use Sigma rules for detection logic

---

### Task 21: Implement AttackSurfaceAgent (Purple Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/purple/attack_surface_agent.py`
- Create: `packages/jaguarete-agents/tests/test_attack_surface_agent.py`

Agent profile:
- Name: `AttackSurfaceAgent`
- Role: `Attack Surface Mapping Coordinator`
- Goal: Coordinate red team agents to build complete attack surface maps with risk scores
- Constraints: Aggregate findings from all agents, deduplicate, score by risk

---

### Task 22: Implement ReportGeneratorAgent (Purple Team)

**Files:**
- Create: `packages/jaguarete-agents/src/jaguarete_agents/purple/report_generator_agent.py`
- Create: `packages/jaguarete-agents/tests/test_report_generator_agent.py`

Agent profile:
- Name: `ReportGeneratorAgent`
- Role: `Security Report Generator`
- Goal: Generate executive and technical security reports from agent findings
- Constraints: Two report modes (executive summary, technical detail), include remediation recommendations

---

### Task 23: Tag F2 milestone

```bash
uv run pytest packages/jaguarete-agents/tests/ -v
git tag v0.0.3-f2-agents
```

---

## Phase F3: Security Tools

### Task 24: Create jaguarete-tools package scaffold

**Files:**
- Create: `packages/jaguarete-tools/pyproject.toml`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/__init__.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/recon/__init__.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/analysis/__init__.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/intel/__init__.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/forensics/__init__.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/reporting/__init__.py`

Dependencies: `jaguarete-core[agent]`

**Commit:** `feat: scaffold jaguarete-tools package`

---

### Task 25: Implement recon tools

**Files:**
- Create: `packages/jaguarete-tools/src/jaguarete_tools/recon/dns_enum.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/recon/port_scan.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/recon/whois_lookup.py`
- Create: `packages/jaguarete-tools/tests/test_recon_tools.py`

Each tool uses the `@tool` decorator from `jaguarete.agent.resource.tool.base`:

```python
from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc

@tool(description="Perform DNS enumeration on a target domain")
async def dns_enum(
    domain: Annotated[str, Doc("Target domain to enumerate")],
    record_types: Annotated[str, Doc("Comma-separated DNS record types")] = "A,AAAA,MX,NS,TXT,CNAME",
) -> str:
    """Enumerate DNS records for a target domain."""
    import asyncio
    import socket
    # Implementation using socket.getaddrinfo and dns.resolver
    ...
```

**Commit:** `feat: implement recon tools (dns_enum, port_scan, whois_lookup)`

---

### Task 26: Implement intel tools

**Files:**
- Create: `packages/jaguarete-tools/src/jaguarete_tools/intel/cve_lookup.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/intel/mitre_attack.py`
- Create: `packages/jaguarete-tools/tests/test_intel_tools.py`

Tools:
- `cve_lookup`: Query NVD API for CVE details
- `mitre_attack_map`: Map findings to MITRE ATT&CK techniques

**Commit:** `feat: implement intel tools (cve_lookup, mitre_attack_map)`

---

### Task 27: Implement forensics tools

**Files:**
- Create: `packages/jaguarete-tools/src/jaguarete_tools/forensics/log_parser.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/forensics/ioc_extractor.py`
- Create: `packages/jaguarete-tools/tests/test_forensics_tools.py`

Tools:
- `log_parser`: Parse common log formats (syslog, Apache, nginx, Windows Event Log)
- `ioc_extractor`: Extract IPs, domains, hashes, URLs from text

**Commit:** `feat: implement forensics tools (log_parser, ioc_extractor)`

---

### Task 28: Implement reporting tools

**Files:**
- Create: `packages/jaguarete-tools/src/jaguarete_tools/reporting/report_builder.py`
- Create: `packages/jaguarete-tools/src/jaguarete_tools/reporting/risk_scorer.py`
- Create: `packages/jaguarete-tools/tests/test_reporting_tools.py`

Tools:
- `report_builder`: Generate markdown security reports
- `risk_scorer`: Calculate CVSS-based risk scores

**Commit:** `feat: implement reporting tools (report_builder, risk_scorer)`

---

### Task 29: Tag F3 milestone

```bash
uv run pytest packages/jaguarete-tools/tests/ -v
git tag v0.0.4-f3-tools
```

---

## Phase F4: Knowledge Base

### Task 30: Create jaguarete-knowledge package scaffold

**Files:**
- Create: `packages/jaguarete-knowledge/pyproject.toml`
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/__init__.py`
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/sources/__init__.py`
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/feeds/__init__.py`

Dependencies: `jaguarete-core[rag]`, `httpx`

**Commit:** `feat: scaffold jaguarete-knowledge package`

---

### Task 31: Implement MITRE ATT&CK knowledge source

**Files:**
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/sources/mitre_attack.py`
- Create: `packages/jaguarete-knowledge/tests/test_mitre_source.py`

Loads MITRE ATT&CK STIX data, chunks by technique, embeds for RAG retrieval.

**Commit:** `feat: implement MITRE ATT&CK knowledge source`

---

### Task 32: Implement CVE/NVD knowledge source

**Files:**
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/sources/nvd_cve.py`
- Create: `packages/jaguarete-knowledge/tests/test_nvd_source.py`

Fetches from NVD API, chunks by CVE entry, includes CVSS scores in metadata.

**Commit:** `feat: implement NVD/CVE knowledge source`

---

### Task 33: Implement OWASP knowledge source

**Files:**
- Create: `packages/jaguarete-knowledge/src/jaguarete_knowledge/sources/owasp.py`
- Create: `packages/jaguarete-knowledge/tests/test_owasp_source.py`

Loads OWASP Top 10 and testing guide, chunks by category.

**Commit:** `feat: implement OWASP knowledge source`

---

### Task 34: Tag F4 milestone

```bash
uv run pytest packages/jaguarete-knowledge/tests/ -v
git tag v0.0.5-f4-knowledge
```

---

## Phase F5: Auth & App Server

### Task 35: Create jaguarete-app package scaffold

**Files:**
- Create: `packages/jaguarete-app/pyproject.toml`
- Create: `packages/jaguarete-app/src/jaguarete_app/__init__.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/api/__init__.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/auth/__init__.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/config.py`

Dependencies: `jaguarete-core[all]`, `jaguarete-agents`, `jaguarete-tools`, `jaguarete-knowledge`, `fastapi`, `uvicorn`, `python-jose[cryptography]`, `passlib[bcrypt]`

**Commit:** `feat: scaffold jaguarete-app package`

---

### Task 36: Implement JWT authentication

**Files:**
- Create: `packages/jaguarete-app/src/jaguarete_app/auth/jwt.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/auth/models.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/auth/dependencies.py`
- Create: `packages/jaguarete-app/tests/test_auth.py`

Implement:
- `create_access_token(data, expires)` -> JWT token
- `create_refresh_token(data)` -> refresh token
- `verify_token(token)` -> payload
- `get_current_user` FastAPI dependency
- User model with roles: admin, analyst, viewer
- Scopes: red_team, blue_team, knowledge, reports

**Commit:** `feat: implement JWT authentication with RBAC`

---

### Task 37: Implement FastAPI server

**Files:**
- Create: `packages/jaguarete-app/src/jaguarete_app/main.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/api/agents.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/api/chat.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/api/knowledge.py`
- Create: `packages/jaguarete-app/src/jaguarete_app/api/auth_routes.py`
- Create: `packages/jaguarete-app/tests/test_api.py`

Endpoints:
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/agents` - List available agents
- `POST /api/chat` - Chat with an agent (SSE streaming)
- `GET /api/knowledge` - List knowledge bases
- `POST /api/knowledge/query` - RAG query

**Commit:** `feat: implement FastAPI server with auth and agent endpoints`

---

### Task 38: Tag F5 milestone

```bash
uv run pytest packages/jaguarete-app/tests/ -v
git tag v0.0.6-f5-app
```

---

## Phase F6: Frontend

### Task 39: Strip and rebrand web frontend

**Files:**
- Modify: `web/package.json` (rename, update deps)
- Delete unnecessary pages (playground, evaluation, models_evaluation)
- Modify: theme to dark mode
- Modify: i18n to en/es only

This is a large task - break down further during execution.

**Commit:** `refactor: strip and rebrand frontend for Jaguarete`

---

### Task 40: Implement security dashboard

**Files:**
- Create: `web/pages/dashboard.tsx`
- Modify: `web/pages/chat/` (security-focused chat UI)
- Create: `web/components/SecurityMetrics.tsx`
- Create: `web/components/AgentStatus.tsx`

**Commit:** `feat: implement security dashboard frontend`

---

## Phase F7: Docker & Docs

### Task 41: Create Docker setup

**Files:**
- Create: `docker/Dockerfile`
- Create: `docker-compose.yml`
- Create: `.env.example`

**Commit:** `feat: add Docker setup for Jaguarete`

---

### Task 42: Write documentation

**Files:**
- Modify: `CONTRIBUTING.md` (update for Jaguarete)
- Create: `docs/getting-started.md`
- Create: `docs/agents.md`
- Create: `docs/tools.md`
- Create: `docs/knowledge-bases.md`

**Commit:** `docs: add Jaguarete documentation`

---

### Task 43: Create GitHub Actions CI

**Files:**
- Create: `.github/workflows/ci.yml`

Jobs: lint, test (Python 3.10, 3.11), build

**Commit:** `ci: add GitHub Actions workflow`

---

### Task 44: Final tag

```bash
git tag v0.1.0
```

---

## Execution Notes

- **F0 (Tasks 1-10)** is the most critical and risky phase - many imports will break
- **F1 (Tasks 11-13)** validates the core engine works after stripping
- **F2-F4 (Tasks 14-34)** are the value-add - security agents, tools, knowledge
- **F5-F7 (Tasks 35-43)** make it a complete deployable product
- Each task should be executed with TDD where applicable
- Commit after every task
- Tag after every phase milestone
