from pydantic import BaseModel, Field
from typing import Literal

class ArticleCreate(BaseModel):
    author_id: int = Field(..., example=1)
    title: str = Field(..., example="Где можно отдохнуть этим летом?")
    content: str = Field(..., example="Лето — идеальное время для путешествий и отдыха...")
    published_at: str = Field(..., example="2025-06-01 10:00:00")

class CommentCreate(BaseModel):
    article_id: int = Field(..., example=1)
    user_id: int = Field(..., example=3)
    text: str = Field(..., example="Отличные советы, спасибо!")
    created_at: str = Field(..., example="2025-06-02 14:30:00")

class CategoryCreate(BaseModel):
    name: str = Field(..., example="Путешествия")