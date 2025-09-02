from typing import List, Dict, Any, Optional
from .base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, "products")

    async def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get product by name"""
        return await self.collection.find_one({"name": name})

    async def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get products by category"""
        return await self.get_all(skip=skip, limit=limit, filters={"category": category})

    async def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all active products"""
        return await self.get_all(skip=skip, limit=limit, filters={"is_active": True})

    async def search_products(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search products by name or description"""
        query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return await self.get_all(skip=skip, limit=limit, filters=query)

    async def get_products_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get products within price range"""
        query = {"price": {"$gte": min_price, "$lte": max_price}}
        return await self.get_all(skip=skip, limit=limit, filters=query)

    async def get_low_stock_products(self, threshold: int = 10, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get products with low stock"""
        query = {"stock_quantity": {"$lte": threshold}, "is_active": True}
        return await self.get_all(skip=skip, limit=limit, filters=query)

    async def name_exists(self, name: str) -> bool:
        """Check if product name already exists"""
        return await self.exists({"name": name})

    async def update_stock(self, product_id: str, new_quantity: int) -> Optional[Dict[str, Any]]:
        """Update product stock quantity"""
        return await self.update(product_id, {"stock_quantity": new_quantity})