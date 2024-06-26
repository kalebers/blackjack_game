from PySide6.QtWidgets import QMessageBox, QListWidgetItem, QLabel, QLineEdit
from PySide6.QtCore import Slot
from game import BlackJackGame
from player import Player


class BlackJackUIHandlers:
    @Slot()
    def add_player(self) -> None:
        """Adds a player to the game."""
        player_name = self.player_name_input.text()
        try:
            player_money = int(self.player_money_input.text())
            if player_name and player_money > 0:
                if player_name in [player.name for player in self.players]:
                    QMessageBox.warning(
                        self, "Duplicate Name", "Player name already exists."
                    )
                else:
                    self.players.append(Player(name=player_name, money=player_money))
                    self.info_label.setText(
                        f"Player {player_name} added with ${player_money}."
                    )
                    self.player_name_input.clear()
                    self.player_money_input.clear()
                    self.update_player_list()
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a valid name and positive money amount.",
            )

    def update_player_list(self) -> None:
        """Updates the player list displayed in the UI."""
        self.player_list.clear()
        for player in self.players:
            item = QListWidgetItem(f"{player.name}: ${player.money}")
            self.player_list.addItem(item)

    @Slot()
    def start_game(self) -> None:
        """Starts the game after players are added."""
        if not self.players:
            QMessageBox.warning(
                self,
                "No Players",
                "Please add at least one player before starting the game.",
            )
            return
        self.game = BlackJackGame(self.players)
        self.info_label.setText("Game started. Place your bets.")
        self.update_bet_layout()
        self.start_button.setEnabled(True)
        self.add_player_button.setEnabled(False)
        self.start_game_button.setEnabled(False)
        # Hide player input fields and labels
        self.player_name_input.setVisible(False)
        self.player_money_input.setVisible(False)
        self.player_name_label.setVisible(False)
        self.player_money_label.setVisible(False)
        self.add_player_button.setVisible(False)

    def update_bet_layout(self) -> None:
        """Updates the layout with betting inputs for each player."""
        for player in self.players:
            player_label = QLabel(f"{player.name}'s bet: ")
            player_input = QLineEdit()
            self.bet_inputs[player.name] = player_input
            self.bet_layout.addWidget(player_label)
            self.bet_layout.addWidget(player_input)
        self.layout.addLayout(self.bet_layout)

    @Slot()
    def start_round(self) -> None:
        """Starts a new round after bets are placed."""
        for player in self.players:
            try:
                bet_amount = int(self.bet_inputs[player.name].text())
                player.place_bet(bet_amount)
            except ValueError:
                QMessageBox.warning(
                    self, "Invalid Bet", f"Invalid bet amount for {player.name}."
                )
                return
        self.game.start_round()
        self.current_player_index = 0
        self.update_info()
        self.update_player_list()
        self.enable_player_actions()

    def enable_player_actions(self) -> None:
        """Enables the hit and stand buttons for the current player."""
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.update_info()

    def disable_player_actions(self) -> None:
        """Disables the hit and stand buttons."""
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    @Slot()
    def hit(self) -> None:
        """Handles the hit action for the current player."""
        player = self.game.players[self.current_player_index]
        player.hand.add_card(self.game.deck.deal())
        self.update_info()
        if player.hand.is_busted():
            self.disable_player_actions()
            QMessageBox.information(self, "Bust", f"{player.name} busts!")
            player.lose_bet()
            self.next_player_turn()

    @Slot()
    def stand(self) -> None:
        """Handles the stand action for the current player."""
        self.disable_player_actions()
        self.next_player_turn()

    def next_player_turn(self) -> None:
        """Moves to the next player's turn."""
        self.current_player_index += 1
        if self.current_player_index < len(self.game.players):
            self.enable_player_actions()
            self.update_info()  # Update info without showing all bank cards
        else:
            self.bank_turn()
            self.update_info(True)

    def bank_turn(self) -> None:
        """Handles the bank's turn."""
        # Skip bank turn if all players are busted
        if all(player.hand.is_busted() for player in self.game.players):
            self.determine_winner()
            return
        self.game.bank_turn()
        self.update_info(True)  # Show all bank cards after bank's turn
        self.determine_winner()

    def determine_winner(self) -> None:
        """Determines the winner and updates the UI."""
        self.game.determine_winner()
        self.update_info(True)  # Show all bank cards

        self.update_player_list()  # Update player money in the list

        for player in self.game.players:
            player_value = player.hand.calculate_value()
            bank_value = self.game.bank.hand.calculate_value()

            if player.hand.is_busted():
                message = f"{player.name} busts!"
            elif self.game.bank.hand.is_busted():
                message = f"{player.name} wins! Bank busts!"
            elif player_value > bank_value:
                message = f"{player.name} wins!"
            elif player_value < bank_value:
                message = f"{player.name} loses!"
            else:
                message = f"{player.name} pushes!"  # when both values are equal

            QMessageBox.information(self, "Result", message)

        self.reset_game_prompt()

    @Slot()
    def reset_game_prompt(self) -> None:
        """Prompts the user to reset the game after a round."""
        reply = QMessageBox.question(
            self,
            "Reset Game",
            "Do you want to reset the game?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.reset_game()

    @Slot()
    def reset_game(self) -> None:
        """Resets the game to its initial state."""
        self.players.clear()
        self.current_player_index = -1
        self.info_label.setText("Enter player details to start the game.")
        self.start_button.setEnabled(False)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.add_player_button.setEnabled(True)
        self.start_game_button.setEnabled(True)
        # Show player input fields and labels
        self.player_name_input.setVisible(True)
        self.player_money_input.setVisible(True)
        self.player_name_label.setVisible(True)
        self.player_money_label.setVisible(True)
        self.add_player_button.setVisible(True)
        # Clear layout for betting inputs
        for i in reversed(range(self.bet_layout.count())):
            widget = self.bet_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.bet_inputs.clear()
        self.update_player_list()

    def update_info(self, show_all_bank_cards: bool = False) -> None:
        """Updates the information label with the current game state."""
        info_text = "<html><body>"
        for index, player in enumerate(self.game.players):
            player_hand = ", ".join(map(str, player.hand.cards))
            player_value = player.hand.calculate_value()
            bold_name = f"<b>{player.name}</b>"
            current_indicator = (
                "<span style='color:red'> (Current Player)</span>"
                if index == self.current_player_index
                else ""
            )
            info_text += f"{bold_name}{current_indicator}<br>{player_hand} (Value: {player_value})<br><br>"

        bank_hand = (
            ", ".join(map(str, self.game.bank.hand.cards[:1])) + ", [Hidden]"
            if not show_all_bank_cards
            else ", ".join(map(str, self.game.bank.hand.cards))
        )
        bank_value = (
            self.game.bank.hand.calculate_value() if show_all_bank_cards else "?"
        )
        info_text += f"<b>Bank</b><br>{bank_hand} (Value: {bank_value})"

        info_text += "</body></html>"

        self.info_label.setText(info_text)
