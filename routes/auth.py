from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from passlib.context import CryptContext
from auth import auth_handler

auth_router=APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/register", response_model=pyd.BaseUser)
def user_reg(user: pyd.CreateUser, db:Session=Depends(get_db)):
    user_db=db.query(m.User).filter(m.User.email==user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db=m.User()
    user_db.name=user.name
    user_db.last_name=user.last_name
    user_db.patronymic=user.patronymic
    user_db.email=user.email
    user_db.role_id=user.role_id
    user_db.password_hash=pwd_context.hash(user.password)
    user_db.phone=user.phone
    db.add(user_db)
    db.commit()
    return user_db

@auth_router.post("/login")
def user_auth(login:pyd.LoginUser,db:Session=Depends(get_db)):
    user_db=db.query(m.User).filter(m.User.email==login.email).first()
    if not user_db:
        raise HTTPException(404)
    if auth_handler.verify_password(login.password,user_db.password_hash):
        return {"token":auth_handler.encode_token(user_db.id)}
    raise HTTPException(400)
