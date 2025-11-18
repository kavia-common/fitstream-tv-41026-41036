from __future__ import annotations

import datetime as dt
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import get_settings

# Initialize password hashing context (bcrypt)
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Do not log the input. Validate that password is a non-empty string before calling.
    """
    if not isinstance(password, str) or password == "":
        # Basic validation per PySecure minimal standard
        raise ValueError("Password must be a non-empty string.")
    return _pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    Returns True if match, False otherwise.
    """
    if not isinstance(plain_password, str) or plain_password == "":
        return False
    if not isinstance(hashed_password, str) or hashed_password == "":
        return False
    try:
        return _pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Avoid leaking details about hash internals
        return False


# PUBLIC_INTERFACE
def create_access_token(subject: str, extra_claims: Optional[Dict[str, Any]] = None, expires_delta_minutes: Optional[int] = None) -> str:
    """
    Create a signed JWT access token.

    Parameters:
    - subject: Unique identifier for the token subject (e.g., user id/email)
    - extra_claims: Optional dict of additional claims to include
    - expires_delta_minutes: Optional override for expiry minutes

    Returns: Encoded JWT string.
    """
    settings = get_settings()
    to_encode: Dict[str, Any] = extra_claims.copy() if extra_claims else {}
    now = dt.datetime.utcnow()
    expire_minutes = expires_delta_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    exp = now + dt.timedelta(minutes=expire_minutes)
    to_encode.update({"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())})

    # Using HS256 symmetric signing
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


# PUBLIC_INTERFACE
def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Raises:
      JWTError for invalid tokens or expired tokens.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # Basic validation: ensure required claims exist
        if "sub" not in payload:
            raise JWTError("Invalid token: missing subject")
        return payload
    except JWTError:
        # Re-raise to allow caller to map to 401 without exposing details
        raise
