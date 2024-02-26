from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from db.manager import Base


class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, default=func.now())
    price = Column(Float)

    # Chave estrangeira para o produto
    product_id = Column(Integer, ForeignKey('products.product_id'))

    # Relacionamento com o produto
    product = relationship('Product', back_populates='price_history')
