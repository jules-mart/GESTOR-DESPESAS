from repositories.limite_repository import LimiteRepository
from repositories.transacao_repository import TransacaoRepository
from repositories.usuario_repository import UsuarioRepository

class DIContainer:
    def __init__(self):
        self.transacao_repository = TransacaoRepository()
        self.usuario_repository = UsuarioRepository()
        self.limite_repository = LimiteRepository()

        self.usuario_ativo = None