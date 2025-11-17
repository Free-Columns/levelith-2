"""
User Management API Endpoints

Provides REST API for user CRUD operations and authentication.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import UserDB
from backend.models.user import hash_password, verify_password
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, UserWithExperiences

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
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        User information with experiences

    Raises:
        HTTPException: If user not found
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
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all users with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of users
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
async def update_user(user_id: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information.

    Args:
        user_id: User ID
        user_data: Updated user data
        db: Database session

    Returns:
        Updated user information

    Raises:
        HTTPException: If user not found
    """
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
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session

    Raises:
        HTTPException: If user not found
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()


@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        Authentication token information

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # TODO: Implement JWT token generation
    # For now, return basic user info
    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "note": "JWT token generation to be implemented"
    }
