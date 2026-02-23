import hashlib
import secrets
from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

ROLE_ADMIN = "Admin"
ROLE_OPERATOR = "Operator"
ROLE_ANALYST = "Analyst"

_TOKEN_STORE: dict[str, int] = {}
_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    payload = f"{settings.secret_key}:{password}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _TOKEN_STORE[token] = user_id
    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth token")

    user_id = _TOKEN_STORE.get(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*allowed_roles: str) -> Callable[[User], User]:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.name not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency


def enforce_analytics_abac(user: User, h3_index: str) -> None:
    if user.role.name != ROLE_ANALYST:
        return

    assigned_regions = user.assigned_regions()
    if h3_index not in assigned_regions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst is not assigned to this H3 region",
        )
