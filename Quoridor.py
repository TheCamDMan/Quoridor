# Author: Cameron Blankenship
# Date: 8/3/2021
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
    composition. This class is also responsible for tracking the player
    turns."""

    def __init__(self):
        """Initializes the game Board, Players 1 and 2, sets it as
        the first Player's turn."""
        self._Board = Board()
        self._P1 = Player(1)
        self._P2 = Player(2)
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

    def move_pawn(self, player, coordinates):
        """Moves the given Player to the given coordinates on the Board, if
        it is a valid move. If move is forbidden or game has already won,
        return False. Otherwise return True."""
        pass

    def place_fence(self, player, fence_type, coordinates):
        """Places a given Player's fence of given fence_type at the given
        coordinates, if it is a valid fence placement. If not a valid
        fence placement or game has already been won, return False.
        Otherwise return True."""
        pass

    def is_winner(self, player):
        """Returns True if a given Player is the winner of the game.
        Otherwise returns False."""
        pass


class Board:
    """Represents the game board as a list of tuples that act as coordinates
    on the Board. Each coordinate represents a cell and is referenced by the top left
    corner. This class also has two lists that store the coordinates of vertical fences and
    horizontal fences.
    This class is also responsible for validating Player movements, as
    well as where each fence is placed and validating fence placement. This class will
    communicate with Player and QuoridorGame in order to validate Player moves and fence
    placement."""

    def __init__(self):
        """Initializes the game board by storing the coordinates of the cells
        as tuples in a list, and stores the vertical and horizontal fences
        in their own lists."""

        self._cells = list()
        self._v_fence = list()
        self._h_fence = list()
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

    def validate_fence_place(self, coordinates):
        """Validates the placement of the fences by ensuring that no fence
        is already at the given coordinates parameter, that the player has
        fences available to them, and that the fence is inbounds of the
        Board."""
        pass

    def validate_pawn_move(self, coordinates):
        """Validates the Player move by ensuring that there is no fence
        blocking their path, that the move is inbounds of the board, and
        that the move is valid given the circumstance.
        Takes a coordinates parameter."""
        pass

    def print_board(self):
        """Prints the board out for debugging purposes."""
        pass


class Player:
    """Represents a player of the QuoridorGame. Starts at their base line,
    in the middle of the left or right edge of the board. Has ten fences
    to start with.
    This class is responsible for tracking how many fences the Player has,
    moving the pawn across the board, and placing fences on the board.
    This class will communicate with Board in order to track movements, and
    will communicate with QuoridorGame to change Player turn."""

    def __init__(self, number):
        """Initialize the Player with number, ten fences, and starting
        coordinates based on which Player they are."""

        self._player = number

        if self._player == 1:
            self._player_position = (0, 4)
        elif self._player == 2:
            self._player_position = (8, 4)

        self._fences = 10

    def get_player_position(self):
        """Returns the player position coordinates."""
        return self._player_position

    def get_fence_count(self):
        """Returns the number of fences the Player has."""
        return self._fences



"""DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

1. How to store the Board:

Board will be stored as a list of tuples that contain the coordinates
of each cell. The fences will be stored as the coordinates where they 
were placed in the list that corresponds to the orientation of the fence.

2. Initializing the board:
    
    for each row up to 8:
        for each column up to 8:
            add a tuple with those coordinates to the list
    
    make a list to hold player coordinates
    make a list to hold vertical fences
    make a list to hold horizontal fences

3. How to track which player's turn it is to play:
    
    create a data-member in QuoridorGame class that will store player_turn
    as a variable, starting with 1 when initialized for the first time.

    when Player takes a turn, whether it be placing fence or moving pawn,
    use set_player_turn to set the next move to the opposite Player's turn.

4. How to validate moving of a pawn:

    look at the pawn's position
    if pawn is trying to move outside of edges of board:
        return False
    if pawn is moving right:
        check vertical fence list for a fence at next cell
        if there is a fence:
            return False
        if there is no fence:
            update pawn position
            return True
    if pawn is moving up:
        check horizontal fence list for a fence at the current cell
        if there is a fence:
            return False
        if there if no fence:
            update pawn position
            return True
    if pawn is moving down:
        check horizontal fence list for a fence a the cell below current cell
        if there is a fence:
            return False
        if there is no fence:
            update fence position
            return True
    if pawn is moving left:
        check vertical fence list for a fence at the current cell
        if there is a fence:
            return False
        if there is no fence:
            update pawn position
            return True
    if pawn if moving diagonal:
        check to see if other player is in the position directly adjacent to the player
        if not:
            return False
        else:
            update player position
            return True
            
5. How to validate placing of the fences:

    store the type of fence and desired coordinates in variable
    if the fence is trying to be placed outside the edges of board:
        return False
    if there is a fence of the same type at that position:
        return False
    else:
        update player fence count
        store fence coordinates into the correct fence type list
        
6. How to track fences on and off the board:

    Player has data member that will keep track of fence count.
    Each time player places a new fence, the count will be decremented.
    If count is 0, player will not be able to place fence.
    
    Fences on the board will be tracked by two lists. One for vertical
    fences and one for horizontal fences.
    
7. How to track the pawn's position on the board:

    player position will be stored as a data member in the Player class.
    It will have a get and set method in order to access and change.
    Position will be cross-referenced with fence lists in Board class to ensure
    validity of move.
    """