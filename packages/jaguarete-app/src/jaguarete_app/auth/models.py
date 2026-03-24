"""Authentication models."""

from enum import Enum
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Scope(str, Enum):
    """Permission scopes."""
    RED_TEAM = "red_team"
    BLUE_TEAM = "blue_team"
    KNOWLEDGE = "knowledge"
    REPORTS = "reports"


# Role -> default scopes mapping
ROLE_SCOPES: dict[UserRole, list[Scope]] = {
    UserRole.ADMIN: list(Scope),
    UserRole.ANALYST: [Scope.RED_TEAM, Scope.BLUE_TEAM, Scope.KNOWLEDGE, Scope.REPORTS],
    UserRole.VIEWER: [Scope.KNOWLEDGE, Scope.REPORTS],
}


class User(BaseModel):
    """User model."""
    username: str
    hashed_password: str
    role: UserRole = UserRole.VIEWER
    scopes: list[Scope] = Field(default_factory=list)
    disabled: bool = False


class TokenData(BaseModel):
    """JWT token payload data."""
    sub: str  # username
    role: UserRole
    scopes: list[str] = Field(default_factory=list)


class TokenResponse(BaseModel):
    """Token response for login endpoint."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Login request body."""
    username: str
    password: str
