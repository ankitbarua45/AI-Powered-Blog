from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from models.schemas import BlogPostCreate, BlogPostUpdate, BlogPost, Category, Tag, CategoryCreate, TagCreate
from models.database import get_database
from routers.auth import get_current_user, User
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=BlogPost)
async def create_blog_post(
    post: BlogPostCreate,
    current_user = Depends(get_current_user)
):
    try:
        db = await get_database()
        
        post_dict = post.dict()
        # Handle both dict and User objects
        author_id = current_user.get("id") if isinstance(current_user, dict) else str(current_user.id)
        post_dict["author_id"] = author_id
        
        if post.is_published:
            post_dict["published_at"] = datetime.utcnow()
        
        result = await db.blog_posts.insert_one(post_dict)
        created_post = await db.blog_posts.find_one({"_id": result.inserted_id})
        
        return BlogPost(**created_post)
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection not available")

@router.get("/", response_model=List[BlogPost])
async def get_blog_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[str] = None,
    tag: Optional[str] = None,
    is_published: Optional[bool] = None
):
    try:
        db = await get_database()
        
        query = {}
        if category_id:
            query["category_id"] = category_id
        if tag:
            query["tags"] = tag
        if is_published is not None:
            query["is_published"] = is_published
        
        posts = await db.blog_posts.find(query).skip(skip).limit(limit).to_list(length=limit)
        return [BlogPost(**post) for post in posts]
    except Exception as e:
        # Return empty list if database is not connected (for demo purposes)
        print(f"Database error: {e}")
        return []

@router.get("/{post_id}", response_model=BlogPost)
async def get_blog_post(post_id: str):
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        post = await db.blog_posts.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return BlogPost(**post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection not available")

@router.put("/{post_id}", response_model=BlogPost)
async def update_blog_post(
    post_id: str,
    post_update: BlogPostUpdate,
    current_user = Depends(get_current_user)
):
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        existing_post = await db.blog_posts.find_one({"_id": ObjectId(post_id)})
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Handle both dict and User objects
        user_id = current_user.get("id") if isinstance(current_user, dict) else str(current_user.id)
        if existing_post["author_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")
        
        update_dict = {k: v for k, v in post_update.dict().items() if v is not None}
        
        if "is_published" in update_dict:
            if update_dict["is_published"] and not existing_post.get("is_published"):
                update_dict["published_at"] = datetime.utcnow()
        
        update_dict["updated_at"] = datetime.utcnow()
        
        await db.blog_posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": update_dict}
        )
        
        updated_post = await db.blog_posts.find_one({"_id": ObjectId(post_id)})
        return BlogPost(**updated_post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection not available")

@router.delete("/{post_id}")
async def delete_blog_post(
    post_id: str,
    current_user = Depends(get_current_user)
):
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        existing_post = await db.blog_posts.find_one({"_id": ObjectId(post_id)})
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Handle both dict and User objects
        user_id = current_user.get("id") if isinstance(current_user, dict) else str(current_user.id)
        if existing_post["author_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")
        
        await db.blog_posts.delete_one({"_id": ObjectId(post_id)})
        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection not available")

@router.post("/categories", response_model=Category)
async def create_category(
    category: CategoryCreate,
    current_user = Depends(get_current_user)
):
    db = await get_database()
    
    # Check if category already exists
    existing_category = await db.categories.find_one({"slug": category.slug})
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists"
        )
    
    result = await db.categories.insert_one(category.dict())
    created_category = await db.categories.find_one({"_id": result.inserted_id})
    
    return Category(**created_category)

@router.get("/categories/", response_model=List[Category])
async def get_categories():
    db = await get_database()
    categories = await db.categories.find().to_list(length=100)
    return [Category(**category) for category in categories]

@router.post("/tags", response_model=Tag)
async def create_tag(
    tag: TagCreate,
    current_user = Depends(get_current_user)
):
    db = await get_database()
    
    # Check if tag already exists
    existing_tag = await db.tags.find_one({"slug": tag.slug})
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this slug already exists"
        )
    
    result = await db.tags.insert_one(tag.dict())
    created_tag = await db.tags.find_one({"_id": result.inserted_id})
    
    return Tag(**created_tag)

@router.get("/tags/", response_model=List[Tag])
async def get_tags():
    db = await get_database()
    tags = await db.tags.find().to_list(length=100)
    return [Tag(**tag) for tag in tags]
