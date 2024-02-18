import json
from datetime import datetime

from api.schemas.price_history import PriceHistoryUpdate
from db.database import DATABASE_URL
from db.manager import DatabaseManager
from kafka.consumer import KafkaConsumer


class ProdutoProcessor:
    def __init__(self, kafka_topic):
        self.kafka_consumer = KafkaConsumer(kafka_topic)
        self.db_manager = DatabaseManager(database_url=DATABASE_URL)

    def processar_produto(self):
        try:
            for mensagem in self.kafka_consumer.consume():
                produto = json.loads(mensagem)
                produto_bd = self.db_manager.get_product_by_id(
                    produto['product_id']
                )
                if produto_bd:
                    # Comparar preços
                    if (
                        abs(
                            produto_bd.data_price
                            - float(produto['data_price'])
                        )
                        > 1
                    ):
                        print(
                            f"O preço do produto {produto['product_id']} foi alterado de {produto_bd.data_price} para {produto['data_price']}"
                        )
                        produto_bd.data_price = produto['data_price']
                        self.db_manager.update_product_price(
                            PriceHistoryUpdate(
                                product_id=produto['product_id'],
                                new_price=produto['data_price'],
                                date=datetime.now(),
                                price=produto['data_price'],
                            )
                        )
                else:
                    self.db_manager.create_product(produto)
                    print(f"O produto {produto['product_id']} foi adicionado")

        except KeyboardInterrupt:
            self.kafka_consumer.close()
