from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from ..models.user import User, UserCreate, UserUpdate, UserResponse
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..utils.dependencies import get_current_active_user
from ..config.database import get_database

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new user
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    return await user_service.create_user(user_create)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all users with pagination
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    return await user_service.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific user by ID
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a user
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    return await user_service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a user
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user"
        )


@router.get("/me/profile", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """
    Get current user's profile
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    # Get user by username from the token
    user_data = await user_repository.get_by_username(current_user.username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        _id=str(user_data["_id"]),
        username=user_data["username"],
        email=user_data["email"],
        is_active=user_data["is_active"],
        created_at=user_data["created_at"]
    )