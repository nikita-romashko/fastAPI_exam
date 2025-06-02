from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class BaseArticle(BaseModel):
    id:int = Field(example=1)
    title:str = Field(example="Где можно отдохнуть этим летом?")
    content:str=Field(example="""Лето — идеальное время для путешествий и отдыха. Если вы ищете, где провести незабываемые каникулы, рассмотрите следующие варианты:

Черноморское побережье — тёплое море, солнце и уютные курорты.

Алтай и Байкал — для любителей природы и активного отдыха.

Заграница — Турция, Грузия и Сербия остаются доступными и интересными направлениями.

Планируйте заранее, бронируйте жильё и не забывайте про страховку. Хорошего отдыха!""")
    published_at:int = Field(example="02.05.2025 10:00:00")

class BaseComment(BaseModel):
    id:int=Field(example=1)
    text:str=Field(example="Отличная статья!")
    created_at:datetime = Field(example = "2025-06-01 15:30:00")

class BaseCategory(BaseModel):
    id:int=Field(example=1)
    name:str=Field(example="Наука")