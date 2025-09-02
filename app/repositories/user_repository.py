from typing import Optional, Dict, Any
from .base import BaseRepository
from ..models.user import User


class UserRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, "users")

    async def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        return await self.collection.find_one({"username": username})

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return await self.collection.find_one({"email": email})

    async def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return await self.exists({"username": username})

    async def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return await self.exists({"email": email})

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        return await self.create(user_data)

    async def get_active_users(self, skip: int = 0, limit: int = 100):
        """Get all active users"""
        return await self.get_all(skip=skip, limit=limit, filters={"is_active": True})