from src.card import Card, Deck
import pytest


def test_card_initialization():
    card = Card("Hearts", "A")
    assert card.suit == "Hearts"
    assert card.rank == "A"


def test_card_value():
    card = Card("Hearts", "2")
    assert card.value() == 2

    card = Card("Hearts", "J")
    assert card.value() == 10

    card = Card("Hearts", "A")
    assert card.value() == 11


def test_card_str():
    card = Card("Hearts", "A")
    assert str(card) == "A of Hearts"


def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52


def test_deck_shuffle():
    deck = Deck()
    original_order = deck.cards[:]
    deck.shuffle()
    assert deck.cards != original_order  # Ensure deck is shuffled


def test_deck_deal():
    deck = Deck()
    dealt_card = deck.deal()
    assert isinstance(dealt_card, Card)
    assert len(deck.cards) == 51  # Ensure a card is removed from the deck


def test_deck_deal_all_cards():
    deck = Deck()
    dealt_cards = [deck.deal() for _ in range(52)]
    assert len(deck.cards) == 0  # Ensure all cards are dealt
    assert len(dealt_cards) == 52  # Ensure 52 cards are dealt
    with pytest.raises(IndexError):
        deck.deal()  # Ensure dealing from empty deck raises error
