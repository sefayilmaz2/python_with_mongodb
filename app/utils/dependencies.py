from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..utils.security import verify_token
from ..models.user import TokenData, User
from ..repositories.user_repository import UserRepository
from ..config.database import get_database

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_database)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user