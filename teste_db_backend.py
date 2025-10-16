from database.db_session import init_db
from di_container import DIContainer
from models.despesa import Despesa
from models.receita import Receita
from models.usuario import Usuario

if __name__ == "__main__":
    init_db()

    container = DIContainer()

    usu = Usuario(nome="Jose", idade=22, email="teste@gmail.com")
    income = Receita(descricao="Freelance project", valor=1200, usuario=usu)
    outcome = Despesa(descricao="Rent payment", valor=800, usuario=usu)

    container.transacao_repository.add(income)
    container.transacao_repository.add(outcome)