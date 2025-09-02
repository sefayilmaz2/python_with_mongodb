from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime


class BaseRepository(ABC):
    def __init__(self, database, collection_name: str):
        self.database = database
        self.collection_name = collection_name
        self.collection: AsyncIOMotorCollection = database[collection_name]

    async def create(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document"""
        document["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(document)
        created_document = await self.collection.find_one({"_id": result.inserted_id})
        return created_document

    async def get_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        if not ObjectId.is_valid(document_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(document_id)})

    async def get_all(self, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get all documents with pagination and optional filters"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(self, document_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update document by ID"""
        if not ObjectId.is_valid(document_id):
            return None
        
        update_data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.collection.find_one({"_id": ObjectId(document_id)})
        return None

    async def delete(self, document_id: str) -> bool:
        """Delete document by ID"""
        if not ObjectId.is_valid(document_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0

    async def count(self, filters: Dict[str, Any] = None) -> int:
        """Count documents with optional filters"""
        query = filters or {}
        return await self.collection.count_documents(query)

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if document exists with given filters"""
        count = await self.collection.count_documents(filters, limit=1)
        return count > 0

    def convert_objectid_to_str(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ObjectId to string for JSON serialization"""
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document