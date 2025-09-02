from typing import List, Optional
from fastapi import HTTPException, status
from ..models.product import Product, ProductCreate, ProductUpdate, ProductResponse
from ..repositories.product_repository import ProductRepository
from datetime import datetime


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def create_product(self, product_create: ProductCreate) -> ProductResponse:
        """Create a new product"""
        # Check if product name already exists
        if await self.product_repository.name_exists(product_create.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product name already exists"
            )
        
        # Create product data
        product_data = {
            "name": product_create.name,
            "description": product_create.description,
            "price": product_create.price,
            "category": product_create.category,
            "stock_quantity": product_create.stock_quantity,
            "is_active": True
        }
        
        # Create product in database
        created_product = await self.product_repository.create(product_data)
        
        # Convert to response model
        return ProductResponse(
            _id=str(created_product["_id"]),
            name=created_product["name"],
            description=created_product.get("description"),
            price=created_product["price"],
            category=created_product["category"],
            stock_quantity=created_product["stock_quantity"],
            is_active=created_product["is_active"],
            created_at=created_product["created_at"],
            updated_at=created_product.get("updated_at")
        )

    async def get_product_by_id(self, product_id: str) -> ProductResponse:
        """Get product by ID"""
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return ProductResponse(
            _id=str(product["_id"]),
            name=product["name"],
            description=product.get("description"),
            price=product["price"],
            category=product["category"],
            stock_quantity=product["stock_quantity"],
            is_active=product["is_active"],
            created_at=product["created_at"],
            updated_at=product.get("updated_at")
        )

    async def get_all_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Get all products"""
        products = await self.product_repository.get_all(skip=skip, limit=limit)
        return [
            ProductResponse(
                _id=str(product["_id"]),
                name=product["name"],
                description=product.get("description"),
                price=product["price"],
                category=product["category"],
                stock_quantity=product["stock_quantity"],
                is_active=product["is_active"],
                created_at=product["created_at"],
                updated_at=product.get("updated_at")
            )
            for product in products
        ]

    async def get_active_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Get all active products"""
        products = await self.product_repository.get_active_products(skip=skip, limit=limit)
        return [
            ProductResponse(
                _id=str(product["_id"]),
                name=product["name"],
                description=product.get("description"),
                price=product["price"],
                category=product["category"],
                stock_quantity=product["stock_quantity"],
                is_active=product["is_active"],
                created_at=product["created_at"],
                updated_at=product.get("updated_at")
            )
            for product in products
        ]

    async def update_product(self, product_id: str, product_update: ProductUpdate) -> ProductResponse:
        """Update product"""
        # Check if product exists
        existing_product = await self.product_repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Prepare update data
        update_data = {}
        if product_update.name is not None:
            # Check if new name already exists (and it's not the same product)
            existing_name = await self.product_repository.get_by_name(product_update.name)
            if existing_name and str(existing_name["_id"]) != product_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product name already exists"
                )
            update_data["name"] = product_update.name
        
        if product_update.description is not None:
            update_data["description"] = product_update.description
        
        if product_update.price is not None:
            update_data["price"] = product_update.price
        
        if product_update.category is not None:
            update_data["category"] = product_update.category
        
        if product_update.stock_quantity is not None:
            update_data["stock_quantity"] = product_update.stock_quantity
        
        if product_update.is_active is not None:
            update_data["is_active"] = product_update.is_active
        
        # Update product
        updated_product = await self.product_repository.update(product_id, update_data)
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update product"
            )
        
        return ProductResponse(
            _id=str(updated_product["_id"]),
            name=updated_product["name"],
            description=updated_product.get("description"),
            price=updated_product["price"],
            category=updated_product["category"],
            stock_quantity=updated_product["stock_quantity"],
            is_active=updated_product["is_active"],
            created_at=updated_product["created_at"],
            updated_at=updated_product.get("updated_at")
        )

    async def delete_product(self, product_id: str) -> bool:
        """Delete product"""
        # Check if product exists
        existing_product = await self.product_repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return await self.product_repository.delete(product_id)

    async def search_products(self, search_term: str, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Search products by name or description"""
        products = await self.product_repository.search_products(search_term, skip=skip, limit=limit)
        return [
            ProductResponse(
                _id=str(product["_id"]),
                name=product["name"],
                description=product.get("description"),
                price=product["price"],
                category=product["category"],
                stock_quantity=product["stock_quantity"],
                is_active=product["is_active"],
                created_at=product["created_at"],
                updated_at=product.get("updated_at")
            )
            for product in products
        ]

    async def get_products_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Get products by category"""
        products = await self.product_repository.get_by_category(category, skip=skip, limit=limit)
        return [
            ProductResponse(
                _id=str(product["_id"]),
                name=product["name"],
                description=product.get("description"),
                price=product["price"],
                category=product["category"],
                stock_quantity=product["stock_quantity"],
                is_active=product["is_active"],
                created_at=product["created_at"],
                updated_at=product.get("updated_at")
            )
            for product in products
        ]