# main.py (VERSÃO FINAL E CORRIGIDA)
import sys
from PySide6.QtWidgets import QApplication
from Login import TelaLogin
from TelaPrincipal import TelaPrincipal


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tela_login = None
        self.tela_principal = None
        self.mostrar_login()

    def mostrar_login(self):
        # --- MUDANÇA AQUI ---
        # Garante que a tela principal seja fechada ao fazer logout
        if self.tela_principal:
            self.tela_principal.close()

        self.tela_login = TelaLogin()
        self.tela_login.login_sucesso.connect(self.mostrar_principal)
        self.tela_login.show()

    def mostrar_principal(self):
        self.tela_principal = TelaPrincipal()
        self.tela_principal.logout_efetuado.connect(self.mostrar_login)
        self.tela_principal.show()

        # --- MUDANÇA AQUI ---
        # Agora o controlador fecha a tela de login APÓS a principal estar aberta
        if self.tela_login:
            self.tela_login.close()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
