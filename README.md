# Crawler Shein

O **Crawler Shein** é um projeto de Web Scraping desenvolvido para extrair informações detalhadas de produtos do site Shein. Automatizando a coleta de dados, o projeto visa criar um histórico de preços para análises detalhadas das variações ao longo do tempo.

## Funcionalidades

- **Web Scraping Automatizado:** Utiliza Selenium para automatizar a navegação e extração de dados do site Shein.
- **Armazenamento em Banco de Dados:** Utiliza um banco de dados SQLite para armazenar os dados extraídos.

## Instalação
Antes de começar, certifique-se de ter o Python e o Docker instalados no seu sistema.

Para instalar e usar o Crawler Shein, siga as instruções detalhadas abaixo:

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/crawler-shein.git
    cd crawler-shein
    ```

2. Construa a imagem Docker:

    ```bash
    docker build -t crawler-shein .
    ```

3. Execute o container Docker:

    ```bash
    docker run -it crawler-shein
    ```

## Uso

Após executar o container Docker, o projeto será iniciado automaticamente. Os dados extraídos serão armazenados em um banco de dados SQLite.

## Próximos Passos

- **Análise de Dados:** Implementar funcionalidades para consumir os dados do banco e realizar análises de tendências de preços.
- **Serviço de Comparação de Preços:** Desenvolver um serviço que compara os preços atuais dos produtos com seus históricos para identificar oportunidades de compra.

## Contribuições

Contribuições são bem-vindas! 
Se você tem sugestões, abra uma [issue](https://github.com/wesleyolvr/shein_crawler/issues) ou envie um [pull request](https://github.com/wesleyolvr/shein_crawler/pulls) para melhorar o projeto.

