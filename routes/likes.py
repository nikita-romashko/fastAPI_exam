from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import models as m
from database import get_db
from auth import auth_handler

like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.post("/", status_code=status.HTTP_201_CREATED)
def add_like(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    article = db.query(m.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    existing_like = db.query(m.Like).filter_by(article_id=article_id, user_id=current_user.id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Лайк уже поставлен")

    like = m.Like(article_id=article_id, user_id=current_user.id)
    db.add(like)
    db.commit()
    return {"detail": "Лайк добавлен"}

@like_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    like = db.query(m.Like).filter_by(article_id=article_id, user_id=current_user.id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Лайк не найден")

    db.delete(like)
    db.commit()

@like_router.get("/count", summary="Получить количество лайков статьи")
def get_likes_count(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = db.query(m.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    count = db.query(m.Like).filter_by(article_id=article_id).count()
    return {"article_id": article_id, "likes_count": count}