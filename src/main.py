from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QFormLayout,
)
from PySide6.QtCore import Slot
from game import BlackJackGame
from player import Player


class BlackJackUI(QMainWindow):
    """Represents the UI for the Black Jack game."""

    def __init__(self) -> None:
        """Initializes the UI without game instance initially."""
        super().__init__()
        self.players = []
        self.current_player_index = -1
        self.initUI()

    def initUI(self) -> None:
        """Initializes the UI components."""
        self.setWindowTitle("Black Jack Game")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.info_label = QLabel("Enter player details to start the game:")
        self.layout.addWidget(self.info_label)

        self.player_form_layout = QFormLayout()
        self.player_name_input = QLineEdit()
        self.player_money_input = QLineEdit()
        self.player_form_layout.addRow("Player Name:", self.player_name_input)
        self.player_form_layout.addRow("Initial Money:", self.player_money_input)

        self.layout.addLayout(self.player_form_layout)

        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        self.layout.addWidget(self.add_player_button)

        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_game_button)

        self.bet_layout = QHBoxLayout()
        self.bet_inputs = {}

        self.start_button = QPushButton("Start Round")
        self.start_button.clicked.connect(self.start_round)
        self.start_button.setEnabled(False)
        self.layout.addWidget(self.start_button)

        self.action_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.setEnabled(False)

        self.stand_button = QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        self.stand_button.setEnabled(False)

        self.action_layout.addWidget(self.hit_button)
        self.action_layout.addWidget(self.stand_button)
        self.layout.addLayout(self.action_layout)

        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        self.central_widget.setLayout(self.layout)

    @Slot()
    def add_player(self) -> None:
        """Adds a player to the game."""
        player_name = self.player_name_input.text()
        try:
            player_money = int(self.player_money_input.text())
            if player_name and player_money > 0:
                if player_name in [player.name for player in self.players]:
                    QMessageBox.warning(
                        self, "Duplicate Name", "Player name already exists."
                    )
                else:
                    self.players.append(Player(name=player_name, money=player_money))
                    self.info_label.setText(
                        f"Player {player_name} added with ${player_money}."
                    )
                    self.player_name_input.clear()
                    self.player_money_input.clear()
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Input",
                    "Please enter a valid name and positive money amount.",
                )
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a valid name and positive money amount.",
            )

    @Slot()
    def start_game(self) -> None:
        """Starts the game with the added players."""
        if not self.players:
            QMessageBox.warning(
                self,
                "No Players",
                "Please add at least one player before starting the game.",
            )
            return

        self.game = BlackJackGame(self.players)
        self.info_label.setText("Game started. Place your bets.")
        self.update_bet_layout()
        self.start_button.setEnabled(True)
        self.add_player_button.setEnabled(False)
        self.start_game_button.setEnabled(False)

    def update_bet_layout(self) -> None:
        """Updates the layout to include bet inputs for each player."""
        for player in self.players:
            player_label = QLabel(f"{player.name}'s bet: ")
            player_input = QLineEdit()
            self.bet_inputs[player.name] = player_input
            self.bet_layout.addWidget(player_label)
            self.bet_layout.addWidget(player_input)

        self.layout.addLayout(self.bet_layout)

    def start_round(self) -> None:
        """Starts a new round and updates the UI."""
        for player in self.players:
            try:
                bet_amount = int(self.bet_inputs[player.name].text())
                player.place_bet(bet_amount)
            except ValueError:
                QMessageBox.warning(
                    self, "Invalid Bet", f"Invalid bet amount for {player.name}."
                )
                return

        self.game.start_round()
        self.current_player_index = 0  # Reset player index at the start of the round
        self.update_info()
        self.enable_player_actions()

    def enable_player_actions(self) -> None:
        """Enables the hit and stand buttons for the current player."""
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.update_info()

    def disable_player_actions(self) -> None:
        """Disables the hit and stand buttons."""
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    @Slot()
    def hit(self) -> None:
        """Handles the hit action for the current player."""
        player = self.game.players[self.current_player_index]
        player.hand.add_card(self.game.deck.deal())
        self.update_info()
        if player.hand.is_busted():
            self.disable_player_actions()
            QMessageBox.information(self, "Bust", f"{player.name} busts!")
            player.lose_bet()
            self.next_player_turn()

    @Slot()
    def stand(self) -> None:
        """Handles the stand action for the current player."""
        self.disable_player_actions()
        self.next_player_turn()

    def next_player_turn(self) -> None:
        """Moves to the next player's turn."""
        self.current_player_index += 1
        if self.current_player_index < len(self.game.players):
            self.enable_player_actions()
        else:
            self.bank_turn()

    def bank_turn(self) -> None:
        """Handles the bank's turn."""
        self.game.bank_turn()
        self.update_info()
        self.determine_winner()

    def determine_winner(self) -> None:
        """Determines the winner and updates the UI."""
        self.game.determine_winner()
        self.update_info()
        for player in self.game.players:
            if (
                player.hand.calculate_value() > self.game.bank.hand.calculate_value()
                and not player.hand.is_busted()
            ):
                QMessageBox.information(self, "Winner", f"{player.name} wins!")
        self.reset_game()

    @Slot()
    def reset_game(self) -> None:
        """Resets the game to initial state."""
        self.players = []
        self.bet_inputs = {}
        self.info_label.setText("Enter player details to start the game:")
        self.start_button.setEnabled(False)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.add_player_button.setEnabled(True)
        self.start_game_button.setEnabled(True)

        # Clear layout for bets
        for i in reversed(range(self.bet_layout.count())):
            widget = self.bet_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.update_info()

    def update_info(self) -> None:
        """Updates the information displayed in the UI."""
        info_text = ""
        if self.players:
            for player in self.players:
                info_text += f"{player.name}: {player.hand} - Money: ${player.money}\n"
            if self.current_player_index >= len(self.game.players):
                info_text += f"Bank: {self.game.bank.hand}\n"
        self.info_label.setText(info_text)


if __name__ == "__main__":
    app = QApplication([])

    ui = BlackJackUI()
    ui.show()
    app.exec_()
