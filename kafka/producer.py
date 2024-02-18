from confluent_kafka import Producer

from logs.logger import logger


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(
            {
                'bootstrap.servers': 'localhost:9092',
                'client.id': 'python-producer',
            }
        )

    def produce(self, topic, value):
        try:
            self.producer.produce(topic, value.encode('utf-8'))
            self.producer.flush()
            logger.info(
                f"Mensagem enviada com sucesso para o tópico '{topic}'."
            )
        except Exception as e:
            logger.error(f'Erro ao enviar mensagem para o Kafka: {e}')

    def close(self):
        self.producer.close()
