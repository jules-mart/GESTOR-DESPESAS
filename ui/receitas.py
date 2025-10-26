# ui/Receitas.py (CORRIGIDO)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

from models.receita import Receita


class AbaReceitas(QWidget):
    def __init__(self, di_container):
        super().__init__()
        self.di_container = di_container
        self.setWindowTitle("Extrato de Receitas")
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # Dados de exemplo de RECEITAS
        self.receitas = self.di_container.transacao_repository.get_receitas_by_user(self.di_container.usuario_ativo.id)

        main_layout = QVBoxLayout(self)

        # Filtros
        filtro_layout = QHBoxLayout()
        self.data_ini = QLineEdit()
        self.data_ini.setPlaceholderText("Data inicial (dd/mm/aaaa)")
        self.data_fim = QLineEdit()
        self.data_fim.setPlaceholderText("Data final (dd/mm/aaaa)")

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Transferência", "Pix", "Dinheiro"])

        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(
            ["Todos", "Salário", "Trabalho Extra", "Vendas"])

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(
            self.filtrar_receitas)  # Esta linha agora funciona

        self.btn_adicionar = QPushButton("+")
        self.btn_adicionar.setFixedWidth(40)
        self.btn_adicionar.clicked.connect(self.abrir_adicionar_receita)

        for widget in [self.data_ini, self.data_fim, self.tipo_combo, self.categoria_combo, self.btn_filtrar, self.btn_adicionar]:
            filtro_layout.addWidget(widget)
        main_layout.addLayout(filtro_layout)

        # Conteúdo principal
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Tabela à esquerda
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Data", "Descrição", "Tipo", "Categoria", "Valor"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet(
            "background-color: #2c2c3c; color: white; border:none;")
        self.tabela.setShowGrid(False)
        content_layout.addWidget(self.tabela)

        # Gráficos à direita
        self.graficos_layout = QVBoxLayout()
        content_layout.addLayout(self.graficos_layout)

        # Label total
        self.label_total = QLabel()
        self.label_total.setAlignment(Qt.AlignCenter)
        self.label_total.setStyleSheet("font-size: 16pt; color: white;")
        self.graficos_layout.addWidget(self.label_total)

        # Gráfico Tipo
        self.fig_tipo = Figure(figsize=(4, 2.5))
        self.fig_tipo.patch.set_facecolor("#1e1e2f")
        self.canvas_tipo = FigureCanvas(self.fig_tipo)
        self.graficos_layout.addWidget(self.canvas_tipo)

        # Gráfico Categoria
        self.fig_cat = Figure(figsize=(4, 2.5))
        self.fig_cat.patch.set_facecolor("#1e1e2f")
        self.canvas_cat = FigureCanvas(self.fig_cat)
        self.graficos_layout.addWidget(self.canvas_cat)

        # Carregar dados
        self.carregar_receitas(self.receitas)
        self.atualizar_graficos()

    # ================= Funções =================
    def carregar_receitas(self, lista):
        self.tabela.setRowCount(0)
        total = 0
        for r in lista:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(r.data))
            self.tabela.setItem(row, 1, QTableWidgetItem(r.descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(r.metodo_pagamento))
            self.tabela.setItem(row, 3, QTableWidgetItem(r.categoria))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R$ {r.valor:.2f}"))
            total += r.valor
        self.label_total.setText(f"Total de Receitas: R$ {total:.2f}")

    # --- AQUI ESTÁ A FUNÇÃO QUE FALTAVA ---
    def filtrar_receitas(self):
        data_ini = self.data_ini.text().strip()
        data_fim = self.data_fim.text().strip()
        tipo = self.tipo_combo.currentText()
        categoria = self.categoria_combo.currentText()

        def str_para_data(s):
            try:
                return datetime.strptime(s, "%d/%m/%Y")
            except (ValueError, TypeError):
                return None

        ini = str_para_data(data_ini)
        fim = str_para_data(data_fim)

        filtradas = []
        for r in self.receitas:
            data_receita = str_para_data(r.data)
            if data_receita:  # Só processa se a data for válida
                if (not ini or data_receita >= ini) and (not fim or data_receita <= fim):
                    if (tipo == "Todos" or r.metodo_pagamento == tipo) and (categoria == "Todos" or r.categoria == categoria):
                        filtradas.append(r)

        self.carregar_receitas(filtradas)
        self.atualizar_graficos(filtradas)
    # ----------------------------------------

    def atualizar_graficos(self, lista=None):
        if lista is None:
            lista = self.receitas

        # --- Gráfico por Tipo ---
        tipos = list(set(r.metodo_pagamento for r in lista))
        valores_tipo = [sum(r.valor
                            for r in lista if r.metodo_pagamento == t) for t in tipos]

        self.fig_tipo.clear()
        ax1 = self.fig_tipo.add_subplot(111)
        ax1.pie(
            valores_tipo,
            labels=tipos,
            textprops={'color': 'white'},
            autopct='%1.1f%%'
        )
        self.canvas_tipo.draw()

        # --- Gráfico por Categoria ---
        categorias = list(set(r.categoria for r in lista))
        valores_cat = [
            sum(r.valor for r in lista if r.categoria == c) for c in categorias]

        self.fig_cat.clear()
        ax2 = self.fig_cat.add_subplot(111)
        ax2.pie(
            valores_cat,
            labels=categorias,
            textprops={'color': 'white'},
            autopct='%1.1f%%'
        )
        self.canvas_cat.draw()

    # ================= Adicionar receita =================
    def abrir_adicionar_receita(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Receita")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")
        layout = QFormLayout(dialog)

        input_data = QLineEdit()
        input_data.setPlaceholderText("dd/mm/aaaa")
        input_desc = QLineEdit()
        input_tipo = QComboBox()
        input_tipo.addItems(["Transferência", "Pix", "Dinheiro"])
        input_categoria = QComboBox()
        input_categoria.addItems(["Salário", "Trabalho Extra", "Vendas"])
        input_valor = QLineEdit()

        layout.addRow("Data:", input_data)
        layout.addRow("Descrição:", input_desc)
        layout.addRow("Tipo:", input_tipo)
        layout.addRow("Categoria:", input_categoria)
        layout.addRow("Valor:", input_valor)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def adicionar():
            try:
                valor = float(input_valor.text().replace(",", "."))

                nova_receita = Receita(
                    descricao=input_desc.text(),
                    categoria=input_categoria.currentText(),
                    metodo_pagamento=input_tipo.currentText(),
                    valor=valor,
                    tipo="receita",
                    usuario_id=self.di_container.usuario_ativo.id,
                    data=input_data.text()
                )

                self.di_container.transacao_repository.add(nova_receita)

                receitas_db = self.di_container.transacao_repository.get_receitas_by_user(self.di_container.usuario_ativo.id)
                self.carregar_receitas(receitas_db)
                self.atualizar_graficos()
                dialog.accept()
            except:
                QMessageBox.warning(dialog, "Erro", "Valor inválido!")

        buttons.accepted.connect(adicionar)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()
