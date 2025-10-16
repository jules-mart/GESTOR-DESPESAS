from database.db_session import SessionLocal
from models.transacao import Transacao

class TransacaoRepository:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def add(self, transacao: Transacao):
        session = self._session_factory()
        session.add(transacao)
        session.commit()
        session.close()

    def get_all(self):
        session = self._session_factory()
        items = session.query(Transacao).all()
        session.close()
        return items
    
    # TODO
    def get_balance(id):
        pass