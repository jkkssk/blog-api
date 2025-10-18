from pydantic import BaseModel
from datetime import datetime
from typing import List


class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Post(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    likes: int = 0
    ratings: List[int] = []
    rating: float = 0.0
