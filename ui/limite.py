# ui/Limites.py (COM GRÁFICOS CIRCULARES)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDialog, QFormLayout, QDialogButtonBox, QMessageBox,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from database.di_container import DIContainer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from models.limite import Limite


class AbaLimites(QWidget):
    def __init__(self, di_container: DIContainer, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent; color: white;")

        self.usuario_id = di_container.usuario_ativo.id
        self.limite_repository = di_container.limite_repository
        self.transacao_repository = di_container.transacao_repository
        
        # Initialize empty data structures
        self.gastos_atuais = {}  
        self.limites = {}

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

        # Load data from database
        self.carregar_limites_do_banco()

    def carregar_limites_do_banco(self):
        """Load limits from database and update the display"""
        if self.usuario_id:
            limites_db = self.limite_repository.get_by_usuario_id(self.usuario_id)
            
            self.limites = {}
            for limite in limites_db:
                self.limites[limite.categoria_limite] = limite.valor_limite
            
            self.carregar_gastos_atuais()
            
            self.atualizar_lista_limites()

    def carregar_gastos_atuais(self):
        """Load current expenses for each category"""

        try:
            despesas_mes_atual = self.transacao_repository.get_current_month_despesas(self.usuario_id)
            
            self.gastos_atuais = {categoria: 0 for categoria in self.limites.keys()}
            
            # Sum expenses by category
            for despesa in despesas_mes_atual:
                categoria = despesa.categoria 
                if categoria in self.gastos_atuais:
                    self.gastos_atuais[categoria] += despesa.valor
                else:
                    self.gastos_atuais[categoria] = despesa.valor
                    
        except Exception as e:
            print(f"Erro ao carregar gastos atuais: {e}")
            self.gastos_atuais = {categoria: 0 for categoria in self.limites.keys()}

    
    def atualizar_lista_limites(self):
        """Update the limits list display"""
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
        # Get available categories (you need to define this based on your categories)
        categorias_disponiveis = self.obter_categorias_disponiveis()
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
                self.adicionar_limite_banco(categoria, valor)
                self.carregar_limites_do_banco()  # Reload from database
            except ValueError:
                self.mostrar_erro("Valor inválido. Por favor, insira um número válido.")

    def obter_categorias_disponiveis(self):
        """Get available categories that don't have limits yet"""
        # TODO: Implement this based on your categories system
        # This should return all possible expense categories that don't have limits set
        todas_categorias = ["Alimentação", "Transporte", "Lazer", "Moradia"]
        categorias_com_limite = self.limites.keys()
        return [cat for cat in todas_categorias if cat not in categorias_com_limite]

    def adicionar_limite_banco(self, categoria: str, valor: float):
        """Add a new limit to the database"""
        if self.usuario_id:
            # Check if limit already exists for this category
            limite_existente = self.limite_repository.get_by_categoria(categoria, self.usuario_id)
            
            if limite_existente:
                # Update existing limit
                self.limite_repository.update(limite_existente.id, valor)
            else:
                # Create new limit
                novo_limite = Limite(
                    categoria_limite=categoria,
                    valor_limite=valor,
                    usuario_id=self.usuario_id
                )
                self.limite_repository.add(novo_limite)

    def mostrar_erro(self, mensagem: str):
        """Show error message"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setWindowTitle("Erro")
        msg.exec()

    def set_usuario_id(self, usuario_id: int):
        """Set user ID and reload data"""
        self.usuario_id = usuario_id
        self.carregar_limites_do_banco()
# --- Widget customizado com o Gráfico Circular ---


class LimiteWidget(QFrame):
    def __init__(self, categoria, gasto, limite, parent=None):
        super().__init__(parent)
        self.categoria = categoria
        self.gasto = gasto
        self.limite = limite
        
        self.setStyleSheet("""
            QFrame {
                background-color: #2c2c3c;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        self.setContentsMargins(0, 0, 0, 10)

        # Layout principal (horizontal: gráfico à esquerda, textos à direita, botões à direita)
        main_layout = QHBoxLayout(self)

        # --- GRÁFICO (Esquerda) ---
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)

        figura = Figure(figsize=(2, 2), dpi=100)
        figura.patch.set_facecolor("#2c2c3c")
        ax = figura.add_subplot(111)

        percentual = (gasto / limite) * 100 if limite > 0 else 0

        # Lógica de cores
        if percentual < 50:
            cor_gasto = "#2a9d8f"  # Verde
        elif percentual < 85:
            cor_gasto = "#f4a261"  # Amarelo
        else:
            cor_gasto = "#e63946"  # Vermelho

        valor_gasto_grafico = min(gasto, limite)
        valor_restante_grafico = limite - valor_gasto_grafico

        valores = [valor_gasto_grafico, valor_restante_grafico]
        cores = [cor_gasto, '#4a4a5a']

        ax.pie(valores, labels=None, colors=cores, startangle=90,
               wedgeprops=dict(width=0.4, edgecolor='#2c2c3c'))

        ax.text(0, 0, f'{percentual:.0f}%', ha='center', va='center',
                fontsize=16, color='white', weight='bold')

        canvas = FigureCanvas(figura)
        chart_container.setFixedSize(150, 150)
        chart_layout.addWidget(canvas)
        main_layout.addWidget(chart_container)

        # --- TEXTOS (Centro) ---
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
        
        # --- BOTÕES (Direita) ---
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setAlignment(Qt.AlignVCenter)
        
        btn_editar = QPushButton("Editar")
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; font-weight: bold;
                padding: 6px 12px; border-radius: 6px; font-size: 12px;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        btn_editar.clicked.connect(self.editar_limite)
        
        btn_excluir = QPushButton("Excluir")
        btn_excluir.setStyleSheet("""
            QPushButton {
                background-color: #ef4444; color: white; font-weight: bold;
                padding: 6px 12px; border-radius: 6px; font-size: 12px;
            }
            QPushButton:hover { background-color: #dc2626; }
        """)
        btn_excluir.clicked.connect(self.excluir_limite)
        
        buttons_layout.addWidget(btn_editar)
        buttons_layout.addWidget(btn_excluir)
        main_layout.addWidget(buttons_container)

    def editar_limite(self):
        # Implement edit functionality
        pass

    def excluir_limite(self):
        # Implement delete functionality
        pass
