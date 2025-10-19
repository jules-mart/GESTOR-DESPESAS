from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database.db_session import Base
import enum

class TipoPagamento(enum.Enum):
    PIX = "Pix"
    DINHEIRO = "Dinheiro"
    DEBITO = "Débito"
    CREDITO = "Crédito"

class MetodoDePagamento(Base):
    __tablename__ = "TMETODO_PAGAMENTO"

    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoPagamento), nullable=False)

    transacoes = relationship("Transacao", back_populates="metodo_pagamento")
