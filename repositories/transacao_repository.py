from datetime import datetime

from sqlalchemy import extract
from database.db_session import SessionLocal
from models.despesa import Despesa
from models.receita import Receita
from models.transacao import Transacao

class TransacaoRepository:
    def __init__(self, session_factory=SessionLocal):
        self.__session_factory = session_factory

    def add(self, transacao: Transacao):
        session = self.__session_factory()
        session.add(transacao)
        session.commit()
        session.close()

    def update(self, transacao: Transacao):
        session = self.__session_factory()
        session.merge(transacao) 
        session.commit()
        session.close()

    def delete(self, transacao: Transacao):
        session = self.__session_factory()
        session.delete(transacao)
        session.commit()
        session.close()

    def get_transacoes_by_user(self, usuario_id):
        session = self.__session_factory()
        items = session.query(Transacao).filter(Transacao.usuario_id == usuario_id).all()
        session.close()
        return items
    
    def get_receitas_by_user(self, usuario_id):
        session = self.__session_factory()
        items = session.query(Receita).filter(Receita.usuario_id == usuario_id).all()
        session.close()
        return items
    
    def get_despesas_by_user(self, usuario_id):
        session = self.__session_factory()
        items = session.query(Despesa).filter(Despesa.usuario_id == usuario_id).all()
        session.close()
        return items
    

    def get_current_month_transactions(self, usuario_id):
        session = self.__session_factory()
        now = datetime.now()

        transacoes = (
            session.query(Transacao)
            .filter(
                Transacao.usuario_id == usuario_id,
                extract('year', Transacao.data) == now.year,
                extract('month', Transacao.data) == now.month
            )
            .all()
        )
        session.close()
        return transacoes
    
    def get_current_month_despesas(self, usuario_id):
        session = self.__session_factory()
        now = datetime.now()

        despesas = (
            session.query(Despesa)
            .filter(
                Transacao.usuario_id == usuario_id,
                extract('year', Despesa.data) == now.year,
                extract('month', Despesa.data) == now.month
            )
            .all()
        )
        session.close()
        return despesas
    

    # TODO
    def get_balance(id):
        pass