from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.models.models import User, UserRole
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        db: Database session
        email: User's email address

    Returns:
        User if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        db: Database session
        user_id: User's UUID

    Returns:
        User if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password: str, role: UserRole = UserRole.USER) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        email: User's email address
        password: User's plain text password (will be hashed)
        role: User's role (default: USER)

    Returns:
        The created user
    """
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        db: Database session
        email: User's email address
        password: User's plain text password

    Returns:
        User if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
