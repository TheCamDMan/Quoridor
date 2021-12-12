## Game

You can see the rules of the game in this [video](https://www.youtube.com/watch?v=6ISruhN0Hc0) and [Page 9 of this educative-sheet_quoridor-english.pdf](https://en.gigamic.com/files/media/fiche_pedagogique/educative-sheet_quoridor-english.pdf) You can implement the fair play rule for extra credit but you are not required to.

This is a two-player version of the game.  Each player will have 10 fences.

The board is formed by 9x9 cells, and the pawn will move on the cells.  The fence will be placed on the edges of the cells.  The four sides of the board are treated as fences and no more fence should be placed on top of it.

The board should be treated as the following picture shows:

![162-u21-portfolio-project-quorridor-board](https://user-images.githubusercontent.com/230170/127580651-5de99bfd-d7d4-4492-9ef2-a5615f0e8b3b.png)

 
The cell coordinates are expressed in `(x,y)` where `x` is the column number and `y` is the row numberThe board positions start with `(0,0)` and end at `(8,8)`. At the beginning of the game, player 1 places pawn 1 (P1) on the top center of the board and player 2 places pawn 2 (P2) on the bottom center of the board.  The position of P1 and P2 is `(4,0)` and `(4,8)` when the game begins.   

The four edges are labeled as fences. The row of the cells where the pawns are positioned at the start of the game are called base lines. A fence is 1 cell long in contrast to what you find the video and PDF saying.

When each player tries to place a fence on the board, the position of the fence is defined by a letter and coordinates.  For vertical fences, we use `v` and for horizontal fences, we use `h`.  As an example, for the blue fence (vertical) in the picture, we use the coordinate of the top corner to define it and for the red fence (horizontal), we use coordinate of the left corner to define it. 

## Validation rules

For example, jumping over the pawn is allowed only when the two pawns face each other. Diagonal movement is allowed when blocked by pawn + fence. A fence only blocks 1 square. Fences cannot be moved once placed thus they cannot be reused. All the rules from the video and the PDF apply unless the README or an Instructor explicitly says otherwise. Preventing the blocking of baseline is considered a part of fair-play rule (See Extra credit section below)

## Playing the game

Player 1 will start the game. Each player takes turn playing. On a player’s turn they will make one move. They can either move the pawn (`move_pawn`) or place a fence (`place_fence`). Your program should be able to determine whether the movement is valid. A turn lasts until the player has made a valid move.
 
The first player whose pawn reaches any of the cells of the opposite player's base line wins the game. No turn can be played after a player has won.

## How your game will be played?

Here's a very simple example of how your QuoridorGame class will be used and is expected to behave, by the autograder or a TA:

```
q = QuoridorGame()
q.move_pawn(2, (4,7)) #moves the Player2 pawn -- invalid move because only Player1 can start, returns False
q.move_pawn(1, (4,1)) #moves the Player1 pawn -- valid move, returns True
q.place_fence(1, 'h',(6,5)) #places Player1's fence -- out of turn move, returns False 
q.move_pawn(2, (4,7)) #moves the Player2 pawn -- valid move, returns True
q.place_fence(1, 'h',(6,5)) #places Player1's fence -- returns True
q.place_fence(2, 'v',(3,3)) #places Player2's fence -- returns True
q.is_winner(1) #returns False because Player 1 has not won
q.is_winner(2) #returns False because Player 2 has not won

```
