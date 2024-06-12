import random
from typing import List

class Card:
    """Represents a single playing card."""

    def __init__(self, suit: str, rank: str) -> None:
        """Initializes the card with a suit and a rank."""
        self.suit = suit
        self.rank = rank

    def value(self) -> int:
        """
        Returns the value of the card.
        Number cards have their face value, face cards have a value of 10,
        and the ace can have a value of 11.
        """
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Initially consider Ace as 11
        else:
            return int(self.rank)

    def __str__(self) -> str:
        """Returns a string representation of the card."""
        return f"{self.rank} of {self.suit}"


class Deck:
    """Represents a deck of 52 playing cards."""

    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self) -> None:
        """Initializes the deck with 52 shuffled cards."""
        self.cards: List[Card] = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """Deals a card from the deck."""
        return self.cards.pop()
