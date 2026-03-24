"""Knowledge base routes."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from jaguarete_app.auth.dependencies import get_current_user, require_scope
from jaguarete_app.auth.models import Scope, TokenData

router = APIRouter()

KNOWLEDGE_BASES = [
    {
        "id": "mitre_attack",
        "name": "MITRE ATT&CK",
        "description": "Adversary tactics, techniques, and procedures",
        "documents": 15,
    },
    {
        "id": "nvd_cve",
        "name": "NVD CVE Database",
        "description": "Known vulnerabilities and exposures",
        "documents": 5,
    },
    {
        "id": "owasp_top10",
        "name": "OWASP Top 10",
        "description": "Top web application security risks",
        "documents": 10,
    },
]


class KnowledgeQuery(BaseModel):
    """Knowledge query request."""
    query: str
    source: str | None = None
    limit: int = 5


@router.get("")
async def list_knowledge_bases(
    user: TokenData = Depends(require_scope(Scope.KNOWLEDGE)),
):
    """List available knowledge bases."""
    return {"knowledge_bases": KNOWLEDGE_BASES}


@router.post("/query")
async def query_knowledge(
    request: KnowledgeQuery,
    user: TokenData = Depends(require_scope(Scope.KNOWLEDGE)),
):
    """Query security knowledge bases."""
    # Placeholder - will integrate with actual RAG pipeline
    return {
        "query": request.query,
        "source": request.source or "all",
        "results": [
            {
                "source": "mitre_attack",
                "content": f"Placeholder result for: {request.query}",
                "relevance": 0.95,
            }
        ],
    }
