from .base_models import *
from typing import List,  Optional

class SchemaUser(BaseUser):
    role:BaseRole

class SchemaLike(BaseLike):
    user: BaseUser

class SchemaArticle(BaseArticle):
    author:BaseUser
    categories:List[BaseCategory]
    comments:List[BaseComment]
    likes_count: Optional[int] = 0
    likes:List[SchemaLike]

class SchemaComment(BaseComment):
    article:BaseArticle
    user:BaseUser
