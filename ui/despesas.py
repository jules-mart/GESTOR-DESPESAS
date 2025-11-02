from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit,
    QComboBox, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDate, Signal
from database.di_container import DIContainer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date, datetime
import sys

from models.despesa import Despesa
from models.lista_despesas import ListaDespesas


class TelaDespesas(QWidget):
    despesa_adicionada = Signal()

    def __init__(self, di_container: DIContainer):
        super().__init__()
        self.di_container = di_container
        self.setWindowTitle("Extrato de Despesas")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        self.despesas = ListaDespesas(di_container)

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

        self.btn_adicionar = QPushButton("＋ Adicionar Despesa")
        self.btn_adicionar.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; font-weight: bold;
                font-size: 14px; padding: 8px 16px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_adicionar.clicked.connect(self.abrir_adicionar_despesa)
        filtro_layout.addWidget(self.btn_adicionar)

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
        self.carregar_despesas()
        self.atualizar_graficos()

    # ================= Funções =================
    def carregar_despesas(self, lista=None):
        if lista is None:
            lista = self.despesas.lista_despesas
        self.tabela.setRowCount(0)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "Tipo", "Categoria", "Valor", "Editar", "Excluir"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

            # Botão editar
            btn_editar = QPushButton("✏️")
            btn_editar.setStyleSheet("background-color: #3b82f6; color: white; border-radius: 4px; font-size: 11px; padding: 1px;")
            btn_editar.setFixedSize(28, 22)
            btn_editar.clicked.connect(lambda _, desp=d: self.editar_despesa(desp))
            widget_editar = QWidget()
            layout_editar = QHBoxLayout(widget_editar)
            layout_editar.addWidget(btn_editar)
            layout_editar.setAlignment(Qt.AlignCenter)
            layout_editar.setContentsMargins(0, 0, 0, 0)
            self.tabela.setCellWidget(row, 5, widget_editar)

            # Botão excluir
            btn_excluir = QPushButton("🗑️")
            btn_excluir.setStyleSheet("background-color: #ef4444; color: white; border-radius: 4px; font-size: 11px; padding: 1px;")
            btn_excluir.setFixedSize(28, 22)
            btn_excluir.clicked.connect(lambda _, desp=d: self.excluir_despesa(desp))
            widget_excluir = QWidget()
            layout_excluir = QHBoxLayout(widget_excluir)
            layout_excluir.addWidget(btn_excluir)
            layout_excluir.setAlignment(Qt.AlignCenter)
            layout_excluir.setContentsMargins(0, 0, 0, 0)
            self.tabela.setCellWidget(row, 6, widget_excluir)

        self.label_total.setText(f"Total de Despesas: R$ {total:.2f}")

    def editar_despesa(self, despesa):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Despesa")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")
        layout = QFormLayout(dialog)

        input_data = QDateEdit()
        input_data.setCalendarPopup(True)
        input_data.setDisplayFormat("dd-MM-yyyy")
        input_data.setDate(QDate(despesa.data.year, despesa.data.month, despesa.data.day))
        input_desc = QLineEdit(despesa.descricao)
        input_tipo = QComboBox()
        input_tipo.addItems(["Pix", "Crédito", "Débito", "Dinheiro"])
        input_tipo.setCurrentText(despesa.metodo_pagamento)
        input_categoria = QComboBox()
        input_categoria.addItems(["Alimentação", "Transporte", "Lazer", "Moradia"])
        input_categoria.setCurrentText(despesa.categoria)
        input_valor = QLineEdit(str(despesa.valor))

        layout.addRow("Data:", input_data)
        layout.addRow("Descrição:", input_desc)
        layout.addRow("Tipo:", input_tipo)
        layout.addRow("Categoria:", input_categoria)
        layout.addRow("Valor:", input_valor)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def salvar_edicao():
            try:
                despesa.descricao = input_desc.text().strip()
                despesa.metodo_pagamento = input_tipo.currentText()
                despesa.categoria = input_categoria.currentText()
                despesa.valor = float(input_valor.text().replace(",", "."))
                qdate = input_data.date()
                despesa.data = date(qdate.year(), qdate.month(), qdate.day())

                self.di_container.transacao_repository.update(despesa)
                self.despesas.atualizar_despesas()
                self.carregar_despesas()
                self.atualizar_graficos()
                dialog.accept()
                self.despesa_adicionada.emit()
            except Exception as e:
                QMessageBox.warning(dialog, "Erro", f"Não foi possível salvar: {e}")

        buttons.accepted.connect(salvar_edicao)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    def excluir_despesa(self, despesa):
        resp = QMessageBox.question(
            self,
            "Excluir Despesa",
            f"Tem certeza que deseja excluir '{despesa.descricao}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            try:
                self.di_container.transacao_repository.delete(despesa)
                self.despesas.atualizar_despesas()
                self.carregar_despesas()
                self.atualizar_graficos()
                self.despesa_adicionada.emit()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível excluir: {e}")

    def filtrar_despesas(self):
        ini_qdate = self.data_ini.date()
        fim_qdate = self.data_fim.date()
        ini = datetime(ini_qdate.year(), ini_qdate.month(), ini_qdate.day())
        fim = datetime(fim_qdate.year(), fim_qdate.month(), fim_qdate.day())

        tipo = self.tipo_combo.currentText()
        categoria = self.categoria_combo.currentText()

        filtradas = self.despesas.filtrar_despesas(ini, fim, tipo, categoria)

        self.carregar_despesas(filtradas)
        self.atualizar_graficos(filtradas)

    def atualizar_graficos(self, lista=None):
        if lista is None:
            lista = self.despesas.lista_despesas

        # --- Gráfico por Tipo ---
        tipos_filtrados, valores_filtrados = self.despesas.informacoes_grafico_tipo(lista)

        self.fig_tipo.clear()
        ax1 = self.fig_tipo.add_subplot(111)
        ax1.set_facecolor('#1e1e2f')
        self.fig_tipo.patch.set_facecolor('#1e1e2f')

        colors_tipo = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFA726', '#AB47BC']

        wedges1, texts1, autotexts1 = ax1.pie(
            valores_filtrados,
            labels=tipos_filtrados,
            colors=colors_tipo[:len(tipos_filtrados)],
            textprops={'color': 'white', 'fontsize': 10},
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.5, edgecolor='none', linewidth=0)
        )

        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        self.canvas_tipo.draw()

        # --- Gráfico por Categoria ---
        categorias_filtradas, valores_cat_filtrados = self.despesas.informacoes_grafico_categoria(lista)

        self.fig_cat.clear()
        ax2 = self.fig_cat.add_subplot(111)
        ax2.set_facecolor('#1e1e2f')
        self.fig_cat.patch.set_facecolor('#1e1e2f')

        colors_cat = ['#6A89CC', '#F8C471', '#82CCDD', '#B8E994', '#60A3BC', '#CAD3C8', '#E55039', '#78E08F']

        wedges2, texts2, autotexts2 = ax2.pie(
            valores_cat_filtrados,
            labels=categorias_filtradas,
            colors=colors_cat[:len(categorias_filtradas)],
            textprops={'color': 'white', 'fontsize': 10},
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.5, edgecolor='none', linewidth=0)
        )

        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        self.canvas_cat.draw()

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
            if not input_desc.text().strip():
                QMessageBox.warning(dialog, "Erro", "O campo descrição não pode estar vazio.")
                return

            try:
                valor = float(input_valor.text().replace(",", "."))
                if valor <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(dialog, "Erro", "Insira um valor numérico positivo.")
                return

            qdate = input_data.date()
            if not qdate.isValid():
                QMessageBox.warning(dialog, "Erro", "Data inválida.")
                return

            python_date = date(qdate.year(), qdate.month(), qdate.day())

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

                self.despesas.atualizar_despesas()

                self.carregar_despesas()
                self.atualizar_graficos()

                dialog.accept()
                self.despesa_adicionada.emit()
            except Exception as e:
                QMessageBox.warning(dialog, "Erro", f"Erro ao salvar no banco de dados: {e}")

        buttons.accepted.connect(adicionar)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()
