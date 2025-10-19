# ui/TelaPrincipal.py (VERSÃO FINAL E CORRIGIDA)

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
# <-- 1. VERIFIQUE SE 'Signal' ESTÁ A SER IMPORTADO
from PySide6.QtCore import Qt, Signal
from Resumo import AbaResumo
from receitas import AbaReceitas
from despesas import TelaDespesas
from limite import AbaLimites
from usuario import AbaUsuario
from meta import AbaMeta


class TelaPrincipal(QMainWindow):
    # --- 2. ESTE É O "RÁDIO" (SINAL) QUE ESTAVA EM FALTA ---
    logout_efetuado = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel Financeiro Principal")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        self.tab_view = QTabWidget()
        self.tab_view.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #2c2c3c; color: white; padding: 10px; border-radius: 5px;
            }
            QTabBar::tab:selected { background: #3b82f6; }
        """)
        layout_principal.addWidget(self.tab_view)

        # --- Adiciona as abas ---
        self.tab_view.addTab(AbaResumo(), "Resumo")
        self.tab_view.addTab(AbaReceitas(), "Receitas")
        self.tab_view.addTab(TelaDespesas(), "Despesas")
        self.tab_view.addTab(AbaLimites(), "Limites")

        receitas_exemplo = {i: 5000 for i in range(1, 13)}
        despesas_exemplo = {i: 3000 for i in range(1, 13)}
        self.tab_view.addTab(
            AbaMeta(receitas=receitas_exemplo, despesas=despesas_exemplo), "Metas")

        aba_usuario = AbaUsuario()
        aba_usuario.logout_solicitado.connect(self.realizar_logout)
        self.tab_view.addTab(aba_usuario, "Usuário")

        self.tab_view.setCurrentIndex(0)

    # --- 3. ESTA FUNÇÃO USA O "RÁDIO" PARA AVISAR O main.py ---
    def realizar_logout(self):
        self.logout_efetuado.emit()
        self.close()
