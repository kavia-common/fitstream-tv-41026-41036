from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

# PUBLIC_INTERFACE
class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (min 8 chars)")

# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    """Schema for user login request."""
    username: EmailStr = Field(..., description="Email used as username for OAuth2Compatibility")
    password: str = Field(..., min_length=8, max_length=128, description="User password")

# PUBLIC_INTERFACE
class TokenResponse(BaseModel):
    """JWT token response returned on successful login."""
    access_token: str = Field(..., description="Bearer token")
    token_type: str = Field(default="bearer", description="Type of the token, always 'bearer'")

# PUBLIC_INTERFACE
class UserProfile(BaseModel):
    """Public profile information for the authenticated user."""
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    is_active: bool = Field(..., description="Whether the user is active")

# PUBLIC_INTERFACE
class AuthError(BaseModel):
    """Standard error payload for auth endpoints."""
    detail: str = Field(..., description="Error detail message")

# Optional schema used internally or by /auth/me explicitly
# PUBLIC_INTERFACE
class MeResponse(UserProfile):
    """Response body for /auth/me endpoint."""
    pass
