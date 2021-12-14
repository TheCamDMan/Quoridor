# Author: Cameron Blankenship
# Date: 8/11/2021
# Description: A game of Quoridor with classes representing the board as
#              a 9 x 9 grid and two players. Players take turns either moving their pawn
#              one cell or placing a fence to block the movement of the other player.
#              If either player reaches the base line of the other player, the game is
#              won by that player.


class QuoridorGame:
    """Represents a Quoridor game that has a Board and two Players.
    Players take turns either moving or placing fences to block the
    other Player. If either Player reaches the base line of the other
    Player, the game is won by that Player.
    This class is responsible for initializing the game with a Board
    with two Players, and tracking Player turn. This class will have
    the Player class and Board class as data members, thus utilizing
    composition.
    """

    def __init__(self):
        """Initializes the game Board, Players 1 and 2, sets it as
        the first Player's turn."""
        self._P1 = Player(1)
        self._P2 = Player(2)
        self._Board = Board()
        self._player_turn = 1

    def get_board(self):
        """Returns the Board."""
        return self._Board

    def get_p1(self):
        """Returns Player 1."""
        return self._P1

    def get_p2(self):
        """Returns Player 2."""
        return self._P2

    def get_player_turn(self):
        """Returns player turn."""
        return self._player_turn

    def set_player_turn(self, player):
        """Sets turn to given Player."""
        self._player_turn = player

    def move_pawn(self, player_num, coordinates):
        """Moves the given Player to the given coordinates on the Board, if
        it is a valid move. If move is forbidden or game has already won,
        return False. Otherwise return True."""

        # no move may be played if game is already won
        if self.is_winner(1):
            return False
        if self.is_winner(2):
            return False

        # validates player move
        if not self.validate_pawn_move(player_num, coordinates):
            return False

        self.get_board().set_player_positions(player_num, coordinates)

        # updates player turn
        if player_num == 1:
            self.set_player_turn(2)
        else:
            self.set_player_turn(1)

        return True

    def place_fence(self, player_num, fence_type, coordinates):
        """Places a given Player's fence of given fence_type at the given
        coordinates, if it is a valid fence placement. If not a valid
        fence placement or game has already been won, return False.
        Otherwise return True."""

        # no move may be played if game is already won
        if self.is_winner(1):
            return False
        if self.is_winner(2):
            return False

        if player_num == 1:
            player = self.get_p1()
        else:
            player = self.get_p2()

        if not self.validate_fence_place(player_num, fence_type, coordinates):
            return False

        # adds the fence to corresponding fence type list
        if fence_type == "v":
            self.get_board().get_v_fence().append(coordinates)
        else:
            self.get_board().get_h_fence().append(coordinates)

        player.sub_fence_count()

        if player_num == 1:
            self.set_player_turn(2)
        else:
            self.set_player_turn(1)

        return True

    def validate_fence_place(self, player_num, fence_type, coordinates):
        """Validates the placement of the fences by ensuring that no fence
        is already at the given coordinates parameter, that the player has
        fences available to them, and that the fence is inbounds of the
        Board."""

        # checks if it is player's turn
        if self.get_player_turn() != player_num:
            return False

        # returns false if given an invalid fence_type
        if fence_type != "v" and fence_type != "h":
            return False

        # returns false if the player has no fences left
        if player_num == 1:
            player = self.get_p1()
        else:
            player = self.get_p2()
        if player.get_fence_count() < 1:
            return False

        # returns false if there is a fence already at the location or
        # if player tries to place a fence outside the border of the board
        if fence_type == "v":
            if coordinates in self.get_board().get_v_fence():
                return False
            if coordinates[0] < 0 or coordinates[0] > 9:
                return False
            if coordinates[1] < 0 or coordinates[1] > 8:
                return False
        if fence_type == "h":
            if coordinates in self.get_board().get_h_fence():
                return False
            if coordinates[0] < 0 or coordinates[0] > 8:
                return False
            if coordinates[1] < 0 or coordinates[1] > 9:
                return False

        return True

    def validate_pawn_move(self, player_num, coordinates):
        """Validates the Player move by ensuring that there is no fence
        blocking their path, that the move is inbounds of the board, and
        that the move is valid given the circumstance.
        Takes a coordinates parameter and player number."""

        # checks if it is player's turn
        if self.get_player_turn() != player_num:
            return False

        # initializes the position variables for ease of use
        positions = self.get_board().get_player_positions()

        # can't move pawn on top of other pawn
        if coordinates in positions:
            return False

        if player_num == 1:
            position = positions[0]
        else:
            position = positions[1]

        current_x = position[0]
        current_y = position[1]
        future_x = coordinates[0]
        future_y = coordinates[1]

        # checks if player tries to move too many spaces
        if abs(future_x - current_x) > 2:
            return False
        if abs(future_y - current_y) > 2:
            return False

        # checks if player is moving diagonal
        if future_x != current_x and future_y != current_y:
            if player_num == 1:
                opponent_pos = positions[1]
            else:
                opponent_pos = positions[0]

            # checks to see if there is a fence in the way
            if future_x > current_x:  # if moving right
                if (future_x, future_y) in self.get_board().get_v_fence():
                    return False

            elif future_x < current_x:  # if moving left
                if (current_x, current_y) in self.get_board().get_v_fence():
                    return False

            elif future_y > current_y:  # if moving down
                if (future_x, future_y) in self.get_board().get_h_fence():
                    return False

            elif future_y < current_y:  # if moving up
                if (current_x, current_y) in self.get_board().get_h_fence():
                    return False

            # validates the diagonal movement
            return self.diagonal_validation(
                current_x, current_y, future_x, future_y, opponent_pos
            )

        # not moving diagonal
        if player_num == 1:
            opponent_pos = positions[1]
        else:
            opponent_pos = positions[0]

        # not moving diagonal, checks if fence in the way
        if future_x > current_x:  # if moving right
            if (future_x, future_y) in self.get_board().get_v_fence():
                return False

        elif future_x < current_x:  # if moving left
            if (current_x, current_y) in self.get_board().get_v_fence():
                return False

        elif future_y > current_y:  # if moving down
            if (future_x, future_y) in self.get_board().get_h_fence():
                return False

        elif future_y < current_y:  # if moving up
            if (current_x, current_y) in self.get_board().get_h_fence():
                return False

        # returns False if player tries to jump and opponent is not in the way or there
        # is a fence in the way
        if future_x - current_x == 2:
            if (
                opponent_pos != (current_x + 1, current_y)
                or (current_x + 2, current_y) in self.get_board().get_v_fence()
            ):
                return False
        elif future_x - current_x == -2:
            if (
                opponent_pos != (current_x - 1, current_y)
                or (current_x - 1, current_y) in self.get_board().get_v_fence()
            ):
                return False
        elif future_y - current_y == 2:
            if (
                opponent_pos != (current_x, current_y + 1)
                or (current_x, current_y + 2) in self.get_board().get_h_fence()
            ):
                return False
        elif future_y - current_y == -2:
            if (
                opponent_pos != (current_x, current_y - 1)
                or (current_x, current_y - 1) in self.get_board().get_h_fence()
            ):
                return False

        return True

    def diagonal_validation(
        self, current_x, current_y, future_x, future_y, opponent_pos
    ):
        """Validates a diagonal move by the player. The only time it will return true is if the opponent
        is blocking the forward movement of the player and there are no fences in the way."""

        # if moving up right
        if future_x > current_x and future_y < current_y:

            # if opponent is to the right, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x + 1, current_y)
                and (current_x + 2, current_y) in self.get_board().get_v_fence()
                and (current_x + 1, current_y) not in self.get_board().get_h_fence()
            ):
                return True

            # if opponent is above, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x, current_y - 1)
                and (current_x, current_y - 1) in self.get_board().get_h_fence()
                and (current_x + 1, current_y - 1) not in self.get_board().get_v_fence()
            ):
                return True
            return False

        # if moving up left
        elif future_x < current_x and future_y < current_y:

            # if opponent is above, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x, current_y - 1)
                and (current_x, current_y - 1) in self.get_board().get_h_fence()
                and (current_x, current_y - 1) not in self.get_board().get_v_fence()
            ):
                return True

            # if opponent is to the left, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x - 1, current_y)
                and (current_x - 1, current_y) in self.get_board().get_v_fence()
                and (current_x - 1, current_y) not in self.get_board().get_h_fence()
            ):
                return True
            return False

        # if moving down left
        elif future_x < current_x and future_y > current_y:

            # if opponent is to the left, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x - 1, current_y)
                and (current_x - 1, current_y) in self.get_board().get_v_fence()
                and (current_x - 1, current_y + 1) not in self.get_board().get_h_fence()
            ):
                return True

            # if opponent is below, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x, current_y + 1)
                and (current_x, current_y + 2) in self.get_board().get_h_fence()
                and (current_x, current_y + 1) not in self.get_board().get_v_fence()
            ):
                return True
            return False

        # if moving down right
        elif future_x > current_x and future_y > current_y:

            # if opponent is to below, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x, current_y + 1)
                and (current_x, current_y + 2) in self.get_board().get_h_fence()
                and (current_x + 1, current_y + 1 not in self.get_board().get_v_fence())
            ):
                return True

            # if opponent is to the right, there is a fence behind the opponent,
            # and there is no fence next to opponent ,return True
            if (
                opponent_pos == (current_x + 1, current_y)
                and (current_x + 2, current_y) in self.get_board().get_v_fence()
                and (current_x + 1, current_y + 1) not in self.get_board().get_h_fence()
            ):
                return True
            return False

    def is_winner(self, player_num):
        """Returns True if a given Player is the winner of the game.
        Otherwise returns False."""

        positions = self.get_board().get_player_positions()
        if player_num == 1:
            position = positions[0]
            if position[1] == 8:
                return True
        else:
            position = positions[1]
            if position[1] == 0:
                return True
        return False

    def print_board(self):
        """Prints the board out for debugging purposes."""
        column = 0
        board = self.get_board()
        for row in range(10):
            while column < 9:
                if (column, row) in board.get_h_fence():
                    print(" _", end="")
                    column += 1
                else:
                    print("  ", end="")
                    column += 1

            if row == 9:
                continue

            print("\n", end="")
            column = 0
            while column < 10:
                if (column, row) in board.get_v_fence():
                    print("|", end="")
                else:
                    print(" ", end="")

                player_positions = board.get_player_positions()
                if (column, row) == player_positions[0]:
                    print("1", end="")
                elif (column, row) == player_positions[1]:
                    print("2", end="")
                elif column < 9:
                    print("+", end="")
                column += 1

            print("\n", end="")
            column = 0
        print("\n")


