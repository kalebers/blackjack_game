from src.card import Card
from src.hand import Hand


def test_hand_initialization():
    hand = Hand()
    assert hand.cards == []


def test_add_card():
    hand = Hand()
    card = Card("Hearts", "A")
    hand.add_card(card)
    assert hand.cards == [card]


def test_calculate_value_no_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "2"))
    hand.add_card(Card("Spades", "3"))
    assert hand.calculate_value() == 5


def test_calculate_value_with_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "A"))
    hand.add_card(Card("Spades", "9"))
    assert hand.calculate_value() == 20


def test_calculate_value_with_multiple_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "A"))
    hand.add_card(Card("Spades", "A"))
    hand.add_card(Card("Clubs", "9"))
    assert hand.calculate_value() == 21


def test_calculate_value_busting_with_aces():
    hand = Hand()
    hand.add_card(Card("Hearts", "A"))
    hand.add_card(Card("Spades", "A"))
    hand.add_card(Card("Clubs", "9"))
    hand.add_card(Card("Diamonds", "5"))
    assert hand.calculate_value() == 16


def test_is_busted():
    hand = Hand()
    hand.add_card(Card("Hearts", "10"))
    hand.add_card(Card("Spades", "10"))
    hand.add_card(Card("Clubs", "5"))
    assert hand.is_busted() is True

    hand = Hand()
    hand.add_card(Card("Hearts", "10"))
    hand.add_card(Card("Spades", "9"))
    assert hand.is_busted() is False


def test_hand_str():
    hand = Hand()
    hand.add_card(Card("Hearts", "A"))
    hand.add_card(Card("Spades", "9"))
    assert str(hand) == "A of Hearts, 9 of Spades (value: 20)"

    hand.add_card(Card("Clubs", "2"))
    assert str(hand) == "A of Hearts, 9 of Spades, 2 of Clubs (value: 22)"  # value: 12
