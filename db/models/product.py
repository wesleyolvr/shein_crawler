from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.manager import Base


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    href = Column(String)
    data_title = Column(String)
    data_price = Column(Float)
    data_id_category = Column(String)
    data_sku = Column(String)
    data_spu = Column(String)
    data_us_price = Column(Float)
    data_us_origin_price = Column(Float)
    discount = Column(String)
    image_src = Column(String)
    product_type = Column(String)

    # Relacionamento com o histórico de preços
    price_history = relationship('PriceHistory', back_populates='product')

    # Relacionamento com os comentários
    comments = relationship('Comment', back_populates='product')

    # Relacionamento com as avaliações
    ratings = relationship('ProductRating', back_populates='product')
