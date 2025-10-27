# ui/TelaPrincipal.py (VERSÃO FINAL E CORRIGIDA)

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
# <-- 1. VERIFIQUE SE 'Signal' ESTÁ A SER IMPORTADO
from PySide6.QtCore import Qt, Signal
from ui.Resumo import AbaResumo
from ui.receitas import AbaReceitas
from ui.despesas import TelaDespesas
from ui.limite import AbaLimites
from ui.usuario import AbaUsuario
from ui.meta import AbaMeta


class TelaPrincipal(QMainWindow):
    # --- 2. ESTE É O "RÁDIO" (SINAL) QUE ESTAVA EM FALTA ---
    logout_efetuado = Signal()

    def __init__(self, di_container):
        super().__init__()
        self.di_container = di_container
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
        self.tab_view.addTab(AbaResumo(self.di_container), "Resumo")
        self.tab_view.addTab(AbaReceitas(self.di_container), "Receitas")
        self.tab_view.addTab(TelaDespesas(self.di_container), "Despesas")
        self.tab_view.addTab(AbaLimites(), "Limites")
        aba_usuario = AbaUsuario(self.di_container)
        aba_usuario.logout_solicitado.connect(self.realizar_logout)
        self.tab_view.addTab(aba_usuario, "Usuário")

        self.tab_view.setCurrentIndex(0)

    # --- 3. ESTA FUNÇÃO USA O "RÁDIO" PARA AVISAR O main.py ---
    def realizar_logout(self):
        self.logout_efetuado.emit()
        self.close()
