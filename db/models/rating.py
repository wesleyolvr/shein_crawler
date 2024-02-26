from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.database import Base


class ProductRating(Base):
    __tablename__ = 'product_ratings'

    id = Column(Integer, autoincrement=True, primary_key=True)
    rating = Column(Float)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    product = relationship('Product', back_populates='ratings')
