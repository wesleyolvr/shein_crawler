from confluent_kafka import Consumer

from logs.logger import logger


class KafkaConsumer:
    def __init__(self, topic):
        self.consumer = Consumer(
            {
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'my_consumer_group',
                'auto.offset.reset': 'earliest',
            }
        )
        self.topic = topic
        self.consumer.subscribe([self.topic])

    def consume(self):
        while True:
            msg = self.consumer.poll(5.0)
            if msg is None:
                logger.info('Não há mensagens')
                continue
            if msg.error():
                logger.error(f'Erro no consumidor: {msg.error()}')
                continue
            msg_txt = msg.value().decode('utf-8')
            logger.info(f'Mensagem recebida: {msg_txt}')
            yield msg_txt

    def close(self):
        self.consumer.close()
