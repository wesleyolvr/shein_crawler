from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

# Configuração do Banco de Dados
engine = create_engine(DATABASE_URL)

# Criando uma Sessão do Banco de Dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para Declaração de Modelos
Base = declarative_base()

# Função para Obter uma Sessão do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
