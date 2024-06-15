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
        self.round_over = False

    def start_round(self) -> None:
        """Starts a new round by dealing initial cards and placing bets."""
        self.round_over = False
        for player in self.players:
            player.deck = (
                Deck()
            )  # Reinitialize player's deck at the start of each round
            player.hand = Hand()
            player.place_bet(int(input(f"{player.name}, place your bet: ")))
            player.hand.add_card(player.deck.deal())
            player.hand.add_card(player.deck.deal())

        self.bank.deck = Deck()  # Reinitialize bank's deck at the start of each round
        self.bank.hand = Hand()
        self.bank.hand.add_card(self.bank.deck.deal())
        self.bank.hand.add_card(self.bank.deck.deal())

    def player_turn(self, player: Player) -> None:
        """Handles the turn logic for a player."""
        while True:
            print(f"{player.name}'s hand: {player.hand}")
            if player.hand.is_busted():
                print(f"{player.name} busts!")
                player.lose_bet()
                self.round_over = True
                return

            action = input(f"{player.name}, do you want to hit or stand? ").lower()
            if action == "hit":
                player.hand.add_card(player.deck.deal())
            elif action == "stand":
                break
            else:
                print("Invalid action. Please choose 'hit' or 'stand'.")

    def bank_turn(self) -> None:
        """Handles the turn logic for the bank."""
        print(f"Bank's hand: {self.bank.hand}")
        while self.bank.hand.calculate_value() < 17:
            self.bank.hand.add_card(self.bank.deck.deal())
            print(f"Bank's hand: {self.bank.hand}")
            if self.bank.hand.is_busted():
                print("Bank busts!")
                for player in self.players:
                    if not player.hand.is_busted():
                        player.win_bet()
                return

    def determine_winner(self) -> None:
        """Determines the winner of the round."""
        if self.bank.hand.is_busted():
            return  # Winners already determined in bank_turn

        bank_value = self.bank.hand.calculate_value()
        for player in self.players:
            if player.hand.is_busted():
                continue
            player_value = player.hand.calculate_value()
            if player_value > bank_value:
                player.win_bet()
                print(f"{player.name} wins!")
            elif player_value < bank_value:
                player.lose_bet()
                print(f"{player.name} loses!")
            else:
                player.push_bet()
                print(f"{player.name} pushes!")

    def play_round(self) -> None:
        """Plays a round of Black Jack."""
        self.start_round()
        for player in self.players:
            self.player_turn(player)
            if self.round_over:
                return
        self.bank_turn()
        self.determine_winner()
