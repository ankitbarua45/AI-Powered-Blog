from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        python_schema = core_schema.with_info_plain_validator_function(
            cls.validate
        )
        json_schema = core_schema.str_schema()
        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def validate(cls, v: Any, *args, **kwargs) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

# User Models
class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class UserInDB(User):
    hashed_password: str

# Blog Post Models
class BlogPostBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category_id: Optional[str] = None
    tags: List[str] = []
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: List[str] = []
    is_published: bool = False

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_published: Optional[bool] = None

class BlogPost(BlogPostBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    author_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Category Models
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Tag Models
class TagBase(BaseModel):
    name: str
    slug: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# AI Feature Models
class AISuggestionRequest(BaseModel):
    topic: str
    suggestion_type: str = "outline"  # outline, headings, intro
    context: Optional[str] = None

class AISuggestionResponse(BaseModel):
    suggestions: List[str]
    type: str

class AITextRewriteRequest(BaseModel):
    text: str
    rewrite_type: str = "improve"  # improve, shorten, expand, formal, casual
    context: Optional[str] = None

class AITextRewriteResponse(BaseModel):
    rewritten_text: str
    original_text: str

# SEO Models
class SEOAnalysisRequest(BaseModel):
    title: str
    content: str
    target_keywords: List[str] = []

class SEOAnalysisResponse(BaseModel):
    score: int
    suggestions: List[str]
    meta_title_suggestion: str
    meta_description_suggestion: str
    keyword_analysis: dict
