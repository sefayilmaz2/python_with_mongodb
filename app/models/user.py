from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId


class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias="_id")
    username: str
    email: str
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None