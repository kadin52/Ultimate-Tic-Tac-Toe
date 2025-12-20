# Ultimate Tic Tac Toe

This is a game of Ultimate Tic Tac Toe, written in python. The GUI is created using PyGame.

<p align="center">
	<img src="Images/Completed Board.png" width=50%></img>
</p>

## How To Play

On the surface, ultimate tic tac toe is the same as the standard game: there are nine squares arranged in a 3x3 grid which can each be marked as either an 'X' or an 'O', and three in a row wins the game. Unlike the original game, however, you cannot simply mark a square as 'X' or 'O'. Instead, each square consists of an additional tic tac toe game, which must be won to mark the big square. The overall board is called the 'global board', and the smaller boards are called 'local boards'. The game is won when a player wins three local boards in a row.

On the first turn, Player 'X' can choose any square in any local board they like. From then on, however, the next move will be determined in part by the previous player's move. For example, if Player 'X' plays in the bottom left square of their local board, Player 'O' must then make their next move somewhere in the bottom left local board. This will then determine which local board Player 'X' must play in, and so on. This creates interesting situations in which you may purposefully not win a local board for fear of placing your opponent in an even better position.

<p align="center">
	<img src="Images/First Move.png" width=50%></img>
</p>

#### [Other difficulties need to be developed]

## Prerequisites

In order to run the game you must have PyGame installed on your computer, which can be done using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pygame
```
