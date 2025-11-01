from datetime import date, datetime
from database.di_container import DIContainer
from models.despesa import Despesa
from repositories.transacao_repository import TransacaoRepository


class ListaDespesas():
    def __init__(self, di_container: DIContainer = None):
        self.__di_container = di_container
        self.__lista_despesas: list[Despesa] = self.__di_container.transacao_repository.get_despesas_by_user(self.__di_container.usuario_ativo.id)

    @property
    def lista_despesas(self):
        return self.__lista_despesas.copy()

    def filtrar_despesas(self, dataIni, dataFim, tipo, categoria) -> list[Despesa]:
        filtradas = []
        
        for d in self.__lista_despesas:
            data_desp = datetime(d.data.year, d.data.month, d.data.day) if isinstance(d.data, date) else d.data
            if dataIni <= data_desp <= dataFim:
                if (tipo == "Todos" or d.metodo_pagamento == tipo) and (categoria == "Todos" or d.categoria == categoria):
                    filtradas.append(d)

        return filtradas
    
    def atualizar_despesas(self):
        self.__lista_despesas = self.__di_container.transacao_repository.get_despesas_by_user(self.__di_container.usuario_ativo.id)

    def informacoes_grafico_tipo(self, lista = None) -> tuple[list[str], list[int]]:
        if lista is None:
            lista = self.__lista_despesas
        
        metodo_pagamento = ["Pix", "Crédito", "Débito", "Dinheiro"]
        
        valores_metodo = []
        for t in metodo_pagamento:
            total = 0
            for d in lista:
                if d.metodo_pagamento == t:
                    try:
                        total += float(d.valor)
                    except (ValueError, TypeError):
                        continue
            valores_metodo.append(total)

        metodos_filtrados = []
        valores_filtrados = []
        
        for t, v in zip(metodo_pagamento, valores_metodo):
            if v > 0:
                metodos_filtrados.append(t)
                valores_filtrados.append(v)
        
        return metodos_filtrados, valores_filtrados
    
    def informacoes_grafico_categoria(self, lista=None) -> tuple[list[str], list[float]]:
        if lista is None:
            lista = self.__lista_despesas

        if not lista:
            return [], []
        
        categorias = []
        for d in lista:
            if hasattr(d, 'categoria') and d.categoria:
                categorias.append(d.categoria)
        
        categorias = sorted(list(set(categorias)))
        
        valores_cat = []
        for c in categorias:
            total = 0
            for d in lista:
                if hasattr(d, 'categoria') and d.categoria == c and hasattr(d, 'valor'):
                    try:
                        total += float(d.valor)
                    except (ValueError, TypeError):
                        continue
            valores_cat.append(total)

        categorias_filtradas = []
        valores_cat_filtrados = []
        
        for c, v in zip(categorias, valores_cat):
            if v > 0:
                categorias_filtradas.append(c)
                valores_cat_filtrados.append(v)
        
        return categorias_filtradas, valores_cat_filtrados