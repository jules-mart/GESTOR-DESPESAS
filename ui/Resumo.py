# Resumo.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import ConnectionPatch
import numpy as np
from models.despesa import Despesa
from models.receita import Receita


class InteractiveDonutChart(FigureCanvas):
    def __init__(self, total_receitas, total_despesas, saldo_restante, parent=None):
        self.fig = Figure(figsize=(5, 5), dpi=100, facecolor='#1e1e2f')
        super().__init__(self.fig)
        
        self.total_receitas = total_receitas
        self.total_despesas = abs(total_despesas)
        self.saldo_restante = saldo_restante
        self.parent = parent
        
        self.setup_chart()
        self.animate_chart()
        
    def setup_chart(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e1e2f')
        
        self.ax.axis('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.colors = ['#e63946', '#2a9d8f', '#457b9d']
        self.labels = ['Despesas', 'Saldo Restante']
        
        self.values = [self.total_despesas, self.saldo_restante]
        
        self.wedges, _ = self.ax.pie(
            self.values, 
            colors=self.colors[:2], 
            startangle=90,
            wedgeprops=dict(width=0.5, edgecolor='#1e1e2f', linewidth=2),
            labels=self.labels,
            labeldistance=1.1,
            textprops=dict(color='white', fontsize=10)
        )
        
        porcentagem_gasta = (self.total_despesas / self.total_receitas) * 100 if self.total_receitas > 0 else 0
        self.center_text = self.ax.text(
            0, 0, f'{porcentagem_gasta:.1f}%\nGasto', 
            ha='center', va='center', 
            fontsize=20, color='white', weight='bold',
            fontfamily='Arial'
        )
        
        self.value_labels = []
        for i, (wedge, value) in enumerate(zip(self.wedges, self.values)):
            angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            x = 0.7 * np.cos(np.radians(angle))
            y = 0.7 * np.sin(np.radians(angle))
            
            label = self.ax.text(
                x, y, f'R$ {value:,.2f}',
                ha='center', va='center',
                fontsize=9, color='white', weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors[i], alpha=0.8)
            )
            self.value_labels.append(label)

        self.hovered_wedge = None
        self.cid = self.mpl_connect('motion_notify_event', self.on_hover)
        
    def on_hover(self, event):
        if event.inaxes == self.ax:
            for i, wedge in enumerate(self.wedges):
                if wedge.contains_point([event.x, event.y]):
                    if self.hovered_wedge != wedge:
                        self.highlight_wedge(wedge, i)
                    return
            self.remove_highlight()
    
    def highlight_wedge(self, wedge, index):
        self.remove_highlight()
        wedge.set_alpha(0.8)
        wedge.set_linewidth(3)
        wedge.set_edgecolor('white')
        self.hovered_wedge = wedge
        self.draw()
    
    def remove_highlight(self):
        if self.hovered_wedge:
            self.hovered_wedge.set_alpha(1.0)
            self.hovered_wedge.set_linewidth(2)
            self.hovered_wedge.set_edgecolor('#1e1e2f')
            self.hovered_wedge = None
            self.draw()
    
    def animate_chart(self):
        self.animated_values = [0, 0]
        self.animation_step = 0
        self.animation_steps = 30
        
        def update_animation():
            if self.animation_step < self.animation_steps:
                progress = (self.animation_step + 1) / self.animation_steps
                self.animated_values = [v * progress for v in self.values]
                
                for wedge, new_val in zip(self.wedges, self.animated_values):
                    wedge.set_width(0.5)
                
                porcentagem_gasta = (self.animated_values[0] / self.total_receitas) * 100 if self.total_receitas > 0 else 0
                self.center_text.set_text(f'{porcentagem_gasta:.1f}%\nGasto')
                
                for label, new_val in zip(self.value_labels, self.animated_values):
                    label.set_text(f'R$ {new_val:,.2f}')
                
                self.animation_step += 1
                self.draw()
            else:
                self.animation_timer.stop()
        
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(update_animation)
        self.animation_timer.start(30)


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
        if total_despesas > 0 or total_receitas > 0:
            chart_frame = QFrame()
            chart_frame.setStyleSheet("background-color: #1e1e2f; border-radius: 15px;")
            chart_layout = QVBoxLayout(chart_frame)
            chart_layout.setContentsMargins(10, 10, 10, 10)
            main_layout.addWidget(chart_frame, 1)

            # Create interactive chart
            self.chart = InteractiveDonutChart(total_receitas, total_despesas, saldo_restante)
            chart_layout.addWidget(self.chart)

        else:
            # Se não houver transações, mostra uma mensagem
            placeholder_frame = QFrame()
            placeholder_frame.setStyleSheet("background-color: #1e1e2f; border-radius: 15px;")
            placeholder_layout = QVBoxLayout(placeholder_frame)
            placeholder_layout.setAlignment(Qt.AlignCenter)

            label_placeholder = QLabel(
                "Sem transações este mês. 💸\n\nAdicione receitas ou despesas para ver o resumo.")
            label_placeholder.setAlignment(Qt.AlignCenter)
            label_placeholder.setStyleSheet("font-size: 16px; color: #a5a5a5; padding: 40px;")

            placeholder_layout.addWidget(label_placeholder)
            main_layout.addWidget(placeholder_frame, 1)

        # --- Frame para os Detalhes em Texto (Direita) ---
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d44;
                border-radius: 12px;
                border: 2px solid #3a3a5c;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
                border: none;
            }
        """)
        details_layout = QVBoxLayout(details_frame)
        details_layout.setAlignment(Qt.AlignVCenter)
        details_layout.setSpacing(8)
        details_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(details_frame, 1)

        label_titulo_detalhes = QLabel("📊 Resumo do Mês")
        label_titulo_detalhes.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #7e57c2; margin-bottom: 10px;")
        details_layout.addWidget(label_titulo_detalhes)

        # Receitas card
        receita_frame = QFrame()
        receita_frame.setStyleSheet("""
            QFrame {
                background-color: #26a69a20;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        receita_layout = QHBoxLayout(receita_frame)
        receita_icon = QLabel("💰")
        receita_icon.setStyleSheet("font-size: 18px;")
        receita_text = QLabel(f"Receitas: R$ {total_receitas:,.2f}")
        receita_text.setStyleSheet("font-size: 14px; font-weight: bold;")
        receita_layout.addWidget(receita_icon)
        receita_layout.addWidget(receita_text)
        receita_layout.addStretch()
        details_layout.addWidget(receita_frame)

        # Despesas card
        despesa_frame = QFrame()
        despesa_frame.setStyleSheet("""
            QFrame {
                background-color: #ef535020;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        despesa_layout = QHBoxLayout(despesa_frame)
        despesa_icon = QLabel("💸")
        despesa_icon.setStyleSheet("font-size: 18px;")
        despesa_text = QLabel(f"Despesas: R$ {abs(total_despesas):,.2f}")
        despesa_text.setStyleSheet("font-size: 14px; font-weight: bold;")
        despesa_layout.addWidget(despesa_icon)
        despesa_layout.addWidget(despesa_text)
        despesa_layout.addStretch()
        details_layout.addWidget(despesa_frame)

        # Saldo card - different color from receitas
        saldo_frame = QFrame()
        saldo_color = "#42a5f5" if saldo_restante >= 0 else "#ef5350"
        saldo_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {saldo_color}20;
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        saldo_layout = QHBoxLayout(saldo_frame)
        saldo_icon = QLabel("⚖️")
        saldo_icon.setStyleSheet("font-size: 20px;")
        saldo_text = QLabel(f"Saldo: R$ {saldo_restante:,.2f}")
        saldo_text.setStyleSheet("font-size: 16px; font-weight: bold;")
        saldo_layout.addWidget(saldo_icon)
        saldo_layout.addWidget(saldo_text)
        saldo_layout.addStretch()
        details_layout.addWidget(saldo_frame)

        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        
        if total_receitas > 0:
            porcentagem_gasta = (abs(total_despesas) / total_receitas) * 100
            economia_percentual = 100 - porcentagem_gasta
            
            stats_label = QLabel("Estatísticas:")
            stats_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
            stats_layout.addWidget(stats_label)
            
            stats_text = QLabel(
                f"• {porcentagem_gasta:.1f}% da renda gasta\n"
                f"• {economia_percentual:.1f}% da renda economizada\n"
                f"• {len(receitas)} receita(s)\n"
                f"• {len(despesas)} despesa(s)"
            )
            stats_text.setStyleSheet("font-size: 12px; color: #cccccc; line-height: 1.5;")
            stats_layout.addWidget(stats_text)
        
        details_layout.addWidget(stats_frame)
        details_layout.addStretch()