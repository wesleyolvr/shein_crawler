from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class CommentBase(BaseModel):
    text: str
    nickname: str
    product_id: int
    date: datetime
    images: List[str]


class CommentCreate(CommentBase):
    pass

    @validator('date', pre=True)
    # pylint: disable=no-self-argument
    def format_type_products(cls, value):
        """Formata a data para datetime."""
        return datetime.strptime(value, '%d %b,%Y')


class CommentRead(CommentBase):
    id: int
    images: Optional[str]

    class Config:
        orm_mode = True
