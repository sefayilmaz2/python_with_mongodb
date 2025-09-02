from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..models.brand import Brand, BrandCreate, BrandUpdate, BrandResponse
from ..models.user import User
from ..services.brand_service import BrandService
from ..repositories.brand_repository import BrandRepository
from ..utils.dependencies import get_current_active_user
from ..config.database import get_database

router = APIRouter()


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_create: BrandCreate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new brand
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    return await brand_service.create_brand(brand_create)


@router.get("/", response_model=List[BrandResponse])
async def get_brands(
    skip: int = Query(0, ge=0, description="Number of brands to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of brands to return"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    active_only: bool = Query(False, description="Return only active brands"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all brands with optional filtering and pagination
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    # Handle different filtering options
    if search:
        return await brand_service.search_brands(search, skip=skip, limit=limit)
    elif active_only:
        return await brand_service.get_active_brands(skip=skip, limit=limit)
    else:
        return await brand_service.get_all_brands(skip=skip, limit=limit)


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(
    brand_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific brand by ID
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    return await brand_service.get_brand_by_id(brand_id)


@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: str,
    brand_update: BrandUpdate,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a brand
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    return await brand_service.update_brand(brand_id, brand_update)


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: str,
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a brand
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    success = await brand_service.delete_brand(brand_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete brand"
        )

@router.get("/search/{search_term}", response_model=List[BrandResponse])
async def search_brands(
    search_term: str,
    skip: int = Query(0, ge=0, description="Number of brands to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of brands to return"),
    db = Depends(get_database),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search brands by name or description
    """
    brand_repository = BrandRepository(db)
    brand_service = BrandService(brand_repository)
    
    return await brand_service.search_brands(search_term, skip=skip, limit=limit)