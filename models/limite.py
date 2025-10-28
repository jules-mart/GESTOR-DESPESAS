from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.db_session import Base


class Limite(Base):
    __tablename__ = 'TLIMITE'

    id = Column(Integer, primary_key=True)
    valor_limite = Column(Float)
    categoria_limite = Column(String)

    usuario_id = Column(Integer, ForeignKey("TUSU.id"))
    usuario = relationship("Usuario", back_populates="limites")