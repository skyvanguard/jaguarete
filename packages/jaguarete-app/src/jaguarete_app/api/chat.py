"""Chat routes with SSE streaming."""

import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from jaguarete_app.auth.dependencies import get_current_user
from jaguarete_app.auth.models import TokenData

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request body."""
    agent_id: str
    message: str
    context: dict | None = None


async def _stream_response(agent_id: str, message: str, user: str):
    """Generate SSE stream for agent response."""
    # Placeholder - will integrate with actual agents later
    yield f"data: {json.dumps({'type': 'start', 'agent': agent_id})}\n\n"
    yield f"data: {json.dumps({'type': 'chunk', 'content': f'[{agent_id}] Processing: {message}'})}\n\n"
    yield f"data: {json.dumps({'type': 'chunk', 'content': f'Analysis in progress by {agent_id} for user {user}...'})}\n\n"
    yield f"data: {json.dumps({'type': 'done', 'agent': agent_id})}\n\n"


@router.post("")
async def chat_with_agent(
    request: ChatRequest,
    user: TokenData = Depends(get_current_user),
):
    """Chat with a security agent via SSE streaming."""
    return StreamingResponse(
        _stream_response(request.agent_id, request.message, user.sub),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
