from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        db.database = db.client[settings.database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB at {settings.mongodb_url}")
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    try:
        if db.client:
            db.client.close()
            logger.info("Disconnected from MongoDB")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


async def get_collection(collection_name: str):
    """Get a specific collection from the database"""
    if db.database is None:
        raise Exception("Database not initialized")
    return db.database[collection_name]