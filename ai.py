from chesspiecesandboard import *
from checkLogic import * 
import copy
import random


def AImoveLogic(event, data):
	pass
def AI(color, board):
	pieces = getPieces(color, board)
	piece = random.choice(pieces)
	moveList = piece.legalMoves(board)
	copyMoveList = copy.deepcopy(moveList)
	for checkMove in moveList:
		checkBoard = makeMove(board, checkMove, piece)
		newKing = findPiece(data.selectedPiece.giveColor(), King, checkBoard)
		if inCheck(newKing, checkBoard):
			copyMoveList.remove(checkMove)
	moveList = copyMoveList
	if moveList != []:
		move = random.choice(piece.legalMoves(board)) # generates moves
	piece.move(move)
	x = move[0]
	y = move[1]
	board[x][y] = piece
	board[oldSquare[0]][oldSquare[1]] = 0

def getPieces(color, board):
	pieces = []
	for x in range(len(board)):
	for y in range(len(board)):
	if isinstance(board[x][y], Piece) and board[x][y].giveColor() == color:
		pieces.append([x, y])
	return pieces