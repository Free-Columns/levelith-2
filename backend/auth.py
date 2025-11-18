"""
Authentication and Authorization Module

This module handles JWT token generation, validation, and authentication
for the Levelith application.

Features:
- Access token generation (30 minute expiry)
- Refresh token generation (7 day expiry)
- Token validation and verification
- User authentication dependency for FastAPI endpoints
- Secure password verification

Security Implementation:
- SECURITY-002: bcrypt password hashing (implemented in models/user.py)
- SECURITY-003: JWT token generation and validation (implemented here)
- SECURITY-004: Authentication dependency for endpoint protection (implemented here)
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from backend.config import settings
from backend.models.user import User

# HTTP Bearer token scheme
security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data structure."""
    user_id: str
    username: str
    token_type: str  # "access" or "refresh"


class TokenResponse(BaseModel):
    """Response model for token endpoints."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires


def create_access_token(user_id: str, username: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: Unique user identifier
        username: User's username
        expires_delta: Optional custom expiration time (default: 30 minutes from settings)

    Returns:
        str: Encoded JWT access token

    Example:
        >>> token = create_access_token(user_id="123", username="johndoe")
        >>> # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expire = datetime.utcnow() + expires_delta

    to_encode = {
        "sub": user_id,
        "username": username,
        "token_type": "access",
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(user_id: str, username: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token for a user.

    Args:
        user_id: Unique user identifier
        username: User's username
        expires_delta: Optional custom expiration time (default: 7 days from settings)

    Returns:
        str: Encoded JWT refresh token

    Example:
        >>> token = create_refresh_token(user_id="123", username="johndoe")
        >>> # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.refresh_token_expire_days)

    expire = datetime.utcnow() + expires_delta

    to_encode = {
        "sub": user_id,
        "username": username,
        "token_type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_token_pair(user_id: str, username: str) -> TokenResponse:
    """
    Create both access and refresh tokens for a user.

    Args:
        user_id: Unique user identifier
        username: User's username

    Returns:
        TokenResponse: Object containing both tokens and metadata

    Example:
        >>> tokens = create_token_pair(user_id="123", username="johndoe")
        >>> print(tokens.access_token)
        >>> print(tokens.refresh_token)
    """
    access_token = create_access_token(user_id=user_id, username=username)
    refresh_token = create_refresh_token(user_id=user_id, username=username)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60  # convert to seconds
    )


def verify_token(token: str, expected_type: str = "access") -> TokenData:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify
        expected_type: Expected token type ("access" or "refresh")

    Returns:
        TokenData: Decoded token data

    Raises:
        HTTPException: If token is invalid, expired, or wrong type

    Example:
        >>> token_data = verify_token(token="eyJhbGci...", expected_type="access")
        >>> print(token_data.user_id)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        token_type: str = payload.get("token_type")

        if user_id is None or username is None or token_type is None:
            raise credentials_exception

        if token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {expected_type}, got {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(user_id=user_id, username=username, token_type=token_type)

    except JWTError:
        raise credentials_exception


async def get_current_user_db(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    FastAPI dependency to get the current authenticated user ID from token.

    This function validates the JWT token and returns the token data.
    Use this as a dependency in protected endpoints that use SQLAlchemy.

    Args:
        credentials: HTTP Bearer credentials from request header

    Returns:
        TokenData: Token data containing user_id and username

    Raises:
        HTTPException: If token is invalid

    Example:
        ```python
        @router.get("/protected")
        async def protected_route(
            token_data: TokenData = Depends(get_current_user_db)
        ):
            return {"message": f"Hello {token_data.username}"}
        ```
    """
    token = credentials.credentials
    token_data = verify_token(token, expected_type="access")
    return token_data


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    FastAPI dependency to get the current active user.

    This is a convenience wrapper around get_current_user that ensures
    the user is active. Use this for endpoints that require an active account.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User: The authenticated active user

    Raises:
        HTTPException: If user is not active

    Example:
        ```python
        @router.post("/post-content")
        async def post_content(
            current_user: User = Depends(get_current_active_user)
        ):
            return {"message": "Content posted"}
        ```
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def refresh_access_token(refresh_token: str, user_repository: UserRepository) -> TokenResponse:
    """
    Generate a new access token using a refresh token.

    Args:
        refresh_token: Valid refresh token
        user_repository: User repository for database access

    Returns:
        TokenResponse: New token pair (access + refresh)

    Raises:
        HTTPException: If refresh token is invalid

    Example:
        >>> new_tokens = refresh_access_token(refresh_token="eyJhbGci...", user_repository=repo)
        >>> print(new_tokens.access_token)
    """
    token_data = verify_token(refresh_token, expected_type="refresh")

    # Verify user still exists and is active
    user = user_repository.get_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Create new token pair
    return create_token_pair(user_id=user.id, username=user.username)
