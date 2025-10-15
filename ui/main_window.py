# main.py (localizado em GESTOR-DESPESAS/main.py)
import sys
from PySide6.QtWidgets import QApplication
from Login import TelaLogin  # Importa a partir do pacote 'ui'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela_login = TelaLogin()
    janela_login.show()
    sys.exit(app.exec())
