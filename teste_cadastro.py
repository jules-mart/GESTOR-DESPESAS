# teste_cadastro.py
import sys
from PySide6.QtWidgets import QApplication
from ui.Cadastro import TelaCadastro  # Importa a sua tela de cadastro

# Este ficheiro serve apenas para testar a janela de cadastro de forma isolada.

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cria e exibe apenas a janela de cadastro
    janela_teste = TelaCadastro()
    janela_teste.show()

    sys.exit(app.exec())
