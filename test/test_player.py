import pytest
from src.player import Player, Bank
from src.hand import Hand
from src.card import Deck


def test_player_initialization():
    player = Player("Alice", 100)
    assert player.name == "Alice"
    assert player.money == 100
    assert isinstance(player.hand, Hand)
    assert isinstance(player.deck, Deck)
    assert player.bet == 0


def test_place_bet():
    player = Player("Alice", 100)
    player.place_bet(50)
    assert player.bet == 50
    with pytest.raises(ValueError):
        player.place_bet(200)  # Bet exceeds available money


def test_win_bet():
    player = Player("Alice", 100)
    player.place_bet(50)
    player.win_bet()
    assert player.money == 150


def test_lose_bet():
    player = Player("Alice", 100)
    player.place_bet(50)
    player.lose_bet()
    assert player.money == 50


def test_push_bet():
    player = Player("Alice", 100)
    player.place_bet(50)
    player.push_bet()
    assert player.money == 100  # Money remains the same after push bet


def test_bank_initialization():
    bank = Bank()
    assert bank.name == "Bank"
    assert bank.money == float("inf")
    assert isinstance(bank.hand, Hand)
    assert isinstance(bank.deck, Deck)
    assert bank.bet == 0


def test_bank_no_betting():
    bank = Bank()
    bank.place_bet(100)
    bank.win_bet()
    bank.lose_bet()
    bank.push_bet()
    assert bank.money == float(
        "inf"
    )  # Bank's money remains infinite regardless of bets
