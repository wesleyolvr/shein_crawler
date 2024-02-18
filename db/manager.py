from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import configure_mappers, sessionmaker

from api.schemas.comment import CommentCreate
from api.schemas.price_history import PriceHistoryUpdate
from api.schemas.product import ProductCreate, ProductRead
from api.schemas.rating import ProductRatingCreate
from db.database import Base
from db.models.comment import Comment
from db.models.image import Image
from db.models.price_history import PriceHistory
from db.models.product import Product
from db.models.rating import ProductRating
from logs.logger import logger


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)

        configure_mappers()

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def create_product(self, product_data: ProductCreate):
        """
        Cria um novo produto no banco de dados.
        """
        new_product = Product(**product_data)

        self.session.add(new_product)
        self.session.commit()
        logger.info(f'New product {new_product.data_title}')

    def update_product(self, product_data: ProductCreate):
        """
        Atualiza os dados de um produto existente no banco de dados.
        """
        product_data = ProductCreate(**product_data).model_dump()
        existing_product = self.get_product_by_id(product_data['product_id'])
        if existing_product:
            if existing_product.data_price != product_data['data_price']:
                logger.info(
                    f'Updating product {product_data["data_title"]} : new price : {product_data["data_price"]} - old price : {existing_product.data_price}'
                )
                # Atualiza os dados do produto existente, se o valor do preço for diferente do existente
                existing_product.data_price = product_data['data_price']
                existing_product.data_us_price = product_data['data_us_price']
                existing_product.data_us_origin_price = product_data[
                    'data_us_origin_price'
                ]
                existing_product.discount = product_data['discount']
                existing_product.image_src = product_data['image_src']

                product_price = PriceHistoryUpdate(
                    product_id=product_data['product_id'],
                    new_price=product_data['data_price'],
                    date=datetime.now(),
                    price=product_data['data_price'],
                )

                # Cria um novo registro de preço para o novo valor
                self.add_price_history(product_price)
                self.session.commit()

    def update_product_price(self, product_price: PriceHistoryUpdate):
        """
        Atualiza o preço de um produto existente no banco de dados.
        """
        product = (
            self.session.query(Product)
            .filter_by(product_id=product_price.product_id)
            .first()
        )
        if product:
            product.data_price = product_price.new_price
            self.session.commit()

    def get_product_by_id(self, product_id: str):
        """
        Retorna um produto do banco de dados com base no ID.
        """
        return (
            self.session.query(Product)
            .filter_by(product_id=product_id)
            .first()
        )

    def get_product_by_title(self, product_read: ProductRead):
        """
        Retorna um produto do banco de dados com base no título.
        """
        return (
            self.session.query(Product)
            .filter_by(data_title=product_read['title'])
            .first()
        )

    def get_price_history_by_id(self, product_read: ProductRead):
        """
        Retorna o histórico de preços de um determinado produto.
        """
        return (
            self.session.query(PriceHistory)
            .filter_by(product_id=product_read['product_id'])
            .all()
        )

    def add_price_history(self, product_price: PriceHistoryUpdate):
        """
        Adiciona um novo histórico de preço para um produto no banco de dados.
        """
        product = self.get_product_by_id(product_price.product_id)
        if product:
            new_price_history = PriceHistory(
                date=datetime.now(),
                price=product_price.new_price,
                product=product,
            )
            logger.info(
                f'New price history for product {product.data_title} : new price : {product_price.new_price}'
            )
            product.price_history.append(
                new_price_history
            )  # Adiciona o novo histórico à lista
            self.session.commit()

    def get_all_products(self):
        return self.session.query(Product).all()

    def get_all_href_products(self):
        return self.session.query(Product.href).all()

    def get_products_with_multiple_price_history(self):
        """
        Retorna todos os produtos que possuem mais de um histórico de preços.
        """
        # Subconsulta para contar o número de registros em PriceHistory para cada produto
        subquery = (
            self.session.query(
                PriceHistory.product_id,
                func.count().label('count_price_history'),
            )
            .group_by(PriceHistory.product_id)
            .subquery()
        )

        # Consulta principal para obter produtos com mais de um histórico de preços
        products_with_multiple_history = (
            self.session.query(Product)
            .join(subquery, Product.product_id == subquery.c.product_id)
            .filter(subquery.c.count_price_history > 1)
            .all()
        )

        return products_with_multiple_history

    def add_comment(self, comment: CommentCreate):
        """
        Adiciona um novo comentário para um determinado produto de um determinado nickname.
        """
        comment = CommentCreate(**comment).model_dump()
        product = (
            self.session.query(Product)
            .filter_by(product_id=comment['product_id'])
            .first()
        )
        if product:
            new_comment = Comment(
                text=comment['text'],
                nickname=comment['nickname'],
                product=product,
                date=datetime.now(),
            )
            self.session.add(new_comment)
            self.session.commit()

            if comment['images']:
                # Adiciona imagens ao comentário
                for image_src in comment['images']:
                    new_image = Image(file_name=image_src, comment=new_comment)
                    self.session.add(new_image)

                self.session.commit()

    def add_rate(self, rate: ProductRatingCreate, product_id: str):
        """
        Adiciona uma avaliação para um determinado produto.
        """
        product = self.get_product_by_id(product_id)
        if product:
            new_rate = ProductRating(rating=rate, product=product)
            self.session.add(new_rate)
            self.session.commit()
