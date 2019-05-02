This is Pixel Chess, a chess game with local multiplayer and solo games versus the computer, 
with different levels of difficulty. It uses principled variation search with alpha/beta pruning, 
as well as a basic minimax implementation. The principled variation search(pvs), thinks 8 moves ahead, 
covering approximately 20^8 total board states using pruning and search optimization. The minimax implementation
thinks about 3 moves ahead, covering 20^3 only using alpha/beta pruning. 

To run this game, just click chess.py!

Shortcuts include:
r: to restart the game after a checkmate 
h: to go to the help screen.
p: pausing the game to return to main menu