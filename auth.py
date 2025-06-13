from fastapi import HTTPException, Depends, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext
import models as m
import datetime
import jwt
from config import settings
from typing import Optional

class AuthHandler:
    security=HTTPBearer(auto_error=False)
    pwd_context=CryptContext(
        schemes=['bcrypt']
    )
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    
    def verify_password(self,input_password,db_password):
        return self.pwd_context.verify(input_password,db_password)
    
    def encode_token(self,user_id):
        payload={
            'exp':datetime.datetime.now(tz=datetime.timezone.utc)
            +datetime.timedelta(minutes=30),
            'iat':datetime.datetime.now(tz=datetime.timezone.utc),
            'user_id':user_id
        }
        return jwt.encode(payload,settings.SECRET,algorithm="HS256")

    def decode_token(self,token):
        try:
            payload=jwt.decode(token,settings.SECRET,algorithms="HS256")
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(401,"Просрочка")
        except jwt.InvalidTokenError:
            raise HTTPException(401,"Неверный токен")
        
    def get_current_user(
    self,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ):
        user_id = auth_handler.decode_token(token.credentials)
        user = db.query(m.User).filter(m.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user

    def get_optional_user(
        self,
        db: Session = Depends(get_db),
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ):
        if credentials is None:
            return None
        try:
            user_id = self.decode_token(credentials.credentials)
            user = db.query(m.User).filter(m.User.id == user_id).first()
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
    def auth_wrapper(self,auth:HTTPAuthorizationCredentials=Security(security)):
        return self.decode_token(auth.credentials)
    
auth_handler=AuthHandler()
