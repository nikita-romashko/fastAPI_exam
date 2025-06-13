from fastapi import FastAPI
from routes.categories import category_router
from routes.auth import auth_router
from routes.articles import article_router
from routes.comments import comment_router
from routes.likes import like_router
app = FastAPI()
app.include_router(article_router, prefix = '/api')
app.include_router(category_router, prefix = '/api')
app.include_router(comment_router, prefix = '/api')
app.include_router(like_router, prefix = '/api')
app.include_router(auth_router, prefix = '/api')
