from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QFormLayout,
    QListWidget,
)

from ui_handler import BlackJackUIHandlers


class BlackJackUI(QMainWindow, BlackJackUIHandlers):
    """Represents the UI for the Black Jack game."""

    def __init__(self) -> None:
        """Initializes the UI components and the game state."""
        super().__init__()
        self.players = []
        self.current_player_index = -1
        self.initUI()
        self.player_init()
        self.start_stop_buttons()
        self.action_buttons()
        self.reset_button()

    def initUI(self) -> None:
        """Sets up the UI layout and components."""
        self.setWindowTitle("Black Jack Game")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Information label to display messages to the user
        self.info_label = QLabel("Enter player details to start the game:")
        self.layout.addWidget(self.info_label)

    def player_init(self) -> None:
        # Form layout to enter player name and initial money
        self.player_form_layout = QFormLayout()
        self.player_name_input = QLineEdit()
        self.player_money_input = QLineEdit()
        self.player_name_label = QLabel("Player Name:")
        self.player_money_label = QLabel("Initial Money:")
        self.player_form_layout.addRow(self.player_name_label, self.player_name_input)
        self.player_form_layout.addRow(self.player_money_label, self.player_money_input)
        self.layout.addLayout(self.player_form_layout)

        # Button to add a player
        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        self.layout.addWidget(self.add_player_button)

        # List to display added players
        self.player_list = QListWidget()
        self.layout.addWidget(self.player_list)

    def start_stop_buttons(self) -> None:
        # Button to start the game
        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_game_button)

        # Layout for betting inputs
        self.bet_layout = QHBoxLayout()
        self.bet_inputs = {}

        # Button to start a round
        self.start_button = QPushButton("Start Round")
        self.start_button.clicked.connect(self.start_round)
        self.start_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.start_button)

    def action_buttons(self) -> None:
        # Layout for action buttons (hit and stand)
        self.action_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.setEnabled(False)  # Initially disabled
        self.stand_button = QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        self.stand_button.setEnabled(False)  # Initially disabled
        self.action_layout.addWidget(self.hit_button)
        self.action_layout.addWidget(self.stand_button)
        self.layout.addLayout(self.action_layout)

    def reset_button(self) -> None:
        # Button to reset the game
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)
