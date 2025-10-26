from abc import ABCMeta, abstractmethod
from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_session import Base
from sqlalchemy.orm import DeclarativeMeta

class BaseMeta(DeclarativeMeta, ABCMeta):
    pass

class Transacao(Base, metaclass=BaseMeta):
    __tablename__ = "TTRANSACOES"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))
    categoria = Column(String)
    descricao = Column(String(100))
    valor = Column(Float)
    data = Column(Date)

    usuario_id = Column(Integer, ForeignKey("TUSU.id"))
    usuario = relationship("Usuario", back_populates="transacoes")

    #metodo_pagamento_id = Column(Integer, ForeignKey("TMETODO_PAGAMENTO.id"))
    #metodo_pagamento = relationship("MetodoDePagamento", back_populates="transacoes")

    metodo_pagamento = Column(String(50))

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "transacao"
    }

    @abstractmethod
    def get_valor_com_sinal(self) -> float:
        pass