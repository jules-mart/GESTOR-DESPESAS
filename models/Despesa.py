from sqlalchemy import Column, Integer, ForeignKey
from models.transacao import Transacao

class Despesa(Transacao):
    __tablename__ = "TDESPESA"

    id = Column(Integer, ForeignKey("TTRANSACOES.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "despesa"
    }

    def get_valor_com_sinal(self) -> float:
        return -abs(self.valor)