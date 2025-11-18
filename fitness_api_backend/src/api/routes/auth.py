from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.db.session import get_session
from src.schemas.auth import RegisterRequest, TokenResponse, UserProfile, AuthError, MeResponse
from src.services.auth_service import authenticate_user, create_user_access_token, get_current_user, register_user
from src.models.users import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserProfile,
    responses={400: {"model": AuthError}, 409: {"model": AuthError}, 422: {"model": AuthError}},
    summary="Register a new user",
    description="Create a new user account with email and password. Returns the created user profile.",
)
def register_endpoint(payload: RegisterRequest, session: Session = Depends(get_session)) -> UserProfile:
    """
    Register endpoint.

    Parameters:
        payload: RegisterRequest with email and password.
    Returns:
        UserProfile of newly created user.
    """
    user = register_user(email=payload.email, password=payload.password, session=session)
    return UserProfile(id=user.id, email=user.email, is_active=user.is_active)


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={400: {"model": AuthError}, 401: {"model": AuthError}},
    summary="Obtain JWT access token",
    description="Authenticate using email and password to receive a Bearer token. Supports both JSON body and form data for OAuth2PasswordRequestForm.",
)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> TokenResponse:
    """
    Login endpoint. Accepts OAuth2PasswordRequestForm fields (username, password).
    For client convenience, use Content-Type: application/x-www-form-urlencoded.
    """
    # OAuth2 expects 'username' — we treat it as email
    user = authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        # Safe error not revealing if email or password was incorrect
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_user_access_token(user)
    return TokenResponse(access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model=MeResponse,
    responses={401: {"model": AuthError}, 403: {"model": AuthError}},
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user. Requires Bearer token in Authorization header.",
)
def me_endpoint(current_user: User = Depends(get_current_user)) -> MeResponse:
    """
    Return the currently authenticated user's profile.

    Returns:
        MeResponse with id, email, is_active
    """
    return MeResponse(id=current_user.id, email=current_user.email, is_active=current_user.is_active)
