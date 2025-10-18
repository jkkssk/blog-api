from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

class Post(BaseModel):
    id: int
    authorId: int
    title: str
    content: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    likes: int = 0
    ratings: List[int] = []
    rating: float = 0.0