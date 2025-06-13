from fastapi import FastAPI
from routes.users import user_router
from routes.auth import auth_router
from routes.articles import article_router
app = FastAPI()
app.include_router(article_router)
app.include_router(user_router)
app.include_router(auth_router)
