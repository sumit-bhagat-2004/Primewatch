from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.models import User, UserRole
from app.schemas.user import TokenData

# HTTP Bearer token security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: The HTTP authorization credentials containing the JWT token
        db: Database session

    Returns:
        The authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    # Extract user info from token
    email: Optional[str] = payload.get("sub")
    user_id: Optional[str] = payload.get("user_id")

    if email is None or user_id is None:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.id == UUID(user_id)).first()

    if user is None:
        raise credentials_exception

    return user


def require_role(required_role: UserRole):
    """
    Dependency factory to check if user has the required role.

    Args:
        required_role: The role required to access the endpoint

    Returns:
        A dependency function that checks the user's role
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role: {required_role.value}"
            )
        return current_user
    return role_checker


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user is an admin.

    Args:
        current_user: The current authenticated user

    Returns:
        The user if they are an admin

    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
