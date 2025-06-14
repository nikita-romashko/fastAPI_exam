from database import Base
from sqlalchemy import Enum,Column, Integer, String, ForeignKey, Table, DateTime,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from enums import ArticleStatusEnum

article_category = Table(
    "article_category",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True,nullable=False)
    description = Column(String(255))

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    last_name = Column(String(255),nullable=False)
    patronymic = Column(String(255),nullable=True)
    email = Column(String(255),unique=True,nullable=False)
    password_hash= Column(String(255),nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"),nullable=False)
    phone= Column(String(255),nullable=True)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    role = relationship("Role")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer,primary_key=True,autoincrement=True)
    author_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    status = Column(Enum(ArticleStatusEnum, name='article_status'), default=ArticleStatusEnum.DRAFT, nullable=False)
    published_at = Column(DateTime(), nullable = True)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete")
    categories = relationship("Category", secondary=article_category, back_populates="articles")
    likes = relationship("Like", back_populates="article", cascade="all, delete")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    article_id=Column(Integer, ForeignKey("articles.id",ondelete="CASCADE"),nullable=False)
    text= Column(Text)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    articles = relationship("Article", secondary=article_category, back_populates="categories")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="likes")
    article = relationship("Article", back_populates="likes")