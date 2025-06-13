from sqlalchemy.orm import Session
from database import engine
import models as m
from enums import ArticleStatusEnum
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    # Роли
    role_admin = m.Role(name="Модератор", description=" управление всеми статьями и комментариями")
    role_author = m.Role(name="Автор", description="создание/редактирование своих статей")
    role_reader = m.Role(name="Читатель", description="чтение статей, комментарии")
    session.add_all([role_admin, role_author, role_reader])
    session.commit()

    user1 = m.User(
        name="Иван",
        last_name="Иванов",
        patronymic="Иванович",
        email="ivan@example.com",
        password_hash=pwd_context.hash("supersecret123"),
        role_id=role_author.id,
        phone="+79123456701"
    )
    user2 = m.User(
        name="Мария",
        last_name="Петрова",
        patronymic="Петровна",
        email="maria@example.com",
        password_hash=pwd_context.hash("supersecret123"),
        role_id=role_reader.id,
        phone="+79123456702"
    )
    user3 = m.User(
        name="Игорь",
        last_name="Петров",
        patronymic="Иванович",
        email="igori@example.com",
        password_hash=pwd_context.hash("supersecret123"),
        role_id=role_admin.id,
        phone="+79124456702"
    )
    session.add_all([user1, user2, user3])
    session.commit()


    cat_science = m.Category(name="tech")
    cat_travel = m.Category(name="travel")
    cat_culture = m.Category(name="culture")
    session.add_all([cat_science, cat_travel, cat_culture])
    session.commit()


    article1 = m.Article(
        author_id=user1.id,
        title="Путешествие по Алтаю",
        content="Алтай — это уникальное место для любителей природы...",
        status=ArticleStatusEnum.PUBLISHED.value,
        published_at=datetime.now(),
        categories=[cat_travel]
    )
    article2 = m.Article(
        author_id=user1.id,
        title="Новейшие открытия в биологии",
        content="В последние годы биология достигла значительных успехов...",
        status=ArticleStatusEnum.DRAFT.value,
        categories=[cat_science]
    )
    session.add_all([article1, article2])
    session.commit()


    comment1 = m.Comment(
        user_id=user2.id,
        article_id=article1.id,
        text="Очень познавательная статья, спасибо!"
    )
    comment2 = m.Comment(
        user_id=user2.id,
        article_id=article2.id,
        text="Ждём публикацию статьи."
    )
    session.add_all([comment1, comment2])
    session.commit()


    like1 = m.Like(
        user_id=user2.id,
        article_id=article1.id
    )
    session.add(like1)
    session.commit()