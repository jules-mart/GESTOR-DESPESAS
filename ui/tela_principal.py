# ui/TelaPrincipal.py (VERSÃO FINAL E CORRIGIDA)

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
# <-- 1. VERIFIQUE SE 'Signal' ESTÁ A SER IMPORTADO
from PySide6.QtCore import Qt, Signal
from ui.resumo import AbaResumo
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

        self.aba_resumo = AbaResumo(self.di_container)
        self.aba_receitas = AbaReceitas(self.di_container)
        self.aba_despesas = TelaDespesas(self.di_container)
        self.aba_limites = AbaLimites(self.di_container)



        # --- Adiciona as abas ---
        
        self.tab_view.addTab(self.aba_resumo, "Resumo")
        self.tab_view.addTab(self.aba_receitas, "Receitas")
        self.tab_view.addTab(self.aba_despesas, "Despesas")
        self.tab_view.addTab(self.aba_limites, "Limites")

        self.aba_receitas.receita_adicionada.connect(self.atualizar_resumo)
        self.aba_despesas.despesa_adicionada.connect(self.atualizar_resumo)
        self.aba_despesas.despesa_adicionada.connect(self.atualizar_limites)


        aba_usuario = AbaUsuario(self.di_container)
        aba_usuario.logout_solicitado.connect(self.realizar_logout)
        self.tab_view.addTab(aba_usuario, "Usuário")

        self.tab_view.setCurrentIndex(0)

    def realizar_logout(self):
        self.di_container.usuario_ativo = None
        self.logout_efetuado.emit()
        self.close()

    def atualizar_resumo(self):
        self.tab_view.removeTab(0)
        self.aba_resumo = AbaResumo(self.di_container)
        self.tab_view.insertTab(0, self.aba_resumo, "Resumo")

    def atualizar_limites(self):
        self.tab_view.removeTab(0)
        self.aba_limites = AbaLimites(self.di_container)
        self.tab_view.insertTab(0, self.aba_limites, "Limites")
