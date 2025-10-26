from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit,
    QComboBox, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date, datetime
import sys

from models.despesa import Despesa

class TelaDespesas(QWidget):
    def __init__(self, di_container):
        super().__init__()
        self.di_container = di_container
        self.setWindowTitle("Extrato de Despesas")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        self.despesas = self.di_container.transacao_repository.get_despesas_by_user(self.di_container.usuario_ativo.id)

        main_layout = QVBoxLayout(self)

        # Filtros
        filtro_layout = QHBoxLayout()

        self.data_ini = QDateEdit()
        self.data_ini.setCalendarPopup(True)
        self.data_ini.setDisplayFormat("dd-MM-yyyy")
        self.data_ini.setSpecialValueText("Data inicial")
        self.data_ini.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self.data_ini.setDate(self.data_ini.minimumDate())

        self.data_fim = QDateEdit()
        self.data_fim.setCalendarPopup(True)
        self.data_fim.setDisplayFormat("dd-MM-yyyy")
        self.data_fim.setSpecialValueText("Data final (dd/mm/aaaa)")
        self.data_fim.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self.data_fim.setDate(QDate.currentDate())

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Pix", "Crédito", "Débito", "Dinheiro"])

        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Todos", "Alimentação", "Transporte", "Lazer", "Moradia"])

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.filtrar_despesas)

        self.btn_adicionar = QPushButton("+")
        self.btn_adicionar.setFixedWidth(40)
        self.btn_adicionar.clicked.connect(self.abrir_adicionar_despesa)

        for widget in [self.data_ini, self.data_fim, self.tipo_combo, self.categoria_combo, self.btn_filtrar, self.btn_adicionar]:
            filtro_layout.addWidget(widget)
        main_layout.addLayout(filtro_layout)

        # Conteúdo principal
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Tabela à esquerda
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "Tipo", "Categoria", "Valor"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet("background-color: #2c2c3c; color: white; border:none;")
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
        self.fig_tipo = Figure(figsize=(4,2.5))
        self.fig_tipo.patch.set_facecolor("#1e1e2f")
        self.canvas_tipo = FigureCanvas(self.fig_tipo)
        self.graficos_layout.addWidget(self.canvas_tipo)

        # Gráfico Categoria
        self.fig_cat = Figure(figsize=(4,2.5))
        self.fig_cat.patch.set_facecolor("#1e1e2f")
        self.canvas_cat = FigureCanvas(self.fig_cat)
        self.graficos_layout.addWidget(self.canvas_cat)

        # Carregar dados
        self.carregar_despesas(self.despesas)
        self.atualizar_graficos()

    # ================= Funções =================
    def carregar_despesas(self, lista):
        self.tabela.setRowCount(0)
        total = 0
        for d in lista:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(d.data.strftime("%d/%m/%Y")))
            self.tabela.setItem(row, 1, QTableWidgetItem(d.descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(d.metodo_pagamento))
            self.tabela.setItem(row, 3, QTableWidgetItem(d.categoria))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R$ {d.valor:.2f}"))
            total += d.valor
        self.label_total.setText(f"Total de Despesas: R$ {total:.2f}")


    # TODO: Nao esta funcionando
    def filtrar_despesas(self):
        data_ini = self.data_ini.text().strip()
        data_fim = self.data_fim.text().strip()
        tipo = self.metodo_pagamento_combo.currentText()
        categoria = self.categoria_combo.currentText()

        def str_para_data(s):
            try:
                return datetime.strptime(s, "%d/%m/%Y")
            except:
                return None

        ini = str_para_data(data_ini)
        fim = str_para_data(data_fim)

        filtradas = []
        for d in self.despesas:
            data_desp = str_para_data(d.data.strftime("%d/%m/%Y"))
            if (not ini or data_desp >= ini) and (not fim or data_desp <= fim):
                if (tipo == "Todos" or d.metodo_pagamento == tipo) and (categoria == "Todos" or d.categoria == categoria):
                    filtradas.append(d)
        self.carregar_despesas(filtradas)
        self.atualizar_graficos(filtradas)


    # TODO: Nao esta funcionando
    def atualizar_graficos(self, lista=None):
        if lista is None:
            lista = self.despesas

        tipos = ["Pix", "Crédito", "Débito", "Dinheiro"]
        valores_tipo = [sum(d.valor for d in lista if d.metodo_pagamento==t) for t in tipos]

        tipos_filtrados = [t for t, v in zip(tipos, valores_tipo) if v > 0]
        valores_filtrados = [v for v in valores_tipo if v > 0]

        self.fig_tipo.clear()
        ax1 = self.fig_tipo.add_subplot(111)
        ax1.pie(
            valores_filtrados,
            labels=tipos_filtrados,
            colors=["#e63946","#f4a261","#2a9d8f","#8d99ae"][:len(tipos_filtrados)],
            textprops={'color':'white'},
            autopct='%1.1f%%'
        )
        self.canvas_tipo.draw()

        # --- Gráfico por Categoria ---
        categorias = list(set(d.categoria for d in lista))
        valores_cat = [sum(d.valor for d in lista if d.categoria==c) for c in categorias]

        categorias_filtradas = [c for c, v in zip(categorias, valores_cat) if v > 0]
        valores_cat_filtrados = [v for v in valores_cat if v > 0]

        self.fig_cat.clear()
        ax2 = self.fig_cat.add_subplot(111)
        ax2.pie(
            valores_cat_filtrados,
            labels=categorias_filtradas,
            textprops={'color':'white'},
            autopct='%1.1f%%'
        )
        self.canvas_cat.draw()

    # ================= Adicionar despesa =================
    def abrir_adicionar_despesa(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Despesa")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")
        layout = QFormLayout(dialog)


        input_data = QDateEdit()
        input_data.setCalendarPopup(True)
        input_data.setDisplayFormat("dd-MM-yyyy")
        input_data.setDate(QDate.currentDate())
        input_desc = QLineEdit()
        input_tipo = QComboBox()
        input_tipo.addItems(["Pix", "Crédito", "Débito", "Dinheiro"])
        input_categoria = QComboBox()
        input_categoria.addItems(["Alimentação", "Transporte", "Lazer", "Moradia"])
        input_valor = QLineEdit()

        layout.addRow("Data:", input_data)
        layout.addRow("Descrição:", input_desc)
        layout.addRow("Tipo:", input_tipo)
        layout.addRow("Categoria:", input_categoria)
        layout.addRow("Valor:", input_valor)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def adicionar():
            # Validate description
            if not input_desc.text().strip():
                QMessageBox.warning(dialog, "Erro", "O campo descrição não pode estar vazio.")
                return

            # Validate value
            try:
                valor = float(input_valor.text().replace(",", "."))
                if valor <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(dialog, "Erro", "Insira um valor numérico positivo.")
                return

            # Validate date
            qdate = input_data.date() 
            if not qdate.isValid():
                QMessageBox.warning(dialog, "Erro", "Data inválida.")
                return
            
            python_date = date(qdate.year(), qdate.month(), qdate.day())

            # If all validations pass:
            try:
                nova_despesa = Despesa(
                    descricao=input_desc.text().strip(),
                    categoria=input_categoria.currentText(),
                    metodo_pagamento=input_tipo.currentText(),
                    valor=valor,
                    tipo="despesa",
                    usuario_id=self.di_container.usuario_ativo.id,
                    data=python_date
                )

                self.di_container.transacao_repository.add(nova_despesa)

                despesas_db = self.di_container.transacao_repository.get_despesas_by_user(
                    self.di_container.usuario_ativo.id
                )
                self.carregar_despesas(despesas_db)
                self.atualizar_graficos()

                dialog.accept()

            except Exception as e:
                QMessageBox.warning(dialog, "Erro", f"Erro ao salvar no banco de dados: {e}")

        buttons.accepted.connect(adicionar)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

