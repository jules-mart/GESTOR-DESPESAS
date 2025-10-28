from database.db_session import SessionLocal
from models.limite import Limite

class LimiteRepository:
    def __init__(self, session_factory=SessionLocal):
        self.__session_factory = session_factory

    def add(self, limite: Limite):
        session = self.__session_factory()
        session.add(limite)
        session.commit()
        session.refresh(limite)
        session.close()
        return limite

    def get_by_usuario_id(self, usuario_id: int):
        session = self.__session_factory()
        limites = session.query(Limite).filter(Limite.usuario_id == usuario_id).all()
        session.close()
        return limites

    def update(self, limite_id: int, novo_valor: float):
        session = self.__session_factory()
        limite = session.query(Limite).filter(Limite.id == limite_id).first()
        if limite:
            limite.valor_limite = novo_valor
            session.commit()
            session.refresh(limite)
        session.close()
        return limite

    def delete(self, limite_id: int):
        session = self.__session_factory()
        limite = session.query(Limite).filter(Limite.id == limite_id).first()
        if limite:
            session.delete(limite)
            session.commit()
        session.close()
        return limite

    def get_by_categoria(self, categoria: str, usuario_id: int):
        session = self.__session_factory()
        limite = session.query(Limite).filter(
            Limite.categoria_limite == categoria,
            Limite.usuario_id == usuario_id
        ).first()
        session.close()
        return limite