# Resumo.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from models.despesa import Despesa
from models.receita import Receita


class AbaResumo(QWidget):
    def __init__(self, di_container, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        # Layout principal da aba
        main_layout = QHBoxLayout(self)

        transacoes = di_container.transacao_repository.get_current_month_transactions(
            di_container.usuario_ativo.id)
        receitas = [t for t in transacoes if isinstance(t, Receita)]
        despesas = [t for t in transacoes if isinstance(t, Despesa)]
        total_receitas = sum(r.get_valor_com_sinal() for r in receitas)
        total_despesas = sum(d.get_valor_com_sinal() for d in despesas)

        saldo_restante = total_receitas + total_despesas

        if saldo_restante < 0:
            saldo_restante = 0

        # Frame para o Gráfico (Esquerda)
        # TODO: Fazer algo quando a tela não tiver receitas nem despesas.
        if total_despesas > 0 or total_receitas > 0:
            chart_frame = QFrame()
            chart_layout = QVBoxLayout(chart_frame)
            # O '1' faz com que ocupe metade do espaço
            main_layout.addWidget(chart_frame, 1)

            # --- Criação do Gráfico Circular (Donut Chart) ---
            figura = Figure(figsize=(4, 4), dpi=100)
            figura.patch.set_facecolor("#1e1e2f")  # Cor de fundo
            ax = figura.add_subplot(111)

            valores = [abs(total_despesas), saldo_restante]
            # Vermelho para despesa, verde para saldo
            cores = ['#e63946', '#2a9d8f']

            ax.pie(valores, labels=None, colors=cores, autopct=None, startangle=90,
                   wedgeprops=dict(width=0.4, edgecolor='#1e1e2f'))

            porcentagem_gasta = (abs(total_despesas) / total_receitas) * 100
            ax.text(0, 0, f'{porcentagem_gasta:.1f}%\nGasto', ha='center', va='center',
                    fontsize=24, color='white', weight='bold')

            canvas = FigureCanvas(figura)
            chart_layout.addWidget(canvas)

        else:
            # Se não houver transações, mostra uma mensagem
            placeholder_frame = QFrame()
            placeholder_layout = QVBoxLayout(placeholder_frame)
            placeholder_layout.setAlignment(Qt.AlignCenter)

            label_placeholder = QLabel(
                "Sem transações este mês. 💸\n\nAdicione receitas ou despesas para ver o resumo.")
            label_placeholder.setAlignment(Qt.AlignCenter)
            label_placeholder.setStyleSheet("font-size: 16px; color: #a5a5a5;")

            placeholder_layout.addWidget(label_placeholder)
            # Adiciona no lugar do gráfico
            main_layout.addWidget(placeholder_frame, 1)

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

        label_renda = QLabel(f"Total de Receitas: R$ {total_receitas:,.2f}")
        label_renda.setStyleSheet("font-size: 16px;")
        details_layout.addWidget(label_renda)

        label_despesas = QLabel(
            f"Total de Despesas: R$ {abs(total_despesas):,.2f}")
        label_despesas.setStyleSheet("font-size: 16px;")
        details_layout.addWidget(label_despesas)

        label_saldo = QLabel(f"Saldo Restante: R$ {saldo_restante:,.2f}")
        label_saldo.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2a9d8f;")
        details_layout.addWidget(label_saldo)
