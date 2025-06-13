from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models as m
import pyd
from database import get_db
from auth import auth_handler

comment_router = APIRouter(prefix="/comments", tags=["comments"])

@comment_router.get("/", response_model=List[pyd.SchemaComment])
def get_comments(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    article_id: Optional[int] = Query(None, description="Фильтрация по статье"),
    current_user: Optional[m.User] = Depends(auth_handler.get_optional_user),
):
    skip = (page - 1) * limit
    query = db.query(m.Comment)
    if article_id:
        query = query.filter(m.Comment.article_id == article_id)
    comments = query.offset(skip).limit(limit).all()
    return comments

@comment_router.get("/{comment_id}", response_model=pyd.SchemaComment)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[m.User] = Depends(auth_handler.get_optional_user),
):
    comment = db.query(m.Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment

@comment_router.post("/", response_model=pyd.SchemaComment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: pyd.CreateComment,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    db_comment = m.Comment(
        article_id=comment.article_id,
        user_id=current_user.id,
        text=comment.text,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@comment_router.put("/{comment_id}", response_model=pyd.SchemaComment)
def update_comment(
    comment_id: int,
    comment_data: pyd.CreateComment,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    comment = db.query(m.Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    if comment.user_id != current_user.id and current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа для редактирования")

    comment.text = comment_data.text
    db.commit()
    db.refresh(comment)
    return comment

@comment_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    comment = db.query(m.Comment).get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    if comment.user_id != current_user.id and current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа для удаления")

    db.delete(comment)
    db.commit()
