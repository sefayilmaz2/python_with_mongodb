from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..models.product import Product, ProductCreate, ProductUpdate, ProductResponse
from ..models.user import User
from ..services.product_service import ProductService
from ..repositories.product_repository import ProductRepository
from ..utils.dependencies import get_current_active_user
from ..config.database import get_database

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new product
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    return await product_service.create_product(product_create)


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    active_only: bool = Query(False, description="Return only active products"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all products with optional filtering and pagination
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    # Handle different filtering options
    if search:
        return await product_service.search_products(search, skip=skip, limit=limit)
    elif category:
        return await product_service.get_products_by_category(category, skip=skip, limit=limit)
    elif active_only:
        return await product_service.get_active_products(skip=skip, limit=limit)
    else:
        return await product_service.get_all_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific product by ID
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    return await product_service.get_product_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a product
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    return await product_service.update_product(product_id, product_update)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a product
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete product"
        )


@router.get("/category/{category}", response_model=List[ProductResponse])
async def get_products_by_category(
    category: str,
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get products by category
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    return await product_service.get_products_by_category(category, skip=skip, limit=limit)


@router.get("/search/{search_term}", response_model=List[ProductResponse])
async def search_products(
    search_term: str,
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search products by name or description
    """
    product_repository = ProductRepository(db)
    product_service = ProductService(product_repository)
    
    return await product_service.search_products(search_term, skip=skip, limit=limit)