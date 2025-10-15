# ui/Login.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Signal  # Importa a classe Signal
from Cadastro import TelaCadastro


class TelaLogin(QWidget):
    # --- 1. ESTE É O "RÁDIO" PARA COMUNICAÇÃO ---
    login_sucesso = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema Financeiro")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        self.tela_cadastro = None

        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout_principal)

        # (Toda a sua interface de Título, campos de texto e botões continua aqui)
        # Título
        self.label_titulo = QLabel("Acesso ao Sistema")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout_principal.addWidget(self.label_titulo)
        layout_principal.addSpacing(10)

        # Entrada Usuário
        self.entry_usuario = QLineEdit()
        self.entry_usuario.setPlaceholderText("Usuário")
        self.entry_usuario.setStyleSheet(
            "background-color: #2c2c3c; color: white; padding: 8px; border-radius: 8px;"
        )
        layout_principal.addWidget(self.entry_usuario)
        layout_principal.addSpacing(10)

        # Entrada Senha
        self.entry_senha = QLineEdit()
        self.entry_senha.setPlaceholderText("Senha")
        self.entry_senha.setEchoMode(QLineEdit.Password)
        self.entry_senha.setStyleSheet(
            "background-color: #2c2c3c; color: white; padding: 8px; border-radius: 8px;"
        )
        layout_principal.addWidget(self.entry_senha)
        layout_principal.addSpacing(20)

        # Botão Login
        self.btn_login = QPushButton("Entrar")
        self.btn_login.setStyleSheet(
            "background-color: #3b82f6; color: white; font-weight: bold; font-size: 14px; border-radius: 8px;"
        )
        self.btn_login.setFixedHeight(40)
        self.btn_login.clicked.connect(self.verificar_login)
        layout_principal.addWidget(self.btn_login)
        layout_principal.addSpacing(10)

        # Botão Cadastro
        self.btn_cadastro = QPushButton("Cadastrar")
        self.btn_cadastro.setStyleSheet(
            "background-color: #16a34a; color: white; font-weight: bold; font-size: 14px; border-radius: 8px;"
        )
        self.btn_cadastro.setFixedHeight(40)
        self.btn_cadastro.clicked.connect(self.abrir_cadastro)
        layout_principal.addWidget(self.btn_cadastro)

    def verificar_login(self):
        usuario = self.entry_usuario.text()
        senha = self.entry_senha.text()

        if usuario == "admin" and senha == "1234":
            # --- 2. AQUI AVISAMOS O CONTROLADOR E SAÍMOS DE CENA ---
            self.login_sucesso.emit()
        else:
            QMessageBox.critical(self, "Erro", "Usuário ou senha incorretos!")

    def abrir_cadastro(self):
        if not self.tela_cadastro or not self.tela_cadastro.isVisible():
            self.tela_cadastro = TelaCadastro()
            self.tela_cadastro.show()
