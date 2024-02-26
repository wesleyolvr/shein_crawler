# Apache Kafka e Apache Zookeeper

Este guia aborda os passos necessários para configurar e executar o Apache Kafka e o Apache Zookeeper em sua máquina local. Estes serviços são essenciais para processar e armazenar dados na arquitetura de streaming de dados.

## Pré-requisitos

Certifique-se de ter o Apache Kafka e o Apache Zookeeper instalados em sua máquina local. Você pode encontrar os tutoriais de instalação [aqui](https://kafka.apache.org/quickstart) e [aqui](https://zookeeper.apache.org/doc/current/zookeeperStarted.html), respectivamente.

## Passos

1. **Inicie o Zookeeper**:
   ```sh
   zookeeper-server-start.sh config/zookeeper.properties
   ```

2. **Inicie o Kafka**:
   ```sh
   kafka-server-start.sh config/server.properties
   ```

3. **Crie um tópico** (opcional):
   ```sh
   kafka-topics.sh --create --topic meu-topico --bootstrap-server localhost:9092
   ```

4. **Liste os tópicos existentes** (opcional):
   ```sh
   kafka-topics.sh --list --bootstrap-server localhost:9092
   ```

5. **Publique uma mensagem em um tópico** (opcional):
   ```sh
   kafka-console-producer.sh --topic meu-topico --bootstrap-server localhost:9092
   ```

6. **Consuma mensagens de um tópico** (opcional):
   ```sh
   kafka-console-consumer.sh --topic meu-topico --from-beginning --bootstrap-server localhost:9092
   ```

7. **Exclua um tópico** (opcional):
   ```sh
   kafka-topics.sh --delete --topic meu-topico --bootstrap-server localhost:9092
   ```

8. **Desligue o Kafka e o Zookeeper**:
   - Para interromper o Kafka, pressione `Ctrl + C` no terminal onde ele está sendo executado.
   - Para interromper o Zookeeper, pressione `Ctrl + C` no terminal onde ele está sendo executado.

Depois de seguir esses passos, o Apache Kafka e o Apache Zookeeper estarão em execução em sua máquina local, e você poderá começar a trabalhar com streams de dados em seu projeto.
