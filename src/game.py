from player import Player, Bank
from card import Deck
from hand import Hand


class BlackJackGame:
    """Represents the Black Jack game."""

    def __init__(self, players: list[Player]) -> None:
        """Initializes the game with a list of players and a shared deck."""
        self.players = players
        self.bank = Bank()
        self.deck = Deck()
        self.deck.shuffle()

    def start_round(self) -> None:
        """Starts a new round, dealing initial cards to players and the bank."""
        for player in self.players:
            player.hand = Hand()
            player.hand.add_card(self.deck.deal())
            player.hand.add_card(self.deck.deal())

        self.bank.hand = Hand()
        self.bank.hand.add_card(self.deck.deal())
        self.bank.hand.add_card(self.deck.deal())

    def bank_turn(self) -> None:
        """Performs the bank's turn."""
        while self.bank.hand.calculate_value() < 17:
            self.bank.hand.add_card(self.deck.deal())

    def determine_winner(self) -> None:
        """Determines the winner after the bank's turn."""
        bank_value = self.bank.hand.calculate_value()
        for player in self.players:
            player_value = player.hand.calculate_value()
            if player.hand.is_busted():
                player.lose_bet()
            elif self.bank.hand.is_busted() or player_value > bank_value:
                player.win_bet()
            elif player_value < bank_value:
                player.lose_bet()
            else:
                player.push_bet()
            player.reset_bet()
