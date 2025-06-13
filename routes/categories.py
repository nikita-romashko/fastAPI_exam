from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models as m
import pyd 
from database import get_db
from auth import auth_handler

category_router = APIRouter(prefix="/categories", tags=["categories"])

@category_router.get("/", response_model=List[pyd.BaseCategory])
def get_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    name: Optional[str] = Query(None, description="Фильтрация по части названия категории"),
):
    skip = (page - 1) * limit
    query = db.query(m.Category)
    
    if name:
        query = query.filter(m.Category.name.ilike(f"%{name}%"))

    categories = query.offset(skip).limit(limit).all()
    return categories

@category_router.get("/{category_id}", response_model=pyd.BaseCategory)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(m.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@category_router.post("/", response_model=pyd.BaseCategory, status_code=status.HTTP_201_CREATED)
def create_category(
    category: pyd.CreateCategory,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    if current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа")
    db_category = m.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@category_router.put("/{category_id}", response_model=pyd.BaseCategory)
def update_category(
    category_id: int,
    category_data: pyd.CreateCategory,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    if current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа")
    category = db.query(m.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    category.name = category_data.name
    db.commit()
    db.refresh(category)
    return category

@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(auth_handler.get_current_user),
):
    if current_user.role.name != "Модератор":
        raise HTTPException(status_code=403, detail="Нет доступа")
    category = db.query(m.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    db.delete(category)
    db.commit()