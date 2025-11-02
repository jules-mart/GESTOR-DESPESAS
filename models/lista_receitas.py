from datetime import date, datetime
from database.di_container import DIContainer
from models.receita import Receita


class ListaReceitas:
    def __init__(self, di_container: DIContainer):
        self.di_container = di_container
        self.__lista_receitas: list[Receita] = self.di_container.transacao_repository.get_receitas_by_user(
            self.di_container.usuario_ativo.id
        )

    @property
    def lista_receitas(self):
        return self.__lista_receitas.copy()

    def atualizar_receitas(self):
        self.__lista_receitas = self.di_container.transacao_repository.get_receitas_by_user(
            self.di_container.usuario_ativo.id
        )

    def filtrar_receitas(self, dataIni: date, dataFim: date, tipo: str, categoria: str):
        filtradas = [
            r for r in self.__lista_receitas
            if dataIni <= r.data <= dataFim
            and (tipo == "Todos" or r.metodo_pagamento == tipo)
            and (categoria == "Todos" or r.categoria == categoria)
        ]
        return filtradas

    def informacoes_grafico_tipo(self, lista=None):
        if lista is None:
            lista = self.__lista_receitas
        metodos = ["Pix", "Transferência", "Dinheiro"]
        valores = [sum(r.valor for r in lista if r.metodo_pagamento == m) for m in metodos]

        metodos_filtrados = []
        valores_filtrados = []
        for m, v in zip(metodos, valores):
            if v > 0:
                metodos_filtrados.append(m)
                valores_filtrados.append(v)

        return metodos_filtrados, valores_filtrados

    def informacoes_grafico_categoria(self, lista=None):
        if lista is None:
            lista = self.__lista_receitas
        if not lista:
            return [], []

        categorias = sorted(list(set(r.categoria for r in lista if r.categoria)))
        valores = [sum(r.valor for r in lista if r.categoria == c) for c in categorias]

        categorias_filtradas = []
        valores_filtrados = []
        for c, v in zip(categorias, valores):
            if v > 0:
                categorias_filtradas.append(c)
                valores_filtrados.append(v)

        return categorias_filtradas, valores_filtrados

    # ===== Adicionar, editar e excluir receitas =====
    def adicionar_receita(self, receita: Receita):
        self.di_container.transacao_repository.add(receita)
        self.atualizar_receitas()

    def editar_receita(self, receita: Receita):
        self.di_container.transacao_repository.update(receita)
        self.atualizar_receitas()

    def excluir_receita(self, receita: Receita):
        self.di_container.transacao_repository.delete(receita)
        self.atualizar_receitas()
