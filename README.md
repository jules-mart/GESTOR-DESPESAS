# GESTOR-DESPESAS

Aplicação desktop para gerenciamento financeiro pessoal, desenvolvida em Python com foco em Programação Orientada a Objetos (POO).

Este projeto permite que os usuários controlem suas finanças de forma intuitiva, registrando receitas e despesas, definindo limites de gastos por categoria, estabelecendo metas e visualizando um resumo completo de sua saúde financeira através de gráficos.

## ✨ Funcionalidades Principais

  * **Autenticação de Usuário**: Sistema de Login e Cadastro seguro.
  * **Dashboard (Resumo)**: Tela inicial com um resumo do mês, incluindo saldo atual, total de receitas, total de despesas e gráficos interativos que mostram a distribuição dos gastos.
  * **Gestão de Transações**:
      * **Receitas**: CRUD (Criar, Ler, Atualizar, Deletar) completo para receitas, com filtros por data e categoria.
      * **Despesas**: CRUD completo para despesas, com filtros por data, categoria e método de pagamento.
  * **Limites de Gastos**: Permite ao usuário definir limites de gastos mensais por categoria (ex: Alimentação, Transporte). A interface exibe o progresso de cada limite com gráficos circulares.
  * **Perfil do Usuário**: Permite ao usuário visualizar e atualizar suas informações pessoais (nome, profissão, renda, etc.).

## 🛠️ Tecnologias Utilizadas

O projeto foi construído com as seguintes tecnologias:

  * **Python 3.10+**
  * **PySide6**: Biblioteca oficial do Qt para Python, utilizada para a construção de toda a interface gráfica (UI).
  * **SQLAlchemy**: ORM para interação com o banco de dados.
  * **SQLite**: Banco de dados SQL leve e embarcado.
  * **Matplotlib**: Biblioteca utilizada para gerar os gráficos de resumo.
  * **bcrypt**: Biblioteca para hash e verificação segura de senhas.

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

  * Python 3.10 ou superior
  * Git

### 1\. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/GESTOR-DESPESAS.git
cd GESTOR-DESPESAS
```

### 2\. Criar e Ativar um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Instalar as Dependências

As dependências estão listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Executar a Aplicação

O ponto de entrada da aplicação é o arquivo `main.py`. Ele inicializa o banco de dados e abre a tela de login.

```bash
python main.py
```


-----
