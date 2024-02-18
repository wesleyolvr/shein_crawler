from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.manager import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    comment = relationship('Comment', back_populates='images')
