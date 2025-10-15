# TelaPrincipal.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from PySide6.QtCore import Qt
from Resumo import AbaResumo  # Importa a AbaResumo convertida
# Importa a tela de despesas que já usa PySide6
from despesas import TelaDespesas
from limite import AbaLimites
from receitas import AbaReceitas


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel Financeiro Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # Widget central para conter o layout
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        # --- Cria o sistema de Abas (QTabWidget) ---
        self.tab_view = QTabWidget()
        self.tab_view.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #2c2c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #3b82f6;
            }
        """)
        layout_principal.addWidget(self.tab_view)

        # --- Adiciona as abas ---
        # Aba de Resumo
        aba_resumo = AbaResumo()
        self.tab_view.addTab(aba_resumo, "Resumo")

        # Aba de Despesas
        aba_despesas = TelaDespesas()
        self.tab_view.addTab(aba_despesas, "Despesas")

        # Aba de Limites (Exemplo)
        aba_limites = AbaLimites()
        self.tab_view.addTab(aba_limites, "Limites")

        # Aba de Receitas (Exemplo)
        aba_receitas = AbaReceitas()
        self.tab_view.addTab(aba_receitas, "Receitas")

        # Aba de Metas (Exemplo)
        aba_metas = QWidget()
        layout_metas = QVBoxLayout(aba_metas)
        label_metas = QLabel("Aqui ficará o acompanhamento de metas.")
        label_metas.setAlignment(Qt.AlignCenter)
        label_metas.setStyleSheet("font-size: 20px;")
        layout_metas.addWidget(label_metas)
        self.tab_view.addTab(aba_metas, "Metas")

        # Define a aba inicial que será exibida
        self.tab_view.setCurrentIndex(0)
