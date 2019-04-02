Blocky Game
Introduction: the Blocky game
Blocky is a game with simple moves on a simple structure, but like a Rubik’s Cube, it is quite challenging to play. The game is played on a randomly-generated game board made of squares of four different colors, such as this:
Each player has their own goal that they are working towards, such as creating the largest connected “blob” of blue. After each move, the player sees their score, determined by how well they have achieved their goal. The game continues for a certain number of turns, and the player with the highest score at the end is the winner.
Now let’s look in more detail at the rules of the game and the different ways it can be configured for play.
The Blocky board
We call the game board a ‘block’. It is best defined recursively. A block is either:
•	a square of one color, or
•	a square that is subdivided into 4 equal-sized blocks.
The largest block of all, containing the whole structure, is called the top-level block. We say that the top-level block is at level 0. If the top-level block is subdivided, we say that its four sub-blocks are at level 1. More generally, if a block at level k is subdivided, its four sub-blocks are at level k+1.
A Blocky board has a maximum allowed depth, which is the number of levels down it can go. A board with maximum allowed depth 0 would not be fun to play on – it couldn’t be subdivided beyond the top level, meaning that it would be of one solid color. This board was generated with maximum depth 5:
For scoring, the units of measure are squares the size of the blocks at the maximum allowed depth. We will call these blocks unit cells.

Moves
These are the moves that are allowed on a Blocky board:
•	Rotate the selected block either clockwise or counterclockwise
•	Swap the 4 sub-blocks within the selected block horizontally or vertically
•	“Smash” the selected block: whether it is a solid-colored block or is already subdivided, give it four new, randomly-generated sub-blocks. Smashing the top-level block is not allowed – that would be creating a whole new game. And smashing a unit cell is also not allowed, since it’s already at the maximum allowed depth.

Goals and scoring
At the beginning of the game, each player is assigned a randomly-generated goal. There are two types of goal:
•	Blob goal.
The player must aim for the largest “blob” of a given colour c. A blob is a group of connected blocks with the same colour. Two blocks are connected if their sides touch; touching corners doesn’t count. The player’s score is the number of unit cells in the largest blob of colour c.
•	Perimeter goal.
The player must aim to put the most possible units of a given colour c on the outer perimeter of the board. The player’s score is the total number of unit cells of colour c that are on the perimeter. There is a premium on corner cells: they count twice towards the score.
Notice that both goals are relative to a particular colour. We will call that the target colour for the goal.

Players
The game can be played solitaire (with a single player) or with two or more players. There is no defined limit on the number of players, although the game would not likely be fun to play with a very large number of players.
There are three kinds of player:
•	A human player chooses moves based on user input. Human players are limited to one smash move per game.
•	A random player is a computer player that, as the name implies, chooses moves randomly. Random players have no limit on their smashes. But if they randomly choose to smash the top-level block or a unit cell, neither of which is permitted, they forfeit their turn.
•	A smart player is a computer player that chooses moves more intelligently: It generates a set of random moves and, for each, checks what its score would be if it were to make that move. Then it picks the one that yields the best score. Smart players cannot smash.
Configurations of the game
A Blocky game can be configured in several ways:
•	Maximum allowed depth.
While the specific colour pattern for the board is randomly generated, we control how finely subdivided the squares can be.
•	Number and type of players.
There can be any number of players of each type. The “difficulty” of a smart player (how hard it is to play against) can also be configured.
•	Number of moves.
A game can be configured to run for any desired number of moves. (A game will end early if any player closes the game window.)
Setup and code
•	block.py
•	game.py
•	goal.py
•	player.py
•	renderer.py. 
