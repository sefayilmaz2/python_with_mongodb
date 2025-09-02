from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from ..utils.security import verify_token
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware:
    """JWT Authentication Middleware"""
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        # Skip authentication for certain paths
        skip_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/health"
        ]
        
        if request.url.path in skip_paths:
            response = await call_next(request)
            return response
        
        # Check if path requires authentication (all API paths except login)
        if request.url.path.startswith("/api/v1/") and not request.url.path.startswith("/api/v1/auth/login"):
            authorization = request.headers.get("Authorization")
            scheme, token = get_authorization_scheme_param(authorization)
            
            if not authorization or scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            token_data = verify_token(token)
            if token_data is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Add user info to request state
            request.state.current_user = token_data.username
        
        response = await call_next(request)
        return response