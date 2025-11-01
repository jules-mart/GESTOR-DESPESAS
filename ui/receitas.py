# ui/Receitas.py (CORRIGIDO)

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit,
    QComboBox, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDate, Signal
from database.di_container import DIContainer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date
from models.receita import Receita


class AbaReceitas(QWidget):
    receita_adicionada = Signal()

    def __init__(self, di_container: DIContainer):
        super().__init__()
        self.di_container = di_container
        self.setWindowTitle("Extrato de Receitas")
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # Dados de exemplo de RECEITAS
        self.receitas = self.di_container.transacao_repository.get_receitas_by_user(
            self.di_container.usuario_ativo.id
        )

        main_layout = QVBoxLayout(self)

        # ======= Filtros =======
        self.btn_adicionar = QPushButton("＋ Adicionar Receita")
        self.btn_adicionar.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; font-weight: bold;
                font-size: 14px; padding: 8px 16px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_adicionar.clicked.connect(self.abrir_adicionar_receita)
        
        filtro_layout = QHBoxLayout()
        self.data_ini = QDateEdit()
        self.data_ini.setCalendarPopup(True)
        self.data_ini.setDisplayFormat("dd-MM-yyyy")
        self.data_ini.setDate(QDate(1900, 1, 1))

        self.data_fim = QDateEdit()
        self.data_fim.setCalendarPopup(True)
        self.data_fim.setDisplayFormat("dd-MM-yyyy")
        self.data_fim.setDate(QDate.currentDate())

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Transferência", "Pix", "Dinheiro"])

        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Todos", "Salário", "Trabalho Extra", "Vendas"])

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.filtrar_receitas)

        # Adicionando widgets na ordem correta (botão por último)
        for widget in [self.data_ini, self.data_fim, self.tipo_combo, self.categoria_combo, self.btn_filtrar, self.btn_adicionar]:
            filtro_layout.addWidget(widget)

        main_layout.addLayout(filtro_layout)

        # ======= Conteúdo principal =======
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # ======= Tabela =======
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(
            ["Data", "Descrição", "Tipo", "Categoria", "Valor", "Editar", "Excluir"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet(
            "background-color: #2c2c3c; color: white; border:none;"
        )
        self.tabela.setShowGrid(False)
        content_layout.addWidget(self.tabela)

        # ======= Gráficos =======
        self.graficos_layout = QVBoxLayout()
        content_layout.addLayout(self.graficos_layout)

        self.label_total = QLabel()
        self.label_total.setAlignment(Qt.AlignCenter)
        self.label_total.setStyleSheet("font-size: 16pt; color: white;")
        self.graficos_layout.addWidget(self.label_total)

        self.fig_tipo = Figure(figsize=(4, 2.5))
        self.fig_tipo.patch.set_facecolor("#1e1e2f")
        self.canvas_tipo = FigureCanvas(self.fig_tipo)
        self.graficos_layout.addWidget(self.canvas_tipo)

        self.fig_cat = Figure(figsize=(4, 2.5))
        self.fig_cat.patch.set_facecolor("#1e1e2f")
        self.canvas_cat = FigureCanvas(self.fig_cat)
        self.graficos_layout.addWidget(self.canvas_cat)

        # ======= Dados iniciais =======
        self.carregar_receitas(self.receitas)
        self.atualizar_graficos(self.receitas)

    # =======================
    def carregar_receitas(self, lista):
        self.tabela.setRowCount(0)
        total = 0

        for r in lista:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(r.data.strftime("%d/%m/%Y")))
            self.tabela.setItem(row, 1, QTableWidgetItem(r.descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(r.metodo_pagamento))
            self.tabela.setItem(row, 3, QTableWidgetItem(r.categoria))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R$ {r.valor:.2f}"))
            total += r.valor

            # Botão editar
            btn_editar = QPushButton("✏️")
            btn_editar.setStyleSheet(
                "background-color: #3b82f6; color: white; border-radius: 4px; font-size: 11px; padding: 1px;"
            )
            btn_editar.setFixedSize(28, 22)
            btn_editar.clicked.connect(lambda _, receita=r: self.editar_receita(receita))
            widget_editar = QWidget()
            layout_editar = QHBoxLayout(widget_editar)
            layout_editar.addWidget(btn_editar)
            layout_editar.setAlignment(Qt.AlignCenter)
            layout_editar.setContentsMargins(0, 0, 0, 0)
            self.tabela.setCellWidget(row, 5, widget_editar)

            # Botão excluir
            btn_excluir = QPushButton("🗑️")
            btn_excluir.setStyleSheet(
                "background-color: #ef4444; color: white; border-radius: 4px; font-size: 11px; padding: 1px;"
            )
            btn_excluir.setFixedSize(28, 22)
            btn_excluir.clicked.connect(lambda _, receita=r: self.excluir_receita(receita))
            widget_excluir = QWidget()
            layout_excluir = QHBoxLayout(widget_excluir)
            layout_excluir.addWidget(btn_excluir)
            layout_excluir.setAlignment(Qt.AlignCenter)
            layout_excluir.setContentsMargins(0, 0, 0, 0)
            self.tabela.setCellWidget(row, 6, widget_excluir)

        self.label_total.setText(f"Total de Receitas: R$ {total:.2f}")

    # =======================
    def filtrar_receitas(self):
        ini = date(self.data_ini.date().year(), self.data_ini.date().month(), self.data_ini.date().day())
        fim = date(self.data_fim.date().year(), self.data_fim.date().month(), self.data_fim.date().day())
        tipo = self.tipo_combo.currentText()
        categoria = self.categoria_combo.currentText()

        filtradas = [
            r for r in self.receitas
            if ini <= r.data <= fim and
            (tipo == "Todos" or r.metodo_pagamento == tipo) and
            (categoria == "Todos" or r.categoria == categoria)
        ]
        self.carregar_receitas(filtradas)
        self.atualizar_graficos(filtradas)

    # =======================
    def atualizar_graficos(self, lista=None):
        if lista is None:
            lista = self.receitas

        # --- Gráfico Tipo ---
        tipos = list(set(r.metodo_pagamento for r in lista))
        valores_tipo = [sum(r.valor for r in lista if r.metodo_pagamento == t) for t in tipos]

        self.fig_tipo.clear()
        ax1 = self.fig_tipo.add_subplot(111)
        ax1.set_facecolor('#1e1e2f')
        self.fig_tipo.patch.set_facecolor('#1e1e2f')
        ax1.pie(
            valores_tipo, labels=tipos, autopct='%1.1f%%',
            textprops={'color': 'white'}, startangle=90
        )
        self.canvas_tipo.draw()

        # --- Gráfico Categoria ---
        categorias = list(set(r.categoria for r in lista))
        valores_cat = [sum(r.valor for r in lista if r.categoria == c) for c in categorias]

        self.fig_cat.clear()
        ax2 = self.fig_cat.add_subplot(111)
        ax2.set_facecolor('#1e1e2f')
        self.fig_cat.patch.set_facecolor('#1e1e2f')
        ax2.pie(
            valores_cat, labels=categorias, autopct='%1.1f%%',
            textprops={'color': 'white'}, startangle=90
        )
        self.canvas_cat.draw()

    # =======================
    def abrir_adicionar_receita(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Receita")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")
        layout = QFormLayout(dialog)

        input_data = QDateEdit()
        input_data.setCalendarPopup(True)
        input_data.setDisplayFormat("dd-MM-yyyy")
        input_data.setDate(QDate.currentDate())

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
            python_date = date(qdate.year(), qdate.month(), qdate.day())

            nova_receita = Receita(
                descricao=input_desc.text(),
                categoria=input_categoria.currentText(),
                metodo_pagamento=input_tipo.currentText(),
                valor=valor,
                tipo="receita",
                usuario_id=self.di_container.usuario_ativo.id,
                data=python_date
            )

            self.di_container.transacao_repository.add(nova_receita)
            receitas_db = self.di_container.transacao_repository.get_receitas_by_user(self.di_container.usuario_ativo.id)
            self.carregar_receitas(receitas_db)
            self.atualizar_graficos(receitas_db)
            dialog.accept()
            self.receita_adicionada.emit()

        buttons.accepted.connect(adicionar)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    # =======================
    def editar_receita(self, receita):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Receita")
        dialog.setStyleSheet("background-color: #1e1e2f; color: white;")
        layout = QFormLayout(dialog)

        input_data = QDateEdit()
        input_data.setCalendarPopup(True)
        input_data.setDisplayFormat("dd-MM-yyyy")
        input_data.setDate(QDate(receita.data.year, receita.data.month, receita.data.day))
        input_desc = QLineEdit(receita.descricao)
        input_tipo = QComboBox()
        input_tipo.addItems(["Transferência", "Pix", "Dinheiro"])
        input_tipo.setCurrentText(receita.metodo_pagamento)
        input_categoria = QComboBox()
        input_categoria.addItems(["Salário", "Trabalho Extra", "Vendas"])
        input_categoria.setCurrentText(receita.categoria)
        input_valor = QLineEdit(str(receita.valor))

        layout.addRow("Data:", input_data)
        layout.addRow("Descrição:", input_desc)
        layout.addRow("Tipo:", input_tipo)
        layout.addRow("Categoria:", input_categoria)
        layout.addRow("Valor:", input_valor)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def salvar_edicao():
            try:
                receita.descricao = input_desc.text().strip()
                receita.metodo_pagamento = input_tipo.currentText()
                receita.categoria = input_categoria.currentText()
                receita.valor = float(input_valor.text().replace(",", "."))
                qdate = input_data.date()
                receita.data = date(qdate.year(), qdate.month(), qdate.day())

                self.di_container.transacao_repository.update(receita)
                receitas_db = self.di_container.transacao_repository.get_receitas_by_user(self.di_container.usuario_ativo.id)
                self.carregar_receitas(receitas_db)
                self.atualizar_graficos(receitas_db)
                dialog.accept()
            except Exception as e:
                QMessageBox.warning(dialog, "Erro", f"Não foi possível salvar: {e}")

        buttons.accepted.connect(salvar_edicao)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    # =======================
    def excluir_receita(self, receita):
        resp = QMessageBox.question(
            self,
            "Excluir Receita",
            f"Tem certeza que deseja excluir '{receita.descricao}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            try:
                self.di_container.transacao_repository.delete(receita)
                receitas_db = self.di_container.transacao_repository.get_receitas_by_user(
                    self.di_container.usuario_ativo.id
                )
                self.carregar_receitas(receitas_db)
                self.atualizar_graficos(receitas_db)
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível excluir: {e}")
