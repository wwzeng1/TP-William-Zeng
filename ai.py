from chesspiecesandboard import *
from checkLogic import * 
import copy
import random


def AImoveLogic(event, data):
	if (data.isWTurn == True and data.aiColor == "Black") or (data.isWTurn == False and data.aiColor == "White"):
		moveLogic(event, data)

def aiMoves(data):
	if not (data.isWTurn == True and data.aiColor == "Black") and not (data.isWTurn == False and data.aiColor == "White"):
		data.isWTurn = not data.isWTurn
		if data.aiColor == "White": isMaximisingPlayer = True
		else: isMaximisingPlayer = False
		(square, move) = minimaxRoot(1, data.board, isMaximisingPlayer)
		print((square, move))
		piece = data.board[square[0]][square[1]]
		print(piece)
		piece.move(move)
		data.board[move[0]][move[1]] = piece
		data.board[square[0]][square[1]] = 0
		printBoard(data.board)		

def generateAllMoves(color, board):
	pieces = []
	movesList = []
	for x in range(len(board)):
		for y in range(len(board)):
			if isinstance(board[x][y], Piece) and board[x][y].giveColor() == color:
				pieces.append([x, y])
	for piece in pieces:
		x = piece[0]
		y = piece[1]
		oldSquare = [x, y]
		square = board[x][y]
		moveList = square.legalMoves(board)
		if moveList != []:
			for checkMove in moveList:
					checkBoard = makeMove(board, square, checkMove, oldSquare)
					king = findPiece(square.giveColor(), King, checkBoard)
					if inCheck(king, checkBoard):
						moveList.remove(checkMove)
			for move in moveList:
				movesList.append((square, move, oldSquare))
	return movesList

def boardValue(board):
	pST = dict()
	# pST[WP] = [[0, 0, 0, 0, 0, 0, 0, 0],
	# 			[5, 5, 5, 5, 5, 5, 5, 5],
	# 			[1, 1, 2, 3, 3, 2, 1, 1],
	# 			[.5, .5, 1, 2.5, 2.5, 1, .5, .5],
	# 			[0, 0, 0, 2, 2, 0, 0, 0],
	# 			[.5, -.5, -1, 0, 0, -1, -.5, .5],
	# 			[.5, 1, 1,-2,-2, 1, 1, .5],
	# 			[0, 0, 0, 0, 0, 0, 0, 0]]
	# pST[BP] = [[0, 0, 0, 0, 0, 0, 0, 0],
	# 			[5, 5, 5, 5, 5, 5, 5, 5],
	# 			[1, 1, 2, 3, 3, 2, 1, 1],
	# 			[.5, .5, 1, 2.5, 2.5, 1, .5, .5],
	# 			[0, 0, 0, 2, 2, 0, 0, 0],
	# 			[.5, -.5, -1, 0, 0, -1, -.5, .5],
	# 			[.5, 1, 1,-2,-2, 1, 1, .5],
	# 			[0, 0, 0, 0, 0, 0, 0, 0]]			
	boardValue = 0
	mult = 0
	for x in range(len(board)):
		for y in range(len(board)):
			piece = board[x][y]
			if isinstance(piece, Piece):
				if piece.giveColor() == "Black": mult = -1
				elif piece.giveColor() == "White": mult = 1
				# boardValue += pST[str(piece)][x][y]
				boardValue += (piece.value * mult)
	return boardValue

def checkMove(board, piece, move, oldSquare):
    copyBoard = copy.deepcopy(board)
    x = move[0]
    y = move[1]
    copyBoard[x][y] = piece
    copyBoard[oldSquare[0]][oldSquare[1]] = 0
    return copyBoard

def reverseMove(board, piece, move, oldSquare):
    copyBoard = copy.deepcopy(board)
    x = move[0]
    y = move[1]
    copyBoard[x][y] = 0
    copyBoard[oldSquare[0]][oldSquare[1]] = piece
    return copyBoard

# found from online https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977
def minimaxRoot(depth, board, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    allMoves = generateAllMoves(color, board)
    bestSquare = []
    bestMove = -9999
    bestMoveFound = []
    for (square, move, oldSquare) in allMoves:
        board = checkMove(board, square, move, oldSquare)
        value = minimax(depth, board, not isMaximisingPlayer)
        print(str(square), str(value))
        board = reverseMove(board, square, move, oldSquare)
        if value >= bestMove:
            bestMove = value
            bestMoveFound = move
            bestSquare = oldSquare
        print(str(bestMoveFound), str(bestMove))
    return (bestSquare, bestMoveFound)

def minimax(depth, board, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    if (depth == 0):
        return boardValue(board)
    allMoves = generateAllMoves(color, board)
    if (isMaximisingPlayer):
        bestMove = -9999
        for (square, move, oldSquare) in allMoves:
            board = checkMove(board, square, move, oldSquare)
            bestMove = max(bestMove, minimax(depth - 1, board, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare)
        return bestMove
    else:
        bestMove = 9999
        for (square, move, oldSquare) in allMoves:
            board = checkMove(board, square, move, oldSquare)
            bestMove = min(bestMove, minimax(depth - 1, board, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare)
        return bestMove