# ui/Usuario.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QScrollArea, QFormLayout
)
from PySide6.QtCore import Qt, Signal


class AbaUsuario(QWidget):
    # Signal para notificar a TelaPrincipal que o logout foi acionado
    logout_solicitado = Signal()

    def __init__(self, di_container, parent=None):
        super().__init__(parent)
        self.di_container = di_container
        self.setStyleSheet("background-color: transparent; color: white;")

        self.usuario_ativo = di_container.usuario_ativo

        # --- Dados de exemplo (carregue os dados do utilizador logado) ---
        self.dados_usuario = {
            "nome": "Pessoa",
            "data_nasc": "15/10/1990",
            "cpf": "123.456.789-00",
            "profissao": "Desenvolvedora Python",
            "renda": "5000.00",
            "usuario": "admin"
        }
        # -----------------------------------------------------------------

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # Título
        titulo = QLabel("Perfil do Usuário")
        titulo.setStyleSheet(
            "font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(titulo)

        # Usando QFormLayout para um formulário bem alinhado
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Campos de Dados Pessoais
        self.entry_nome = QLineEdit(self.usuario_ativo.nome)
        self._estilo_campo(self.entry_nome)
        form_layout.addRow("Nome Completo:", self.entry_nome)

        self.entry_data_nasc = QLineEdit(self.usuario_ativo.data_nasc)
        self._estilo_campo(self.entry_data_nasc)
        form_layout.addRow("Data de Nascimento:", self.entry_data_nasc)

        self.entry_cpf = QLineEdit(self.usuario_ativo.cpf)
        self._estilo_campo(self.entry_cpf)
        self.entry_cpf.setReadOnly(True)  # CPF geralmente não é editável
        self.entry_cpf.setStyleSheet(
            self.entry_cpf.styleSheet() + "background-color: #4a4a5a;")
        form_layout.addRow("CPF:", self.entry_cpf)

        self.entry_profissao = QLineEdit(self.usuario_ativo.profissao)
        self._estilo_campo(self.entry_profissao)
        form_layout.addRow("Profissão:", self.entry_profissao)

        self.entry_renda = QLineEdit(self.usuario_ativo.renda_mensal)
        self._estilo_campo(self.entry_renda)
        form_layout.addRow("Renda Mensal (R$):", self.entry_renda)

        # Campo de usuário (não editável)
        self.entry_usuario = QLineEdit(self.usuario_ativo.user)
        self._estilo_campo(self.entry_usuario)
        self.entry_usuario.setReadOnly(True)
        self.entry_usuario.setStyleSheet(
            self.entry_usuario.styleSheet() + "background-color: #4a4a5a;")
        form_layout.addRow("Usuário:", self.entry_usuario)

        main_layout.addLayout(form_layout)
        main_layout.addStretch()  # Empurra os botões para baixo

        # --- Botões ---
        self.btn_salvar = QPushButton("Salvar Alterações")
        self.btn_salvar.setFixedHeight(40)
        self.btn_salvar.setStyleSheet("""
            QPushButton {
                background-color: #16a34a; color: white; font-weight: bold;
                font-size: 14px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #15803d; }
        """)
        self.btn_salvar.clicked.connect(self.salvar_alteracoes)
        main_layout.addWidget(self.btn_salvar)

        self.btn_logout = QPushButton("Logout (Sair)")
        self.btn_logout.setFixedHeight(40)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e63946; color: white; font-weight: bold;
                font-size: 14px; border-radius: 8px; margin-top: 10px;
            }
            QPushButton:hover { background-color: #d62828; }
        """)
        # Conecta o clique do botão à emissão do nosso sinal customizado
        self.btn_logout.clicked.connect(self.logout_solicitado.emit)
        main_layout.addWidget(self.btn_logout)

    def _estilo_campo(self, campo):
        campo.setStyleSheet(
            "background-color: #2c2c3c; color: white; padding: 10px; border-radius: 8px;"
        )

    def salvar_alteracoes(self):
        novo_nome = self.entry_nome.text().strip()
        nova_profissao = self.entry_profissao.text().strip()
        nova_datanasc = self.entry_data_nasc.text()
        nova_renda = self.entry_renda.text().strip()

        user_id = self.di_container.usuario_ativo.id

        user_atualizado = self.di_container.usuario_repository.atualizar_usuario(
            user_id,
            nome=novo_nome,
            profissao=nova_profissao,
            data_nasc=nova_datanasc,
            renda_mensal=nova_renda
        )

        if user_atualizado:
            self.di_container.usuario_ativo = user_atualizado
            QMessageBox.information(self, "Sucesso", "Informações atualizadas com sucesso!")
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível atualizar o usuário.")
