# teste_cadastro.py
import sys
from PySide6.QtWidgets import QApplication
from database.db_session import init_db
from di_container import DIContainer
from ui.Login import TelaLogin
from ui.main_window import AppController


if __name__ == "__main__":
    init_db()

    di = DIContainer()
    controller = AppController(di)
    controller.run()
