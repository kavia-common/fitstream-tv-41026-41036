from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlmodel import select
from src.core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from src.db.session import get_session
from src.models.users import User
from sqlmodel import Session

# OAuth2 scheme declares where clients obtain tokens (the login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def register_user(email: str, password: str, session: Session) -> User:
    """
    Create a new user with hashed password.
    Validates inputs per PySecure minimal standard and returns the created User.
    """
    if not isinstance(email, str) or email.strip() == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email")
    if not isinstance(password, str) or len(password) < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid password")

    # Check existing
    existing = session.exec(select(User).where(User.email == email.lower())).first()
    if existing:
        # Conflict but do not leak details
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    hashed = get_password_hash(password)
    user = User(email=email.lower(), hashed_password=hashed, is_active=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# PUBLIC_INTERFACE
def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    """
    Validate user credentials. Returns User if valid else None.
    """
    if not isinstance(email, str) or email.strip() == "":
        return None
    if not isinstance(password, str) or password == "":
        return None

    user = session.exec(select(User).where(User.email == email.lower())).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# PUBLIC_INTERFACE
def create_user_access_token(user: User) -> str:
    """Create a JWT access token for a user with sub=email."""
    return create_access_token(subject=user.email, extra_claims={"uid": user.id, "act": user.is_active})


# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    FastAPI dependency to extract current user from Bearer token.
    Raises 401 if invalid or inactive.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise credentials_error
    subject = payload.get("sub")
    if not subject:
        raise credentials_error

    user = session.exec(select(User).where(User.email == subject.lower())).first()
    if not user:
        raise credentials_error
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive account")
    return user
