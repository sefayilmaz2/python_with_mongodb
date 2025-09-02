from typing import List, Optional
from fastapi import HTTPException, status
from ..models.user import User, UserCreate, UserUpdate, UserResponse
from ..repositories.user_repository import UserRepository
from ..utils.security import get_password_hash, verify_password
from datetime import datetime


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if username already exists
        if await self.user_repository.username_exists(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if await self.user_repository.email_exists(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_create.password)
        
        # Create user data
        user_data = {
            "username": user_create.username,
            "email": user_create.email,
            "hashed_password": hashed_password,
            "is_active": True
        }
        
        # Create user in database
        created_user = await self.user_repository.create_user(user_data)
        
        # Convert to response model
        return UserResponse(
            _id=str(created_user["_id"]),
            username=created_user["username"],
            email=created_user["email"],
            is_active=created_user["is_active"],
            created_at=created_user["created_at"]
        )

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            _id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            is_active=user["is_active"],
            created_at=user["created_at"]
        )

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users"""
        users = await self.user_repository.get_all(skip=skip, limit=limit)
        return [
            UserResponse(
                _id=str(user["_id"]),
                username=user["username"],
                email=user["email"],
                is_active=user["is_active"],
                created_at=user["created_at"]
            )
            for user in users
        ]

    async def update_user(self, user_id: str, user_update: UserUpdate) -> UserResponse:
        """Update user"""
        # Check if user exists
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prepare update data
        update_data = {}
        if user_update.username is not None:
            # Check if new username already exists (and it's not the same user)
            existing_username = await self.user_repository.get_by_username(user_update.username)
            if existing_username and str(existing_username["_id"]) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            update_data["username"] = user_update.username
        
        if user_update.email is not None:
            # Check if new email already exists (and it's not the same user)
            existing_email = await self.user_repository.get_by_email(user_update.email)
            if existing_email and str(existing_email["_id"]) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already taken"
                )
            update_data["email"] = user_update.email
        
        if user_update.is_active is not None:
            update_data["is_active"] = user_update.is_active
        
        # Update user
        updated_user = await self.user_repository.update(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user"
            )
        
        return UserResponse(
            _id=str(updated_user["_id"]),
            username=updated_user["username"],
            email=updated_user["email"],
            is_active=updated_user["is_active"],
            created_at=updated_user["created_at"]
        )

    async def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        # Check if user exists
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return await self.user_repository.delete(user_id)

    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with username and password"""
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        if not user["is_active"]:
            return None
        
        return user