"""Jaguarete FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jaguarete_app.config import settings
from jaguarete_app.api.auth_routes import router as auth_router
from jaguarete_app.api.agents import router as agents_router
from jaguarete_app.api.chat import router as chat_router
from jaguarete_app.api.knowledge import router as knowledge_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Purple Team Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(agents_router, prefix="/api/agents", tags=["agents"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["knowledge"])


@app.get("/api/health")
async def health_check():
    return {"status": "operational", "service": settings.app_name, "version": settings.app_version}
