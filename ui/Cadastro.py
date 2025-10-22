# ui/Cadastro.py (CORRIGIDO)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt


class TelaCadastro(QWidget):
    def __init__(self, usuario_repository, parent=None):
        super().__init__(parent)
        self.usuario_repository = usuario_repository
        self.setWindowTitle("Cadastro de Usuário")
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        # Aumentei o tamanho mínimo para garantir que tudo caiba confortavelmente
        self.setMinimumSize(500, 650)

        # --- CORREÇÃO: Layout principal para a própria janela ---
        main_layout = QVBoxLayout(self)
        # Remove margens extras da janela
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Área de scroll para conter o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # Remove a borda padrão da QScrollArea para melhor estética
        scroll.setStyleSheet("QScrollArea { border: none; }")
        # Adiciona a scroll area ao layout principal
        main_layout.addWidget(scroll)

        # Container para os widgets dentro da área de scroll
        container = QWidget()
        scroll.setWidget(container)

        # Layout para o conteúdo do formulário
        layout_formulario = QVBoxLayout(container)
        layout_formulario.setAlignment(Qt.AlignTop)
        layout_formulario.setContentsMargins(30, 30, 30, 30)
        layout_formulario.setSpacing(10)

        # Título
        titulo = QLabel("🧾 Cadastro de Usuário")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout_formulario.addWidget(titulo)

        subtitulo = QLabel("Preencha seus dados pessoais e financeiros")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 13px; color: #a5a5a5;")
        layout_formulario.addWidget(subtitulo)
        layout_formulario.addSpacing(15)

        # Campos de Dados Pessoais
        self.entry_nome = QLineEdit()
        self.entry_nome.setPlaceholderText("Nome completo")
        self._estilo_campo(self.entry_nome)
        layout_formulario.addWidget(self.entry_nome)

        self.entry_data_nasc = QLineEdit()
        self.entry_data_nasc.setPlaceholderText(
            "Data de nascimento (DD/MM/AAAA)")
        self._estilo_campo(self.entry_data_nasc)
        layout_formulario.addWidget(self.entry_data_nasc)

        self.entry_cpf = QLineEdit()
        self.entry_cpf.setPlaceholderText("CPF (somente números)")
        self._estilo_campo(self.entry_cpf)
        layout_formulario.addWidget(self.entry_cpf)

        self.entry_profissao = QLineEdit()
        self.entry_profissao.setPlaceholderText("Profissão")
        self._estilo_campo(self.entry_profissao)
        layout_formulario.addWidget(self.entry_profissao)

        self.entry_renda = QLineEdit()
        self.entry_renda.setPlaceholderText("Renda mensal (R$)")
        self._estilo_campo(self.entry_renda)
        layout_formulario.addWidget(self.entry_renda)

        # Dados de Acesso
        label_acesso = QLabel("Dados de Acesso")
        label_acesso.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout_formulario.addWidget(label_acesso)

        self.entry_usuario = QLineEdit()
        self.entry_usuario.setPlaceholderText("Usuário")
        self._estilo_campo(self.entry_usuario)
        layout_formulario.addWidget(self.entry_usuario)

        self.entry_senha = QLineEdit()
        self.entry_senha.setPlaceholderText("Senha")
        self.entry_senha.setEchoMode(QLineEdit.Password)
        self._estilo_campo(self.entry_senha)
        layout_formulario.addWidget(self.entry_senha)

        self.entry_confirmar = QLineEdit()
        self.entry_confirmar.setPlaceholderText("Confirmar senha")
        self.entry_confirmar.setEchoMode(QLineEdit.Password)
        self._estilo_campo(self.entry_confirmar)
        layout_formulario.addWidget(self.entry_confirmar)
        layout_formulario.addSpacing(15)

        # Botão Cadastrar
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setFixedHeight(40)
        self.btn_cadastrar.setStyleSheet(
            "background-color: #16a34a; color: white; font-weight: bold; font-size: 14px; border-radius: 8px;"
        )
        self.btn_cadastrar.clicked.connect(self.cadastrar_usuario)
        layout_formulario.addWidget(self.btn_cadastrar)

    def _estilo_campo(self, campo):
        campo.setStyleSheet(
            "background-color: #2c2c3c; color: white; padding: 10px; border-radius: 8px;"
        )

    def cadastrar_usuario(self):
        senha = self.entry_senha.text()
        confirmar_senha = self.entry_confirmar.text()

        if senha != confirmar_senha:
            QMessageBox.critical(self, "Erro de Cadastro",
                                 "As senhas não coincidem!")
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
            QMessageBox.warning(
                self, "Atenção", "Por favor, preencha todos os campos.")
            return

        sucesso = self.usuario_repository.criar_usuario(
            nome=self.entry_nome.text(),
            data_nasc=self.entry_data_nasc.text(),
            cpf=self.entry_cpf.text(),
            profissao=self.entry_profissao.text(),
            renda=self.entry_renda.text(),
            usuario=self.entry_usuario.text(),
            senha=senha
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")
            self.close()
        else:
            QMessageBox.critical(self, "Erro", "Usuário já existe!")
