from PySide6.QtWidgets import QApplication
from ui import BlackJackUI

if __name__ == "__main__":
    app = QApplication([])

    ui = BlackJackUI()
    ui.show()
    app.exec()
