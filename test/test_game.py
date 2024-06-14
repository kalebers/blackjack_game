import pytest
from unittest.mock import patch, MagicMock
from src.card import Card, Deck
from src.player import Player, Bank
from src.hand import Hand
from src.game import BlackJackGame

def test_blackjackgame_initialization():
    player1 = Player("Alice", 100)
    player2 = Player("Bob", 100)
    game = BlackJackGame([player1, player2])
    assert game.players == [player1, player2]
    assert isinstance(game.bank, Bank)
    assert game.round_over == False

@patch('builtins.input', side_effect=['10', '10'])
def test_start_round(mock_input):
    player1 = Player("Alice", 100)
    player2 = Player("Bob", 100)
    game = BlackJackGame([player1, player2])
    
    game.start_round()

    for player in game.players:
        assert len(player.hand.cards) == 2
        assert player.bet == 10
        assert player.money == 90

    assert len(game.bank.hand.cards) == 2

@patch('builtins.input', side_effect=['stand'])
def test_player_turn_stand(mock_input):
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "7"))
    
    game.player_turn(player)

    assert player.hand.calculate_value() == 17

@patch('builtins.input', side_effect=['hit', 'stand'])
def test_player_turn_hit_and_stand(mock_input):
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "7"))
    player.deck = MagicMock()
    player.deck.deal.return_value = Card("Clubs", "2")
    
    game.player_turn(player)

    assert player.hand.calculate_value() == 19

@patch('builtins.input', side_effect=['hit', 'hit'])
def test_player_turn_bust(mock_input):
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "7"))
    player.deck = MagicMock()
    player.deck.deal.return_value = Card("Clubs", "5")
    
    game.player_turn(player)

    assert player.hand.is_busted()
    assert player.money == 90

def test_bank_turn():
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    game.bank.hand.add_card(Card("Hearts", "10"))
    game.bank.hand.add_card(Card("Spades", "6"))
    game.bank.deck = MagicMock()
    game.bank.deck.deal.return_value = Card("Clubs", "8")

    game.bank_turn()

    assert game.bank.hand.calculate_value() > 17

def test_determine_winner_player_wins():
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "8"))
    game.bank.hand.add_card(Card("Hearts", "10"))
    game.bank.hand.add_card(Card("Spades", "7"))

    game.determine_winner()

    assert player.money == 110

def test_determine_winner_bank_wins():
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "7"))
    game.bank.hand.add_card(Card("Hearts", "10"))
    game.bank.hand.add_card(Card("Spades", "8"))

    game.determine_winner()

    assert player.money == 90

def test_determine_winner_push():
    player = Player("Alice", 100)
    game = BlackJackGame([player])
    player.hand.add_card(Card("Hearts", "10"))
    player.hand.add_card(Card("Spades", "7"))
    game.bank.hand.add_card(Card("Hearts", "10"))
    game.bank.hand.add_card(Card("Spades", "7"))

    game.determine_winner()

    assert player.money == 100

@patch('builtins.input', side_effect=['10', '10', 'stand', 'stand'])
def test_play_round(mock_input):
    player1 = Player("Alice", 100)
    player2 = Player("Bob", 100)
    game = BlackJackGame([player1, player2])
    
    game.play_round()

    assert player1.money in [90, 100, 110]
    assert player2.money in [90, 100, 110]
    assert game.bank.hand.calculate_value() >= 17
