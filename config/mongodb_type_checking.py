from typing import TYPE_CHECKING, Any
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorClientSession

if TYPE_CHECKING:
    TMongoCollection = AsyncIOMotorCollection[dict[str, Any]]
    TMongoDatabase = AsyncIOMotorDatabase[dict[str, Any]]
    TMongoClient = AsyncIOMotorClient[dict[str, Any]]
    TMongoClientSession = AsyncIOMotorClientSession
else:
    TMongoCollection = AsyncIOMotorCollection
    TMongoDatabase = AsyncIOMotorDatabase
    TMongoClient = AsyncIOMotorClient
    TMongoClientSession = AsyncIOMotorClientSession