# Resumo.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AbaResumo(QWidget):
    def __init__(self, di_container, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        # Layout principal da aba
        main_layout = QHBoxLayout(self)

        # --- DADOS DE EXEMPLO (substitua pela sua lógica real) ---
        renda_mensal = 5000.00
        despesas_totais = 3250.50
        saldo_restante = renda_mensal - despesas_totais

        # Frame para o Gráfico (Esquerda)
        chart_frame = QFrame()
        chart_layout = QVBoxLayout(chart_frame)
        # O '1' faz com que ocupe metade do espaço
        main_layout.addWidget(chart_frame, 1)

        # --- Criação do Gráfico Circular (Donut Chart) ---
        figura = Figure(figsize=(4, 4), dpi=100)
        figura.patch.set_facecolor("#1e1e2f")  # Cor de fundo
        ax = figura.add_subplot(111)

        valores = [despesas_totais, saldo_restante]
        # Vermelho para despesa, verde para saldo
        cores = ['#e63946', '#2a9d8f']

        ax.pie(valores, labels=None, colors=cores, autopct=None, startangle=90,
               wedgeprops=dict(width=0.4, edgecolor='#1e1e2f'))

        porcentagem_gasta = (despesas_totais / renda_mensal) * 100
        ax.text(0, 0, f'{porcentagem_gasta:.1f}%\nGasto', ha='center', va='center',
                fontsize=24, color='white', weight='bold')

        canvas = FigureCanvas(figura)
        chart_layout.addWidget(canvas)

        # --- Frame para os Detalhes em Texto (Direita) ---
        details_frame = QFrame()
        details_layout = QVBoxLayout(details_frame)
        # Alinha verticalmente ao centro
        details_layout.setAlignment(Qt.AlignVCenter)
        # O '1' faz com que ocupe a outra metade
        main_layout.addWidget(details_frame, 1)

        label_titulo_detalhes = QLabel("Resumo do Mês")
        label_titulo_detalhes.setStyleSheet(
            "font-size: 22px; font-weight: bold;")
        details_layout.addWidget(label_titulo_detalhes)

        label_renda = QLabel(f"Renda Mensal: R$ {renda_mensal:,.2f}")
        label_renda.setStyleSheet("font-size: 16px;")
        details_layout.addWidget(label_renda)

        label_despesas = QLabel(
            f"Total de Despesas: R$ {despesas_totais:,.2f}")
        label_despesas.setStyleSheet("font-size: 16px;")
        details_layout.addWidget(label_despesas)

        label_saldo = QLabel(f"Saldo Restante: R$ {saldo_restante:,.2f}")
        label_saldo.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2a9d8f;")
        details_layout.addWidget(label_saldo)
