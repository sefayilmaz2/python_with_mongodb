from typing import List, Optional
from fastapi import HTTPException, status
from ..models.brand import Brand, BrandCreate, BrandUpdate, BrandResponse
from ..repositories.brand_repository import BrandRepository
from datetime import datetime


class BrandService:
    def __init__(self, brand_repository: BrandRepository):
        self.brand_repository = brand_repository

    async def create_brand(self, brand_create: BrandCreate) -> BrandResponse:
        """Create a new brand"""
        # Check if brand name already exists
        if await self.brand_repository.name_exists(brand_create.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Brand name already exists"
            )
        
        # Create brand data
        brand_data = {
            "name": brand_create.name,
            "description": brand_create.description,
            "is_active": True
        }
        
        # Create brand in database
        created_brand = await self.brand_repository.create(brand_data)
        
        # Convert to response model
        return BrandResponse(
            _id=str(created_brand["_id"]),
            name=created_brand["name"],
            description=created_brand.get("description"),
            is_active=created_brand["is_active"],
            created_at=created_brand["created_at"],
            updated_at=created_brand.get("updated_at")
        )

    async def get_brand_by_id(self, brand_id: str) -> BrandResponse:
        """Get brand by ID"""
        brand = await self.brand_repository.get_by_id(brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        
        return BrandResponse(
            _id=str(brand["_id"]),
            name=brand["name"],
            description=brand.get("description"),
            is_active=brand["is_active"],
            created_at=brand["created_at"],
            updated_at=brand.get("updated_at")
        )

    async def get_all_brands(self, skip: int = 0, limit: int = 100) -> List[BrandResponse]:
        """Get all brands"""
        brands = await self.brand_repository.get_all(skip=skip, limit=limit)
        return [
            BrandResponse(
                _id=str(brand["_id"]),
                name=brand["name"],
                description=brand.get("description"),
                is_active=brand["is_active"],
                created_at=brand["created_at"],
                updated_at=brand.get("updated_at")
            )
            for brand in brands
        ]

    async def get_active_brands(self, skip: int = 0, limit: int = 100) -> List[BrandResponse]:
        """Get all active brands"""
        brands = await self.brand_repository.get_active_brands(skip=skip, limit=limit)
        return [
            BrandResponse(
                _id=str(brand["_id"]),
                name=brand["name"],
                description=brand.get("description"),
                is_active=brand["is_active"],
                created_at=brand["created_at"],
                updated_at=brand.get("updated_at")
            )
            for brand in brands
        ]

    async def update_brand(self, brand_id: str, brand_update: BrandUpdate) -> BrandResponse:
        """Update brand"""
        # Check if brand exists
        existing_brand = await self.brand_repository.get_by_id(brand_id)
        if not existing_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        
        # Prepare update data
        update_data = {}
        if brand_update.name is not None:
            # Check if new name already exists (and it's not the same brand)
            existing_name = await self.brand_repository.get_by_name(brand_update.name)
            if existing_name and str(existing_name["_id"]) != brand_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Brand name already exists"
                )
            update_data["name"] = brand_update.name
        
        if brand_update.description is not None:
            update_data["description"] = brand_update.description
        
        if brand_update.is_active is not None:
            update_data["is_active"] = brand_update.is_active
        
        # Update brand
        updated_brand = await self.brand_repository.update(brand_id, update_data)
        if not updated_brand:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update brand"
            )
        
        return BrandResponse(
            _id=str(updated_brand["_id"]),
            name=updated_brand["name"],
            description=updated_brand.get("description"),
            is_active=updated_brand["is_active"],
            created_at=updated_brand["created_at"],
            updated_at=updated_brand.get("updated_at")
        )

    async def delete_brand(self, brand_id: str) -> bool:
        """Delete brand"""
        # Check if brand exists
        existing_brand = await self.brand_repository.get_by_id(brand_id)
        if not existing_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        
        return await self.brand_repository.delete(brand_id)

    async def search_brands(self, search_term: str, skip: int = 0, limit: int = 100) -> List[BrandResponse]:
        """Search brands by name or description"""
        brands = await self.brand_repository.search_brands(search_term, skip=skip, limit=limit)
        return [
            BrandResponse(
                _id=str(brand["_id"]),
                name=brand["name"],
                description=brand.get("description"),
                is_active=brand["is_active"],
                created_at=brand["created_at"],
                updated_at=brand.get("updated_at")
            )
            for brand in brands
        ]