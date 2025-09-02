from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId


class Product(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(..., ge=0)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias="_id")
    name: str
    description: Optional[str]
    price: float
    category: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]