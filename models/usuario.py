from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_session import Base

class Usuario(Base):
    __tablename__ = 'TUSU'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)
    email = Column(String)

    transacoes = relationship("Transacao", back_populates="usuario")
