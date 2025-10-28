from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_session import Base


class Usuario(Base):
    __tablename__ = 'TUSU'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nasc = Column(String)
    cpf = Column(String)
    profissao = Column(String)
    renda_mensal = Column(String)
    user = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    transacoes = relationship("Transacao", back_populates="usuario")
    limites = relationship("Limite", back_populates="usuario")
