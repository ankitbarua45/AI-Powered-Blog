from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_blog_platform")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

class Database:
    client: Optional[AsyncIOMotorClient] = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            # Test the connection
            self.client.admin.command('ping')
            print(f"Connected to MongoDB at {settings.MONGODB_URL}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None

    def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

    def get_database(self):
        if self.client is None:
            raise Exception("Database connection not established")
        return self.client[settings.DATABASE_NAME]

database = Database()

async def get_database():
    return database.get_database()
