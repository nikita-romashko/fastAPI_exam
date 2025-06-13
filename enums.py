import enum

class ArticleStatusEnum(str, enum.Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'