from fastapi import APIRouter, HTTPException, Depends, Query, status
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List, Optional
import pyd
from auth import auth_handler
from enums import ArticleStatusEnum

article_router=APIRouter(prefix="/posts", tags=["posts"])

@article_router.get("/", response_model=List[pyd.SchemaArticle])
def get_articles(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    category: Optional[str] = Query(None),
    status: Optional[ArticleStatusEnum] = Query(None),
    current_user: Optional[m.User] = Depends(auth_handler.get_optional_user)
):
    skip = (page - 1) * limit
    query = db.query(m.Article)

    if status == ArticleStatusEnum.DRAFT:
        if current_user is None:
            raise HTTPException(status_code=403, detail="Требуется авторизация для просмотра черновиков")
        if current_user.role.name != "Модератор":
            query = query.filter(m.Article.author_id == current_user.id)
        query = query.filter(m.Article.status == ArticleStatusEnum.DRAFT)

    else:
        if current_user is None or current_user.role.name != "Модератор":
            query = query.filter(m.Article.status == ArticleStatusEnum.PUBLISHED)

    if category:
        query = query.join(m.Article.categories).filter(m.Category.name == category)

    articles = query.offset(skip).limit(limit).all()
    return articles

@article_router.get("/{article_id}", response_model=pyd.SchemaArticle)
def get_article(article_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[m.User] = Depends(auth_handler.get_optional_user)):
    article = db.query(m.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    if article.status == ArticleStatusEnum.DRAFT:
        if current_user is None:
            raise HTTPException(status_code=403, detail="Требуется авторизация для просмотра черновиков")
        if current_user.role.name != "Модератор" and article.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Нет доступа к этой статье")

    return article

@article_router.post("/", response_model=pyd.SchemaArticle, status_code=status.HTTP_201_CREATED)
def create_article(
    article: pyd.CreateArticle,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user)
):
    if current_user.role.name not in ("Автор", "Модератор"):
        raise HTTPException(status_code=403, detail="Только авторы или модераторы могут создавать статьи")
    db_article = m.Article(
        title=article.title,
        content=article.content,
        status=article.status,
        author_id=current_user.id
    )
    if article.category_ids:
        db_article.categories = db.query(m.Category).filter(m.Category.id.in_(article.category_ids)).all()

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@article_router.put("/{article_id}", response_model=pyd.SchemaArticle)
def update_article(
    article_id: int,
    new_data: pyd.CreateArticle,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user)
):
    article = db.query(m.Article).get(article_id)
    print(article.author_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    if article.author_id != current_user.id and current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа")

    article.title = new_data.title
    article.content = new_data.content
    article.status = new_data.status
    article.categories = db.query(m.Category).filter(m.Category.id.in_(new_data.category_ids)).all()

    db.commit()
    db.refresh(article)
    return article

@article_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user)
):
    article = db.query(m.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    if article.author_id != current_user.id and current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа")

    db.delete(article)
    db.commit()