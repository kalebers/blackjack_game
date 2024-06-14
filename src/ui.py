from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, QHBoxLayout
)
from game import BlackJackGame
from player import Player

class BlackJackUI(QMainWindow):
    """Represents the UI for the Black Jack game."""

    def __init__(self, game: BlackJackGame) -> None:
        """Initializes the UI with the game instance."""
        super().__init__()
        self.game = game
        self.initUI()

    def initUI(self) -> None:
        """Initializes the UI components."""
        self.setWindowTitle('Black Jack Game')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.info_label = QLabel('Welcome to Black Jack!')
        self.layout.addWidget(self.info_label)

        self.bet_layout = QHBoxLayout()
        self.bet_inputs = {}
        for player in self.game.players:
            player_label = QLabel(f"{player.name}'s bet: ")
            player_input = QLineEdit()
            self.bet_inputs[player.name] = player_input
            self.bet_layout.addWidget(player_label)
            self.bet_layout.addWidget(player_input)

        self.layout.addLayout(self.bet_layout)

        self.start_button = QPushButton('Start Round')
        self.start_button.clicked.connect(self.start_round)
        self.layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.layout)

    def start_round(self) -> None:
        """Starts a new round and updates the UI."""
        for player in self.game.players:
            bet_amount = int(self.bet_inputs[player.name].text())
            player.place_bet(bet_amount)
        self.game.play_round()
        self.update_info()

    def update_info(self) -> None:
        """Updates the information displayed in the UI."""
        info_text = ""
        for player in self.game.players:
            info_text += f"{player.name}: {player.hand} - Money: ${player.money}\n"
        info_text += f"Bank: {self.game.bank.hand}\n"
        self.info_label.setText(info_text)


if __name__ == '__main__':
    app = QApplication([])

    players = [Player(name="Alice", money=100), Player(name="Bob", money=100)]
    game = BlackJackGame(players)
    ui = BlackJackUI(game)

    ui.show()
    app.exec_()
