import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create Async MongoDB Client
client = AsyncMongoClient(MONGODB_URI)

# Select Database
db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]

documents_collection = db["documents"]