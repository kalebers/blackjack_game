import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.ui import BlackJackUI
from src.game import BlackJackGame


@pytest.fixture
def app(qtbot):
    """Fixture to create the application."""
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    ui = BlackJackUI()
    qtbot.addWidget(ui)
    return ui, qtbot


def test_add_player(app):
    ui, qtbot = app

    # Set player name and money
    qtbot.keyClicks(ui.player_name_input, "John Doe")
    qtbot.keyClicks(ui.player_money_input, "1000")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)

    assert len(ui.players) == 1
    assert ui.players[0].name == "John Doe"
    assert ui.players[0].money == 1000
    assert ui.info_label.text() == "Player John Doe added with $1000."


def test_start_game_without_players(app):
    ui, qtbot = app

    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)

    assert (
        "Please add at least one player before starting the game."
        in ui.info_label.text()
    )


def test_start_game_with_players(app):
    ui, qtbot = app

    # Add a player
    qtbot.keyClicks(ui.player_name_input, "Jane Doe")
    qtbot.keyClicks(ui.player_money_input, "2000")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)

    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)

    assert isinstance(ui.game, BlackJackGame)
    assert ui.start_button.isEnabled()
    assert ui.info_label.text() == "Game started. Place your bets."


def test_start_round_with_valid_bets(app):
    ui, qtbot = app

    # Add a player and start game
    qtbot.keyClicks(ui.player_name_input, "Alice")
    qtbot.keyClicks(ui.player_money_input, "1500")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)
    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)

    # Place a valid bet and start round
    qtbot.keyClicks(ui.bet_inputs["Alice"], "100")
    qtbot.mouseClick(ui.start_button, Qt.LeftButton)

    assert ui.game.players[0].bet == 100
    assert ui.hit_button.isEnabled()
    assert ui.stand_button.isEnabled()


def test_start_round_with_invalid_bet(app):
    ui, qtbot = app

    # Add a player and start game
    qtbot.keyClicks(ui.player_name_input, "Bob")
    qtbot.keyClicks(ui.player_money_input, "1500")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)
    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)

    # Place an invalid bet and try to start round
    qtbot.keyClicks(ui.bet_inputs["Bob"], "not_a_number")
    qtbot.mouseClick(ui.start_button, Qt.LeftButton)

    assert "Invalid bet amount for Bob." in ui.info_label.text()
    assert not ui.game.players[0].bet


def test_player_hits(app):
    ui, qtbot = app

    # Add a player and start game
    qtbot.keyClicks(ui.player_name_input, "Charlie")
    qtbot.keyClicks(ui.player_money_input, "1500")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)
    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)
    qtbot.keyClicks(ui.bet_inputs["Charlie"], "100")
    qtbot.mouseClick(ui.start_button, Qt.LeftButton)

    # Simulate a hit action
    qtbot.mouseClick(ui.hit_button, Qt.LeftButton)

    player = ui.game.players[0]
    assert len(player.hand.cards) == 1  # Assumes hand starts empty
    assert ui.hit_button.isEnabled()
    assert ui.stand_button.isEnabled()


def test_player_stands(app):
    ui, qtbot = app

    # Add a player and start game
    qtbot.keyClicks(ui.player_name_input, "David")
    qtbot.keyClicks(ui.player_money_input, "1500")
    qtbot.mouseClick(ui.add_player_button, Qt.LeftButton)
    qtbot.mouseClick(ui.start_game_button, Qt.LeftButton)
    qtbot.keyClicks(ui.bet_inputs["David"], "100")
    qtbot.mouseClick(ui.start_button, Qt.LeftButton)

    # Simulate a stand action
    qtbot.mouseClick(ui.stand_button, Qt.LeftButton)

    assert not ui.hit_button.isEnabled()
    assert not ui.stand_button.isEnabled()
    assert ui.current_player_index == 1  # Assumes only one player


if __name__ == "__main__":
    pytest.main()
