import logging

class CustomLogger:
    def __init__(self, log_file_path='logs/app.log'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Configurar o formato do log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Configurar o manipulador do log para escrever em um arquivo
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Configurar o manipulador do log para imprimir na saída padrão
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Adicionar os manipuladores ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

# Exemplo de uso
if __name__ == "__main__":
    logger = CustomLogger()

    logger.info("Informação")
    logger.warning("Aviso")
    logger.error("Erro")
    try:
        # Simulando uma exceção
        raise ValueError("Exceção simulada")
    except Exception as e:
        logger.exception("Exceção ocorrida: %s" % str(e))
