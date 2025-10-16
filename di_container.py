from repositories.transacao_repository import TransacaoRepository
from repositories.usuario_repository import UsuarioRepository

class DIContainer:
    def __init__(self):
        # Create shared instances
        self.transacao_repository = TransacaoRepository()
        self.usuario_repository = UsuarioRepository()