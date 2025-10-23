# database/db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///money.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_session():
    return SessionLocal()

def init_db():
    from models.usuario import Usuario
    from models.transacao import Transacao
    from models.despesa import Despesa
    from models.receita import Receita
    #from models.metodo_pagamento import MetodoDePagamento
    Base.metadata.create_all(bind=engine)
