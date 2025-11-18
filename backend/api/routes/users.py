"""
User Management API Endpoints

Provides REST API for user CRUD operations and authentication.
"""

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import UserDB
from backend.models.user import hash_password, verify_password, User
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, UserWithExperiences
from backend.auth import create_token_pair, TokenResponse, verify_token, get_current_user_db, TokenData

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data: User creation data
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check if email already exists
    existing_email = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create user
    db_user = UserDB(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        profile_data=user_data.profile_data or {}
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Convert to response schema
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_verified=db_user.is_verified,
        profile_data=db_user.profile_data,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        last_login=db_user.last_login,
        experience_count=len(db_user.experiences)
    )


@router.get("/{user_id}", response_model=UserWithExperiences)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_db)
):
    """
    Get user by ID (requires authentication).

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user from token

    Returns:
        User information with experiences

    Raises:
        HTTPException: If user not found or not authenticated
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserWithExperiences(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_data=user.profile_data,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        experience_count=len(user.experiences),
        experiences=[exp.id for exp in user.experiences]
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_db)
):
    """
    List all users with pagination (requires authentication).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user from token

    Returns:
        List of users

    Raises:
        HTTPException: If not authenticated
    """
    users = db.query(UserDB).offset(skip).limit(limit).all()

    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            profile_data=user.profile_data,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            experience_count=len(user.experiences)
        )
        for user in users
    ]


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_db)
):
    """
    Update user information (requires authentication).

    Users can only update their own profile.

    Args:
        user_id: User ID
        user_data: Updated user data
        db: Database session
        current_user: Current authenticated user from token

    Returns:
        Updated user information

    Raises:
        HTTPException: If user not found or not authorized
    """
    # Verify user can only update their own profile
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    if user_data.email is not None:
        # Check if email is already taken
        existing = db.query(UserDB).filter(
            UserDB.email == user_data.email,
            UserDB.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        user.email = user_data.email

    if user_data.profile_data is not None:
        user.profile_data.update(user_data.profile_data)

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        profile_data=user.profile_data,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        experience_count=len(user.experiences)
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user_db)
):
    """
    Delete a user (requires authentication).

    Users can only delete their own account.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user from token

    Raises:
        HTTPException: If user not found or not authorized
    """
    # Verify user can only delete their own account
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )

    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access and refresh tokens.

    Args:
        credentials: Login credentials (username and password)
        db: Database session

    Returns:
        TokenResponse: JWT access token, refresh token, and metadata

    Raises:
        HTTPException: If credentials are invalid or user is inactive

    Example:
        Request:
            POST /api/v1/users/login
            {
                "username": "johndoe",
                "password": "SecurePassword123!"
            }

        Response:
            {
                "access_token": "eyJhbGci...",
                "refresh_token": "eyJhbGci...",
                "token_type": "bearer",
                "expires_in": 1800
            }
    """
    # Find user by username
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()

    # Generate JWT token pair
    tokens = create_token_pair(user_id=str(user.id), username=user.username)

    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using a valid refresh token.

    Args:
        refresh_token: Valid JWT refresh token
        db: Database session

    Returns:
        TokenResponse: New JWT access token, refresh token, and metadata

    Raises:
        HTTPException: If refresh token is invalid or user is inactive

    Example:
        Request:
            POST /api/v1/users/refresh
            {
                "refresh_token": "eyJhbGci..."
            }

        Response:
            {
                "access_token": "eyJhbGci...",
                "refresh_token": "eyJhbGci...",
                "token_type": "bearer",
                "expires_in": 1800
            }
    """
    # Verify refresh token
    token_data = verify_token(refresh_token, expected_type="refresh")

    # Verify user still exists and is active
    user = db.query(UserDB).filter(UserDB.id == token_data.user_id).first()
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
    new_tokens = create_token_pair(user_id=str(user.id), username=user.username)

    return new_tokens
