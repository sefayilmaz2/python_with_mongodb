from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from .config.settings import settings
from .config.database import connect_to_mongo, close_mongo_connection
from .routes import auth, users, products

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="A Python Web API with MongoDB, JWT Authentication, and CRUD operations for Users and Products",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Exception",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )


# Database event handlers
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await connect_to_mongo()
        logger.info("Application startup completed")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    try:
        await close_mongo_connection()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.project_name,
        "version": "1.0.0"
    }


# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.api_v1_str}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.api_v1_str}/users",
    tags=["Users"]
)

app.include_router(
    products.router,
    prefix=f"{settings.api_v1_str}/products",
    tags=["Products"]
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )