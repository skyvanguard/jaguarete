"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from jaguarete_app.main import app
from jaguarete_app.auth.jwt import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token():
    return create_access_token({
        "sub": "admin",
        "role": "admin",
        "scopes": ["red_team", "blue_team", "knowledge", "reports"],
    })


@pytest.fixture
def viewer_token():
    return create_access_token({
        "sub": "viewer",
        "role": "viewer",
        "scopes": ["knowledge", "reports"],
    })


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


class TestHealth:
    def test_health_check(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert data["service"] == "Jaguarete"


class TestAuth:
    def test_login_success(self, client):
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrong"},
        )
        assert response.status_code == 401

    def test_login_unknown_user(self, client):
        response = client.post(
            "/api/auth/login",
            json={"username": "nobody", "password": "pass"},
        )
        assert response.status_code == 401

    def test_refresh_token(self, client):
        # First login
        login_resp = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin"},
        )
        refresh = login_resp.json()["refresh_token"]
        # Refresh
        response = client.post(
            f"/api/auth/refresh?refresh_token={refresh}"
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


class TestAgents:
    def test_list_agents_admin(self, client, auth_headers):
        response = client.get("/api/agents", headers=auth_headers)
        assert response.status_code == 200
        agents = response.json()["agents"]
        assert len(agents) == 8

    def test_list_agents_viewer(self, client, viewer_token):
        headers = {"Authorization": f"Bearer {viewer_token}"}
        response = client.get("/api/agents", headers=headers)
        assert response.status_code == 200
        agents = response.json()["agents"]
        # Viewer has knowledge + reports scopes only
        assert all(a["scope_required"] in ("knowledge", "reports") for a in agents)

    def test_list_agents_unauthenticated(self, client):
        response = client.get("/api/agents")
        assert response.status_code == 403 or response.status_code == 401  # No token


class TestChat:
    def test_chat_streaming(self, client, auth_headers):
        response = client.post(
            "/api/chat",
            json={"agent_id": "recon", "message": "scan example.com"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

    def test_chat_unauthenticated(self, client):
        response = client.post(
            "/api/chat",
            json={"agent_id": "recon", "message": "test"},
        )
        assert response.status_code == 403 or response.status_code == 401


class TestKnowledge:
    def test_list_knowledge_bases(self, client, auth_headers):
        response = client.get("/api/knowledge", headers=auth_headers)
        assert response.status_code == 200
        kbs = response.json()["knowledge_bases"]
        assert len(kbs) == 3

    def test_query_knowledge(self, client, auth_headers):
        response = client.post(
            "/api/knowledge/query",
            json={"query": "SQL injection", "limit": 3},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "SQL injection"
        assert len(data["results"]) > 0

    def test_knowledge_requires_scope(self, client):
        # Token without knowledge scope
        from jaguarete_app.auth.jwt import create_access_token
        token = create_access_token({
            "sub": "noscope",
            "role": "viewer",
            "scopes": [],
        })
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/knowledge", headers=headers)
        assert response.status_code == 403
