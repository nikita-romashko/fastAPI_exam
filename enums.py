import enum

class ArticleStatusEnum(str, enum.Enum):
    DRAFT = 'черновик'
    PUBLISHED = 'опубликовано'