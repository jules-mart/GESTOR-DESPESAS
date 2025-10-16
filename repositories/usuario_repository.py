from database.db_session import SessionLocal
from models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def add(self, user: Usuario):
        session = self._session_factory()
        session.add(user)
        session.commit()
        session.close()

    def get_by_id(self, user_id: int):
        session = self._session_factory()
        user = session.get(Usuario, user_id)
        session.close()
        return user

    def get_all(self):
        session = self._session_factory()
        users = session.query(Usuario).all()
        session.close()
        return users
