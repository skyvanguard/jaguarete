"""FastAPI authentication dependencies."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jaguarete_app.auth.jwt import verify_token
from jaguarete_app.auth.models import Scope, TokenData, UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """Extract and validate the current user from JWT token."""
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenData(
        sub=payload["sub"],
        role=UserRole(payload.get("role", "viewer")),
        scopes=payload.get("scopes", []),
    )


def require_scope(scope: Scope):
    """Dependency factory to require a specific scope."""
    async def _check_scope(user: TokenData = Depends(get_current_user)) -> TokenData:
        if scope.value not in user.scopes and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope '{scope.value}' required",
            )
        return user
    return _check_scope