class Board:
    """Represents the game board as a list of tuples that act as coordinates
    on the Board. Each coordinate represents a cell and is referenced by the top left
    corner. This class also has two lists that store the coordinates of vertical fences and
    horizontal fences.
    This list primarily responsible for storing the coordinates of the cells, fences, and players.
    This class will communicate with QuoridorGame in order to validate Player moves and fence
    placement."""

    def __init__(self):
        """Initializes the game board by storing the coordinates of the cells
        as tuples in a list, and stores the vertical and horizontal fences
        in their own lists."""

        self._cells = list()
        self._v_fence = list()
        for num in range(9):
            self._v_fence.append((0, num))
        for num in range(9):
            self._v_fence.append((9, num))

        self._h_fence = list()
        for num in range(9):
            self._h_fence.append((num, 0))
        for num in range(9):
            self._h_fence.append((num, 9))

        self._player_positions = [(4, 0), (4, 8)]
        for row in range(9):
            for column in range(9):
                self._cells.append((column, row))

    def get_cells(self):
        """Returns the list of cells that make up the Board."""
        return self._cells

    def get_v_fence(self):
        """Returns the list of vertical fence coordinates."""
        return self._v_fence

    def get_h_fence(self):
        """Returns the list of horizontal fence coordinates."""
        return self._h_fence

    def get_player_positions(self):
        """Returns the list of player positions."""
        return self._player_positions

    def set_player_positions(self, player, coordinates):
        """Sets a given player's position to a given coordinate on the board."""
        self._player_positions[player - 1] = coordinates


class Player:
    """Represents a player of the QuoridorGame. Starts at their base line,
    in the middle of the bottom (4,8) or top (4,0) edge of the board. Has 10 fences
    to start with.
    This class is responsible for tracking how many fences the Player has.
    This class will communicate with Board in order to place fences, and
    will communicate with QuoridorGame to change Player turn."""

    def __init__(self, number):
        """Initialize the Player with a number and 10 fences."""

        self._player = number
        self._fences = 10

    def get_fence_count(self):
        """Returns the number of fences the Player has."""
        return self._fences

    def sub_fence_count(self):
        """Subtracts 1 from the player's fence count."""
        self._fences -= 1
        return
