from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(Text)
    nickname = Column(String)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    product = relationship('Product', back_populates='comments')
    date = Column(DateTime, default=datetime.now())
    images = relationship('Image', back_populates='comment')
