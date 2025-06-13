from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List
from datetime import datetime
from enums import ArticleStatusEnum 

class CreateUser(BaseModel):
    name: str = Field(...,example="Иван")
    last_name: str = Field(...,example="Иванов")
    password:str=Field(...,example="qweqwqe123")
    patronymic: str | None = Field(None,example="Иванович")
    email: EmailStr = Field(...,example="example@mail.ru")
    role_id:int=Field(...,example=1)
    phone: str | None = Field(None, example="+79123456789")

class CreateArticle(BaseModel):
    title:str = Field(...,example="Где можно отдохнуть этим летом?")
    content:str = Field(...,example="""Лето — идеальное время для путешествий и отдыха. Если вы ищете, где провести незабываемые каникулы, рассмотрите следующие варианты:
Черноморское побережье — тёплое море, солнце и уютные курорты.
Алтай и Байкал — для любителей природы и активного отдыха.
Заграница — Турция, Грузия и Сербия остаются доступными и интересными направлениями.
Планируйте заранее, бронируйте жильё и не забывайте про страховку. Хорошего отдыха!""")
    status: ArticleStatusEnum = Field(..., example=ArticleStatusEnum.DRAFT)
    category_ids: None | List[int] = Field(default=[], example=[1, 2])

class CreateComment(BaseModel):
    article_id:int = Field(...,example=1)
    text:str = Field(...,example="Отличная статья!")


class CreateCategory(BaseModel):
    name:str = Field(...,example="Наука")

class CreateLike(BaseModel):
    article_id: int = Field(..., example=1)