from database.db_session import SessionLocal
from models.usuario import Usuario
from repositories.auth_utils import hash_password, verify_password
from sqlalchemy.exc import IntegrityError


class UsuarioRepository:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def add(self, user: Usuario):
        session = self._session_factory()
        session.add(user)
        session.commit()
        session.close()
    
    def verificar_credenciais(self, usuario: str, senha: str):
        session = self._session_factory()
        user = session.query(Usuario).filter(Usuario.user == usuario).first()
        if user and verify_password(senha, user.senha):
            return user
        return None
    
    def criar_usuario(self, nome, data_nasc, cpf, profissao, renda, usuario, senha):
        novo_usuario = Usuario(
            nome=nome,
            data_nasc=data_nasc,
            cpf=cpf,
            profissao=profissao,
            renda_mensal=renda,
            user=usuario,
            senha=hash_password(senha)
        )

        try:
            self.add(novo_usuario)
            return True
        except IntegrityError:
            self.db.rollback()
            return False
