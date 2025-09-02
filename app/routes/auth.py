from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..models.user import Token, LoginRequest
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from ..utils.security import create_access_token
from ..config.database import get_database
from ..config.settings import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_database)
):
    """
    Login endpoint to get JWT access token
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    # Authenticate user
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db = Depends(get_database)
):
    """
    Login endpoint with JSON payload to get JWT access token
    """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    
    # Authenticate user
    user = await user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}