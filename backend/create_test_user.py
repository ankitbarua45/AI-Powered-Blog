import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_test_user():
    # Connect to MongoDB
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "ai_blog_platform")
    
    client = AsyncIOMotorClient(mongodb_url)
    db = client[database_name]
    
    try:
        # Check if test user already exists
        existing_user = await db.users.find_one({"username": "admin234ai"})
        if existing_user:
            print("Test user 'admin234ai' already exists.")
            return
        
        # Create test user
        test_user = {
            "email": "admin234ai@test.com",
            "username": "admin234ai",
            "full_name": "Test Admin",
            "hashed_password": get_password_hash("12345ty"),
            "is_active": True
        }
        
        result = await db.users.insert_one(test_user)
        print(f"Test user created successfully with ID: {result.inserted_id}")
        print("Username: admin234ai")
        print("Password: 12345ty")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_test_user())
