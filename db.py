"""MongoDB connection and collection accessors.

Reads MONGO_URI from the environment (or a .env file).
Falls back to localhost if the variable is not set.

Usage:
    from db import get_db
    db = get_db()
    db.patients.find_one({"id": 1000})
"""
import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_DB_NAME   = os.getenv("MONGO_DB",  "healthcare")


@lru_cache(maxsize=1)
def _client() -> MongoClient:
    return MongoClient(_MONGO_URI)


def get_db() -> Database:
    """Return the healthcare MongoDB database (cached client)."""
    return _client()[_DB_NAME]
