from .base_models import *
from typing import List

class SchemaUser(BaseUser):
    role:BaseRole

class SchemaArticle(BaseArticle):
    author:BaseUser
    categories:List[BaseCategory]
    comments:List[BaseComment]

class SchemaComment(BaseComment):
    article:BaseArticle
    user:BaseUser

class SchemaLike(BaseLike):
    user: SchemaUser
    article: SchemaArticle