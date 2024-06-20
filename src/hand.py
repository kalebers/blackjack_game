from typing import List
from card import Card


class Hand:
    """Represents a hand of playing cards."""

    def __init__(self) -> None:
        """Initializes an empty hand."""
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        """Adds a card to the hand."""
        self.cards.append(card)

    def calculate_value(self) -> int:
        """Calculates the value of the hand. Adjusts for aces if the total value exceeds 21."""
        total = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == "A")
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        return total

    def is_busted(self) -> bool:
        """Returns True if the hand's value exceeds 21."""
        return self.calculate_value() > 21

    def start_hand(self, deck) -> None:
        """Starts the hand by dealing two cards from the given deck."""
        self.cards = [deck.deal(), deck.deal()]

    def __str__(self) -> str:
        """Returns a string representation of the hand."""
        return (
            ", ".join(str(card) for card in self.cards)
            + f" (value: {self.calculate_value()})"
        )
