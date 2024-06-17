from typing import List
from card import Deck
from player import Player, Bank
from hand import Hand


class BlackJackGame:
    """Represents the Black Jack game."""

    def __init__(self, players: List[Player]) -> None:
        """Initializes the game with a list of players and a bank."""
        self.players = players
        self.bank = Bank()
        self.deck = Deck()
        self.round_over = False

    def start_round(self) -> None:
        """Starts a new round by dealing initial cards and placing bets."""
        self.round_over = False
        self.deck = (
            Deck()
        )  # Reinitialize deck at the start of each round, shared deck for the table
        for player in self.players:
            player.hand = Hand()
            player.hand.start_hand(self.deck)

        self.bank.hand = Hand()
        self.bank.hand.start_hand(self.deck)

    def player_turn(self, player: Player) -> None:
        """Handles the turn logic for a player."""
        if player.hand.is_busted():
            self.round_over = True

    def bank_turn(self) -> None:
        """Handles the turn logic for the bank."""
        while self.bank.hand.calculate_value() < 17:
            self.bank.hand.add_card(self.deck.deal())

    def determine_winner(self) -> None:
        """Determines the winner of the round."""
        if self.bank.hand.is_busted():
            for player in self.players:
                if not player.hand.is_busted():
                    player.win_bet()
            return

        bank_value = self.bank.hand.calculate_value()
        for player in self.players:
            if player.hand.is_busted():
                continue
            player_value = player.hand.calculate_value()
            if player_value > bank_value:
                player.win_bet()
            elif player_value < bank_value:
                player.lose_bet()
            else:
                player.push_bet()

    def play_round(self) -> None:
        """Plays a round of Black Jack."""
        self.start_round()
        for player in self.players:
            self.player_turn(player)
            if self.round_over:
                return
        self.bank_turn()
        self.determine_winner()
