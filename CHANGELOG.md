# **Ongoing Version**
- Version 0.8 released on **26 June 2024**

- **Fixes**:
    - UI class clean for better maintenance.
    - Player class fix on money loss when player loses the bet.
    - ui_handler class addition for bank turn to ensure that when the player(s) go over 21, the bank turn is skipped.

# Version 0.7 released on **25 June 2024**

- **Fixes**:
    - Remove bet and player money from status.
    - Money bet loss after losing a turn.
    - Improved how current player is shown.

# Version 0.6 released on **23 June 2024**

- **Fixes**:
    - Bold player name turn (who is in the current turn).
    - ⁠⁠Skip bank turn if all players have been over 21.
    - Creation of function in order to update current money and current player.

# Version 0.5 released on **20 June 2024**

- **Fixes**:
    - UI player list.
    - Change of execution function on main.
    - Player hand value on display.

# Version 0.4 released on **19 June 2024**

- **Additions**:
    - ui_handler and ui classes to divide main code structure for maintainability.

- **Fixes**:
    - UI fixed: updates the player hand and hides one of the bank cards.

# Version 0.3 released on **17 June 2024**

- **Additions**:
    - New working prototype of UI.

- **Fixes**:
    - Player starting hand with 2 cards
    - Table deck fixed.

# Version 0.2 released on **14 June 2024**
- **Additions**:
    - Support for multiplayers.
- **Fixes**:
    - UI, game and player class fixes for multiplayer support.
    - Game file fix that ensures that each player has a new deck on the beginning of each game.

# Version 0.1 released on **13 June 2024**

- **Additions**:
    - First draft of the card/deck handler for the game.
    - Addition of hand handler for each round.
    - Addition of unittests for each of the classes.
    - Addition of readme file whith explanation on how to setup the environment.
