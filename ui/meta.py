from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import random


class ConfigurarMetaDialog(QDialog):
    """Janela de configuração da meta"""
    def __init__(self, nome_atual, valor_meta_atual, meses_atuais):
        super().__init__()
        self.setWindowTitle("Configurar Meta")
        self.setStyleSheet("background-color: #2c2c3c; color: white;")

        layout = QFormLayout(self)
        self.input_nome = QLineEdit(nome_atual)
        self.input_meta = QLineEdit(str(valor_meta_atual))
        self.input_meses = QLineEdit(str(meses_atuais))

        layout.addRow("Nome da Meta:", self.input_nome)
        layout.addRow("Valor da Meta (R$):", self.input_meta)
        layout.addRow("Número de Meses:", self.input_meses)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)

    def get_valores(self):
        """Retorna os valores inseridos pelo usuário"""
        try:
            nome = self.input_nome.text().strip() or "Meta Financeira"
            valor_meta = float(self.input_meta.text())
            meses = int(self.input_meses.text())
            if valor_meta <= 0 or meses <= 0:
                raise ValueError
            return nome, valor_meta, meses
        except ValueError:
            QMessageBox.warning(self, "Erro", "Insira valores válidos!")
            return None, None, None


class AbaMeta(QWidget):
    def __init__(self, receitas, despesas, meta_anual=20000, meses=12, nome_meta="Meta Financeira"):
        super().__init__()
        self.setWindowTitle("Painel de Meta Financeira")
        self.resize(1100, 650)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # Dados iniciais
        self.receitas = receitas
        self.despesas = despesas
        self.meta_anual = meta_anual
        self.meses = meses
        self.nome_meta = nome_meta

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Botão para configurar meta
        self.btn_config = QPushButton("Configurar Meta")
        self.btn_config.clicked.connect(self.configurar_meta)
        main_layout.addWidget(self.btn_config, alignment=Qt.AlignLeft)

        # Layout horizontal (tabela + gráfico)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # ===== TABELA =====
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Mês", "Receita (R$)", "Despesa (R$)", "Para Meta (R$)"])
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.setStyleSheet("background-color: #2c2c3c; color: white;")
        content_layout.addWidget(self.tabela, 3)

        # ===== GRÁFICO =====
        graf_layout = QVBoxLayout()
        content_layout.addLayout(graf_layout, 2)  # mais espaço para o gráfico

        # Label do nome e progresso
        self.label_nome = QLabel(self.nome_meta)
        self.label_nome.setAlignment(Qt.AlignCenter)
        self.label_nome.setStyleSheet("font-size: 18px; font-weight: bold; color: #2a9d8f;")
        graf_layout.addWidget(self.label_nome)

        self.label_total = QLabel()
        self.label_total.setAlignment(Qt.AlignCenter)
        self.label_total.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        graf_layout.addWidget(self.label_total)

        # Gráfico circular (maior agora)
        self.fig_circular = Figure(figsize=(5.5, 5.5))
        self.fig_circular.patch.set_facecolor("#1e1e2f")
        self.canvas_circular = FigureCanvas(self.fig_circular)
        graf_layout.addWidget(self.canvas_circular, alignment=Qt.AlignCenter)

        # Inicializa tabela e gráfico
        self.carregar_tabela()
        self.atualizar_grafico_circular()

    def carregar_tabela(self):
        """Preenche a tabela com receitas, despesas e valor destinado à meta"""
        self.tabela.setRowCount(self.meses)
        self.total_meta = 0

        for mes in range(1, self.meses + 1):
            receita = self.receitas.get(mes, 0)
            despesa = self.despesas.get(mes, 0)
            para_meta = max(receita - despesa, 0)
            self.total_meta += para_meta

            self.tabela.setItem(mes - 1, 0, QTableWidgetItem(f"Mês {mes}"))
            self.tabela.setItem(mes - 1, 1, QTableWidgetItem(f"R$ {receita:.2f}"))
            self.tabela.setItem(mes - 1, 2, QTableWidgetItem(f"R$ {despesa:.2f}"))
            self.tabela.setItem(mes - 1, 3, QTableWidgetItem(f"R$ {para_meta:.2f}"))

    def atualizar_grafico_circular(self):
        """Atualiza o gráfico circular com o progresso da meta"""
        progresso = min(self.total_meta / self.meta_anual, 1)
        falta = max(1 - progresso, 0)

        self.label_nome.setText(self.nome_meta)
        self.label_total.setText(
            f"Meta: R$ {self.meta_anual:.2f}\n"
            f"Acumulado: R$ {self.total_meta:.2f} ({progresso*100:.1f}%)"
        )

        self.fig_circular.clear()
        ax = self.fig_circular.add_subplot(111)
        ax.pie(
            [progresso, falta],
            labels=[f"Alcançado {progresso*100:.1f}%", f"Falta {falta*100:.1f}%"],
            colors=["#2a9d8f", "#8d99ae"],
            startangle=90,
            textprops={'color': 'white', 'fontsize': 12},
            wedgeprops={'linewidth': 1, 'edgecolor': '#1e1e2f'}
        )
        ax.set_title("Progresso da Meta", color="white", fontsize=14)
        self.canvas_circular.draw()

    def configurar_meta(self):
        """Abre janela de configuração da meta"""
        dialog = ConfigurarMetaDialog(self.nome_meta, self.meta_anual, self.meses)
        if dialog.exec():
            novo_nome, novo_valor, novos_meses = dialog.get_valores()
            if novo_nome and novo_valor and novos_meses:
                self.nome_meta = novo_nome
                self.meta_anual = novo_valor
                self.meses = novos_meses
                self.carregar_tabela()
                self.atualizar_grafico_circular()

