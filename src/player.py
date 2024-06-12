from hand import Hand

class Player:
    """Represents a player in the Black Jack game."""

    def __init__(self, name: str, money: int) -> None:
        """Initializes a player with a name and money."""
        self.name = name
        self.money = money
        self.hand = Hand()
        self.bet = 0

    def place_bet(self, amount: int) -> None:
        """
        Places a bet for the player.
        Raises ValueError if the bet amount exceeds the player's money.
        """
        if amount > self.money:
            raise ValueError("Bet amount exceeds available money")
        self.bet = amount

    def win_bet(self) -> None:
        """Increases the player's money by the bet amount."""
        self.money += self.bet

    def lose_bet(self) -> None:
        """Decreases the player's money by the bet amount."""
        self.money -= self.bet

    def push_bet(self) -> None:
        """Player neither wins nor loses money."""
        pass


class Bank(Player):
    """Represents the bank in the Black Jack game."""

    def __init__(self) -> None:
        """Initializes the bank with infinite money."""
        super().__init__(name="Bank", money=float('inf'))
