from database.di_container import DIContainer
from models.despesa import Despesa
from models.receita import Receita
from models.transacao import Transacao


class Estatisticas():
    def __init__(self, di_container: DIContainer = None):
        self.__di_container = di_container
        self.__transacoes = self.__di_container.transacao_repository.get_current_month_transactions(self.__di_container.usuario_ativo.id)
        self.__receitas = [t for t in self.__transacoes if isinstance(t, Receita)]
        self.__despesas = [t for t in self.__transacoes if isinstance(t, Despesa)]
        self.__total_receitas = sum(r.get_valor_com_sinal() for r in self.__receitas)
        self.__total_despesas = sum(d.get_valor_com_sinal() for d in self.__despesas)
        self.__qntd_receitas = len(self.__receitas)
        self.__qntd_despesas = len(self.__despesas)
        self.__porcentagem_gasta = 0 if self.__total_receitas == 0 else (abs(self.__total_despesas) / self.__total_receitas) * 100
        self.__economia_percentual = 100 - self.__porcentagem_gasta
        self.__saldo_restante = 0 if (self.__total_receitas + self.__total_despesas) <= 0 else self.__total_receitas + self.__total_despesas  

    @property
    def receitas(self):
        return self.__receitas.copy()

    @property
    def despesas(self):
        return self.__despesas.copy()

    @property
    def total_receitas(self):
        return self.__total_receitas

    @property
    def total_despesas(self):
        return self.__total_despesas

    @property
    def qntd_receitas(self):
        return self.__qntd_receitas

    @property
    def qntd_despesas(self):
        return self.__qntd_despesas

    @property
    def porcentagem_gasta(self):
        return self.__porcentagem_gasta

    @property
    def economia_percentual(self):
        return self.__economia_percentual

    @property
    def saldo_restante(self):
        return self.__saldo_restante