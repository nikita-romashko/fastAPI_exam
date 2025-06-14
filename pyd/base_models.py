from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enums import ArticleStatusEnum

class BaseRole(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Автор")
    description:str | None = Field(example="создание/редактирование своих статей")

class BaseUser(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Иван")
    last_name: str = Field(example="Иванов")
    patronymic: str | None = Field(example="Иванович")
    email: EmailStr = Field(example="example@mail.ru")
    phone: str | None = Field(example="+79123456789")
    updated_at: datetime = Field(example = "2025-06-01 15:30:00")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")

class BaseArticle(BaseModel):
    id:int = Field(example=1)
    title:str = Field(example="Где можно отдохнуть этим летом?")
    content:str = Field(example="""Лето — идеальное время для путешествий и отдыха. Если вы ищете, где провести незабываемые каникулы, рассмотрите следующие варианты:
Черноморское побережье — тёплое море, солнце и уютные курорты.
Алтай и Байкал — для любителей природы и активного отдыха.
Заграница — Турция, Грузия и Сербия остаются доступными и интересными направлениями.
Планируйте заранее, бронируйте жильё и не забывайте про страховку. Хорошего отдыха!""")
    status: ArticleStatusEnum = Field(example=ArticleStatusEnum.DRAFT)
    published_at: datetime | None = Field(example = "2025-06-01 15:30:00")
    updated_at: datetime = Field(example = "2025-06-01 15:30:00")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")

class BaseComment(BaseModel):
    id:int = Field(example=1)
    text:str = Field(example="Отличная статья!")
    updated_at: datetime = Field(example = "2025-06-01 15:30:00")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")


class BaseCategory(BaseModel):
    id:int = Field(example=1)
    name:str = Field(example="Наука")
    updated_at: datetime = Field(example = "2025-06-01 15:30:00")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")

class BaseLike(BaseModel):
    id: int = Field(example=1)
    updated_at: datetime = Field(example = "2025-06-01 15:30:00")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")

class LoginUser(BaseModel):
    email:str=Field(example='example@mail.ru',min_length=3,max_length=60)
    password:str=Field(example='qwerty123',min_length=8,max_length=60)