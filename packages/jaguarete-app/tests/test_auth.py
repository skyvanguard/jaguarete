"""Tests for JWT authentication."""

import pytest
from jaguarete_app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)
from jaguarete_app.auth.models import (
    ROLE_SCOPES,
    LoginRequest,
    Scope,
    TokenData,
    TokenResponse,
    User,
    UserRole,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "secure_password_123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password(self):
        hashed = hash_password("correct")
        assert not verify_password("wrong", hashed)


class TestTokens:
    def test_create_and_verify_access_token(self):
        data = {"sub": "testuser", "role": "admin", "scopes": ["red_team"]}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert payload["type"] == "access"

    def test_create_and_verify_refresh_token(self):
        data = {"sub": "testuser", "role": "analyst"}
        token = create_refresh_token(data)
        payload = verify_token(token, expected_type="refresh")
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert payload["type"] == "refresh"

    def test_access_token_rejected_as_refresh(self):
        token = create_access_token({"sub": "user"})
        assert verify_token(token, expected_type="refresh") is None

    def test_refresh_token_rejected_as_access(self):
        token = create_refresh_token({"sub": "user"})
        assert verify_token(token, expected_type="access") is None

    def test_invalid_token(self):
        assert verify_token("invalid.token.here") is None

    def test_empty_token(self):
        assert verify_token("") is None


class TestModels:
    def test_user_role_enum(self):
        assert UserRole.ADMIN == "admin"
        assert UserRole.ANALYST == "analyst"
        assert UserRole.VIEWER == "viewer"

    def test_scope_enum(self):
        assert Scope.RED_TEAM == "red_team"
        assert Scope.BLUE_TEAM == "blue_team"

    def test_role_scopes_mapping(self):
        assert len(ROLE_SCOPES[UserRole.ADMIN]) == 4
        assert Scope.RED_TEAM in ROLE_SCOPES[UserRole.ANALYST]
        assert Scope.RED_TEAM not in ROLE_SCOPES[UserRole.VIEWER]

    def test_user_model(self):
        user = User(
            username="admin",
            hashed_password="hashed",
            role=UserRole.ADMIN,
        )
        assert user.username == "admin"
        assert user.disabled is False

    def test_token_response(self):
        resp = TokenResponse(access_token="a", refresh_token="r")
        assert resp.token_type == "bearer"

    def test_login_request(self):
        req = LoginRequest(username="user", password="pass")
        assert req.username == "user"
