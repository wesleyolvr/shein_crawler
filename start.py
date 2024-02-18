import multiprocessing


def start_consumer():
    from api.database.manager import ProdutoProcessor

    processor_produtos = ProdutoProcessor('produtos')
    processor_produtos.processar_produto()


def start_api():
    import uvicorn

    uvicorn.run('api.main:app', reload=True)


if __name__ == '__main__':
    # Iniciar o consumidor em um processo separado
    consumer_process = multiprocessing.Process(target=start_consumer)
    consumer_process.start()

    # Iniciar a API FastAPI
    start_api()
