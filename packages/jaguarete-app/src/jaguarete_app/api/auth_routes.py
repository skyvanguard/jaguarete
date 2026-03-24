"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status

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
    TokenResponse,
    User,
    UserRole,
)

router = APIRouter()

# In-memory user store (replace with DB in production)
_users: dict[str, User] = {
    "admin": User(
        username="admin",
        hashed_password=hash_password("admin"),
        role=UserRole.ADMIN,
        scopes=[s.value for s in ROLE_SCOPES[UserRole.ADMIN]],
    ),
}


def _get_user(username: str) -> User | None:
    return _users.get(username)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT tokens."""
    user = _get_user(request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disabled",
        )
    token_data = {
        "sub": user.username,
        "role": user.role.value,
        "scopes": [s if isinstance(s, str) else s.value for s in user.scopes],
    }
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    payload = verify_token(refresh_token, expected_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    token_data = {
        "sub": payload["sub"],
        "role": payload.get("role", "viewer"),
        "scopes": payload.get("scopes", []),
    }
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )
