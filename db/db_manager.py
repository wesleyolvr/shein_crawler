from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from logs.logger import CustomLogger

Base = declarative_base()


class DatabaseManager:
    
    database_url = 'sqlite:///shein_data.db'
    def __init__(self):
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        self.log = CustomLogger()

    def create_product_or_update(self, product_data: dict):
        """
        Cria um novo produto ou atualiza os dados de um existente no banco de dados.
        """
        existing_product = self.get_product_by_id(product_data['product_id'])
        if existing_product:
            if existing_product.data_price != product_data['data_price']:
                self.log.info(f'Updating product {product_data["data_title"]} : new price : {product_data["data_price"]} - old price : {existing_product.data_price}')
                # Atualiza os dados do produto existente, se o valor do preço for diferente do existente
                existing_product.data_price = product_data['data_price']
                existing_product.data_us_price = product_data['data_us_price']
                existing_product.data_us_origin_price = product_data['data_us_origin_price']
                existing_product.discount = product_data['discount']
                existing_product.image_src = product_data['image_src']
                
                # Cria um novo registro de precão para o novo valor
                self.add_price_history(product_id=product_data['product_id'], price=product_data['data_price'])
            else:
                return None
        else:
            # Cria um novo produto se o product_id não existe
            new_product = Product(**product_data)
            self.session.add(new_product)
            self.session.commit()


    def update_product_price(self, product_id: str, new_price: float):
        """
        Atualiza o preço de um produto existente no banco de dados.
        """
        product = self.session.query(Product).filter_by(product_id=product_id).first()
        if product:
            product.data_price = new_price
            self.session.commit()

    def get_product_by_id(self, product_id: str):
        """
        Retorna um produto do banco de dados com base no ID.
        """
        return self.session.query(Product).filter_by(product_id=product_id).first()

    def add_price_history(self, product_id, price):
        """
        Adiciona um novo histórico de preço para um produto no banco de dados.
        """
        product = self.session.query(Product).filter_by(product_id=product_id).first()
        if product:
            new_price_history = PriceHistory(date=func.now(), price=price, product=product)
            self.session.add(new_price_history)
            self.session.commit()

    def get_price_history(self, product_id: str) -> list:
        """
        Retorna o histórico de preços de um produto com base no ID.
        """
        product = self.session.query(Product).filter_by(product_id=product_id).first()
        if product:
            return product.price_history
        return []


db_manager = DatabaseManager()

from db.database import Product, PriceHistory
