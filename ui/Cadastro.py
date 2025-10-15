# Cadastro_PySide6.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QApplication, QScrollArea
)
from PySide6.QtCore import Qt
import sys

class TelaCadastro(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastro de Usuário")
        self.setFixedSize(500, 650)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # Layout principal com scroll (opcional para telas pequenas)
        scroll = QScrollArea(self)
        scroll.setGeometry(0, 0, 500, 650)
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # Título
        titulo = QLabel("🧾 Cadastro de Usuário")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)

        subtitulo = QLabel("Preencha seus dados pessoais e financeiros")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 13px; color: #a5a5a5;")
        layout.addWidget(subtitulo)
        layout.addSpacing(15)

        # Campos de Dados Pessoais
        self.entry_nome = QLineEdit()
        self.entry_nome.setPlaceholderText("Nome completo")
        self._estilo_campo(self.entry_nome)
        layout.addWidget(self.entry_nome)

        self.entry_data_nasc = QLineEdit()
        self.entry_data_nasc.setPlaceholderText("Data de nascimento (DD/MM/AAAA)")
        self._estilo_campo(self.entry_data_nasc)
        layout.addWidget(self.entry_data_nasc)

        self.entry_cpf = QLineEdit()
        self.entry_cpf.setPlaceholderText("CPF (somente números)")
        self._estilo_campo(self.entry_cpf)
        layout.addWidget(self.entry_cpf)

        self.entry_profissao = QLineEdit()
        self.entry_profissao.setPlaceholderText("Profissão")
        self._estilo_campo(self.entry_profissao)
        layout.addWidget(self.entry_profissao)

        self.entry_renda = QLineEdit()
        self.entry_renda.setPlaceholderText("Renda mensal (R$)")
        self._estilo_campo(self.entry_renda)
        layout.addWidget(self.entry_renda)

        # Dados de Acesso
        label_acesso = QLabel("Dados de Acesso")
        label_acesso.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label_acesso)

        self.entry_usuario = QLineEdit()
        self.entry_usuario.setPlaceholderText("Usuário")
        self._estilo_campo(self.entry_usuario)
        layout.addWidget(self.entry_usuario)

        self.entry_senha = QLineEdit()
        self.entry_senha.setPlaceholderText("Senha")
        self.entry_senha.setEchoMode(QLineEdit.Password)
        self._estilo_campo(self.entry_senha)
        layout.addWidget(self.entry_senha)

        self.entry_confirmar = QLineEdit()
        self.entry_confirmar.setPlaceholderText("Confirmar senha")
        self.entry_confirmar.setEchoMode(QLineEdit.Password)
        self._estilo_campo(self.entry_confirmar)
        layout.addWidget(self.entry_confirmar)

        # Botão Cadastrar
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setFixedHeight(40)
        self.btn_cadastrar.setStyleSheet(
            "background-color: #16a34a; color: white; font-weight: bold; font-size: 14px; border-radius: 8px;"
        )
        self.btn_cadastrar.clicked.connect(self.cadastrar_usuario)
        layout.addWidget(self.btn_cadastrar)

    def _estilo_campo(self, campo):
        campo.setStyleSheet(
            "background-color: #2c2c3c; color: white; padding: 8px; border-radius: 8px;"
        )

    def cadastrar_usuario(self):
        senha = self.entry_senha.text()
        confirmar_senha = self.entry_confirmar.text()

        if senha != confirmar_senha:
            QMessageBox.critical(self, "Erro de Cadastro", "As senhas não coincidem!")
            return

        campos = [
            self.entry_nome.text(),
            self.entry_data_nasc.text(),
            self.entry_cpf.text(),
            self.entry_profissao.text(),
            self.entry_renda.text(),
            self.entry_usuario.text(),
            self.entry_senha.text()
        ]

        if any(campo.strip() == "" for campo in campos):
            QMessageBox.warning(self, "Atenção", "Por favor, preencha todos os campos.")
            return

        QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")
        self.close()


