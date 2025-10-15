# ui/Limites.py (COM GRÁFICOS CIRCULARES)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDialog, QFormLayout, QDialogButtonBox,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AbaLimites(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent; color: white;")

        # --- Dados de exemplo (substitua pela sua lógica de dados real) ---
        self.gastos_atuais = {
            "Alimentação": 350.75,
            "Transporte": 120.00,
            "Lazer": 480.50,
            "Moradia": 0
        }
        self.limites = {
            "Alimentação": 500.00,
            "Transporte": 150.00,
            "Lazer": 400.00,
        }
        # --------------------------------------------------------------------

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # --- Título e Botão ---
        header_layout = QHBoxLayout()
        titulo = QLabel("Limites de Gastos")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")
        header_layout.addWidget(titulo)
        header_layout.addStretch()

        self.btn_adicionar = QPushButton("＋ Adicionar Limite")
        self.btn_adicionar.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; font-weight: bold;
                font-size: 14px; padding: 8px 16px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_adicionar.clicked.connect(self.abrir_dialogo_limite)
        header_layout.addWidget(self.btn_adicionar)
        main_layout.addLayout(header_layout)

        # --- Área de Scroll para a lista de limites ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        main_layout.addWidget(scroll_area)

        container = QWidget()
        scroll_area.setWidget(container)
        self.limites_layout = QVBoxLayout(container)
        self.limites_layout.setAlignment(Qt.AlignTop)

        self.atualizar_lista_limites()

    def atualizar_lista_limites(self):
        while self.limites_layout.count():
            child = self.limites_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for categoria, valor_limite in self.limites.items():
            gasto_categoria = self.gastos_atuais.get(categoria, 0)
            limite_widget = LimiteWidget(
                categoria, gasto_categoria, valor_limite)
            self.limites_layout.addWidget(limite_widget)

    def abrir_dialogo_limite(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Definir Limite")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")

        form_layout = QFormLayout(dialog)

        combo_categoria = QComboBox()
        categorias_disponiveis = [
            c for c in self.gastos_atuais.keys() if c not in self.limites]
        combo_categoria.addItems(categorias_disponiveis)
        form_layout.addRow("Categoria:", combo_categoria)

        input_valor = QLineEdit()
        input_valor.setPlaceholderText("Ex: 500.00")
        form_layout.addRow("Valor do Limite (R$):", input_valor)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form_layout.addWidget(buttons)

        if dialog.exec():
            categoria = combo_categoria.currentText()
            try:
                valor = float(input_valor.text().replace(",", "."))
                self.limites[categoria] = valor
                self.atualizar_lista_limites()
            except ValueError:
                pass

# --- Widget customizado com o Gráfico Circular ---


class LimiteWidget(QFrame):
    def __init__(self, categoria, gasto, limite, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c2c3c;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        self.setContentsMargins(0, 0, 0, 10)

        # Layout principal (horizontal: gráfico à esquerda, textos à direita)
        main_layout = QHBoxLayout(self)

        # --- GRÁFICO (Esquerda) ---
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)

        figura = Figure(figsize=(2, 2), dpi=100)
        figura.patch.set_facecolor("#2c2c3c")  # Cor de fundo do widget
        ax = figura.add_subplot(111)

        percentual = (gasto / limite) * 100 if limite > 0 else 0

        # Lógica de cores
        if percentual < 50:
            cor_gasto = "#2a9d8f"  # Verde
        elif percentual < 85:
            cor_gasto = "#f4a261"  # Amarelo
        else:
            cor_gasto = "#e63946"  # Vermelho

        # Garante que o gráfico não quebre se o gasto for maior que o limite
        valor_gasto_grafico = min(gasto, limite)
        valor_restante_grafico = limite - valor_gasto_grafico

        valores = [valor_gasto_grafico, valor_restante_grafico]
        # Cor do gasto e cor do fundo 'restante'
        cores = [cor_gasto, '#4a4a5a']

        ax.pie(valores, labels=None, colors=cores, startangle=90,
               wedgeprops=dict(width=0.4, edgecolor='#2c2c3c'))

        ax.text(0, 0, f'{percentual:.0f}%', ha='center', va='center',
                fontsize=16, color='white', weight='bold')

        canvas = FigureCanvas(figura)
        # Tamanho fixo para o container do gráfico
        chart_container.setFixedSize(150, 150)
        chart_layout.addWidget(canvas)

        main_layout.addWidget(chart_container)

        # --- TEXTOS (Direita) ---
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setAlignment(Qt.AlignVCenter)

        label_categoria = QLabel(categoria)
        label_categoria.setStyleSheet("font-size: 18px; font-weight: bold;")
        text_layout.addWidget(label_categoria)

        gasto_texto = QLabel(f"Gasto: R$ {gasto:,.2f}")
        gasto_texto.setStyleSheet("font-size: 14px;")
        text_layout.addWidget(gasto_texto)

        limite_texto = QLabel(f"Limite: R$ {limite:,.2f}")
        limite_texto.setStyleSheet("font-size: 14px;")
        text_layout.addWidget(limite_texto)

        main_layout.addWidget(text_container)
