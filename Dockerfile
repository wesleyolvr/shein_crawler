FROM python:3.10-slim

RUN apt-get update && apt-get install -y gnupg curl

# Instale as dependências necessárias
RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Baixe e instale o Chrome
RUN apt-get update  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Baixe e instale o ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    curl -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN touch shein_data.db

CMD ["python3", "crawler/shein_crawler.py"]