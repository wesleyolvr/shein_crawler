from db.db_manager import Base
from sqlalchemy import  Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import  relationship
from sqlalchemy import func


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)  # Assumindo que o ID do produto é uma string
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

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, default=func.now())
    price = Column(Float)

    # Chave estrangeira para o produto
    product_id = Column(String, ForeignKey('products.product_id'))
    product = relationship('Product', back_populates='price_history')