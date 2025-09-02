from typing import List, Dict, Any, Optional
from .base import BaseRepository


class BrandRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, "brand")

    async def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get brand by name"""
        return await self.collection.find_one({"name": name})

    async def get_active_brands(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all active brands"""
        return await self.get_all(skip=skip, limit=limit, filters={"is_active": True})

    async def search_brands(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search brands by name or description"""
        query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return await self.get_all(skip=skip, limit=limit, filters=query)

    async def name_exists(self, name: str) -> bool:
        """Check if brand name already exists"""
        return await self.exists({"name": name})