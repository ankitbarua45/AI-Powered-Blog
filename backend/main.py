from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up AI Blog Platform Backend...")
    from models.database import database
    try:
        database.connect()
        print("Database connection established")
    except Exception as e:
        print(f"Warning: Could not connect to database: {e}")
        print("Application will run in demo mode without database...")
    yield
    # Shutdown
    print("Shutting down AI Blog Platform Backend...")
    from models.database import database
    if database.client:
        database.close()

app = FastAPI(
    title="AI Blog Platform API",
    description="Backend API for AI-Powered Blog Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Blog Platform API is running"}

# Import routers
from routers import auth, blog_posts, ai_features, seo_tools

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(blog_posts.router, prefix="/api/blog-posts", tags=["Blog Posts"])
app.include_router(ai_features.router, prefix="/api/ai", tags=["AI Features"])
app.include_router(seo_tools.router, prefix="/api/seo", tags=["SEO Tools"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
